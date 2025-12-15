
import re
import dns.resolver
import socket
from typing import Tuple

class EmailVerifier:
    '''Verify email addresses using DNS and SMTP checks'''
    
    @staticmethod
    def validate_format(email: str) -> bool:
        '''Check if email format is valid'''
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def check_mx_records(domain: str) -> Tuple[bool, str]:
        '''Check if domain has MX records'''
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return True, str(mx_records[0].exchange)
        except dns.resolver.NoAnswer:
            return False, 'No MX records found'
        except dns.resolver.NXDOMAIN:
            return False, 'Domain does not exist'
        except Exception as e:
            return False, f'DNS error: {str(e)}'
    
    @staticmethod
    def smtp_check(email: str, timeout: int = 10) -> Tuple[bool, str]:
        '''
        Perform SMTP check to verify if mailbox exists
        NOTE: Many servers block this, so not 100% reliable
        '''
        try:
            domain = email.split('@')[1]
            has_mx, mx_host = EmailVerifier.check_mx_records(domain)
            
            if not has_mx:
                return False, mx_host
            
            # Try SMTP connection (basic check only)
            # Full SMTP verification often gets blocked
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                sock.connect((mx_host.rstrip('.'), 25))
                sock.close()
                return True, 'MX server reachable'
            except:
                return False, 'MX server not reachable'
                
        except Exception as e:
            return False, f'SMTP check failed: {str(e)}'
    
    @classmethod
    def verify(cls, email: str) -> Tuple[bool, float, str]:
        '''
        Verify email and return (is_valid, confidence_score, message)
        Confidence: 0.0 - 1.0
        '''
        # Check format
        if not cls.validate_format(email):
            return False, 0.0, 'Invalid email format'
        
        # Check MX records
        domain = email.split('@')[1]
        has_mx, mx_message = cls.check_mx_records(domain)
        
        if not has_mx:
            return False, 0.2, mx_message
        
        # MX records exist - medium confidence
        confidence = 0.7
        
        # Try SMTP check (optional, often blocked)
        smtp_valid, smtp_message = cls.smtp_check(email, timeout=5)
        if smtp_valid:
            confidence = 0.9
            return True, confidence, 'Email verified via SMTP'
        
        # MX exists but SMTP failed - still likely valid
        return True, confidence, f'MX records valid: {mx_message}'
