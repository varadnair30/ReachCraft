
import re
from typing import Optional, List, Tuple
from urllib.parse import urlparse

class EmailPatternDetector:
    '''Detect email patterns from company websites'''
    
    # Common email patterns
    PATTERNS = [
        '{first}.{last}@{domain}',
        '{first}{last}@{domain}',
        '{first}@{domain}',
        '{f}{last}@{domain}',
        '{first}.{l}@{domain}',
        '{first}_{last}@{domain}',
    ]
    
    @staticmethod
    def extract_emails_from_text(text: str) -> List[str]:
        '''Extract all email addresses from text'''
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def detect_pattern(known_emails: List[str], domain: str) -> Optional[str]:
        '''
        Detect email pattern from known emails
        Returns pattern like '{first}.{last}@{domain}'
        '''
        if not known_emails:
            return None
        
        # Analyze first known email
        email = known_emails[0]
        local_part = email.split('@')[0]
        
        # Try to identify pattern
        if '.' in local_part:
            return '{first}.{last}@{domain}'
        elif '_' in local_part:
            return '{first}_{last}@{domain}'
        else:
            # Could be firstname or firstnamelastname
            return '{first}{last}@{domain}'
    
    @staticmethod
    def generate_email(
        first_name: str,
        last_name: str,
        domain: str,
        pattern: Optional[str] = None
    ) -> List[Tuple[str, str]]:
        '''
        Generate possible emails based on pattern
        Returns list of (email, pattern) tuples
        '''
        first = first_name.lower().strip()
        last = last_name.lower().strip()
        f = first[0] if first else ''
        l = last[0] if last else ''
        
        results = []
        
        if pattern:
            # Use specific pattern
            email = pattern.format(
                first=first,
                last=last,
                f=f,
                l=l,
                domain=domain
            )
            results.append((email, pattern))
        else:
            # Try all common patterns
            for p in EmailPatternDetector.PATTERNS:
                try:
                    email = p.format(
                        first=first,
                        last=last,
                        f=f,
                        l=l,
                        domain=domain
                    )
                    results.append((email, p))
                except:
                    continue
        
        return results
    
    @staticmethod
    def extract_domain_from_url(url: str) -> str:
        '''Extract domain from URL'''
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # Remove www.
        domain = re.sub(r'^www\.', '', domain)
        return domain
