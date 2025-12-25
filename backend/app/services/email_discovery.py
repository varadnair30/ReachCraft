

"""
Email Discovery Service
Finds and verifies email addresses using pattern generation and SMTP verification
No paid APIs required!
"""
import re
import smtplib
import dns.resolver
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailDiscoveryService:
    """
    Discovers email addresses through:
    1. Pattern generation (common formats)
    2. SMTP verification (check if mailbox exists)
    """

    # Common email patterns
    PATTERNS = [
        "{first}.{last}@{domain}",           # john.doe@company.com
        "{first}@{domain}",                  # john@company.com
        "{first}{last}@{domain}",            # johndoe@company.com
        "{f}{last}@{domain}",                # jdoe@company.com
        "{first}.{l}@{domain}",              # john.d@company.com
        "{first}_{last}@{domain}",           # john_doe@company.com
        "{last}.{first}@{domain}",           # doe.john@company.com
    ]

    def __init__(self):
        pass

    def generate_email_patterns(
        self, 
        first_name: str, 
        last_name: str, 
        domain: str
    ) -> List[str]:
        """
        Generate possible email addresses based on common patterns

        Args:
            first_name: Person's first name
            last_name: Person's last name
            domain: Company domain (e.g., 'company.com')

        Returns:
            List of possible email addresses
        """
        # Clean inputs
        first = first_name.lower().strip()
        last = last_name.lower().strip() if last_name else ""
        domain = domain.lower().strip()

        # Remove common domain prefixes
        domain = domain.replace('www.', '').replace('http://', '').replace('https://', '')

        candidates = []

        for pattern in self.PATTERNS:
            try:
                email = pattern.format(
                    first=first,
                    last=last,
                    f=first[0] if first else "",
                    l=last[0] if last else "",
                    domain=domain
                )

                # Validate email format
                if self._is_valid_email_format(email):
                    candidates.append(email)
            except (KeyError, IndexError):
                # Skip patterns that don't apply (e.g., no last name)
                continue

        # Remove duplicates while preserving order
        seen = set()
        unique_candidates = []
        for email in candidates:
            if email not in seen:
                unique_candidates.append(email)
                seen.add(email)

        logger.info(f"Generated {len(unique_candidates)} email patterns for {first_name} {last_name}")
        return unique_candidates

    def verify_email_smtp(self, email: str, timeout: int = 10) -> Dict[str, any]:
        """
        Verify if an email address exists using SMTP without sending an email

        Args:
            email: Email address to verify
            timeout: SMTP connection timeout in seconds

        Returns:
            Dict with:
                - valid: bool
                - confidence: float (0.0 to 1.0)
                - reason: str
        """
        try:
            # Extract domain
            domain = email.split('@')[1]

            # Get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_host = str(mx_records[0].exchange)
            except Exception as dns_err:
                logger.warning(f"No MX records for {domain}: {dns_err}")
                return {
                    "valid": False,
                    "confidence": 0.0,
                    "reason": "No MX records found"
                }

            # Connect to mail server
            try:
                server = smtplib.SMTP(timeout=timeout)
                server.set_debuglevel(0)
                server.connect(mx_host)
                server.helo(server.local_hostname)
                server.mail('verify@example.com')

                code, message = server.rcpt(email)
                server.quit()

                # SMTP response codes:
                # 250 = Email exists
                # 550 = Email doesn't exist
                # 451/452 = Greylisted (might exist)

                if code == 250:
                    return {
                        "valid": True,
                        "confidence": 0.9,
                        "reason": "SMTP verified (250)"
                    }
                elif code in [451, 452]:
                    return {
                        "valid": True,
                        "confidence": 0.5,
                        "reason": f"Greylisted ({code})"
                    }
                else:
                    return {
                        "valid": False,
                        "confidence": 0.1,
                        "reason": f"SMTP rejected ({code})"
                    }

            except smtplib.SMTPServerDisconnected:
                # Some servers disconnect immediately (anti-spam)
                return {
                    "valid": True,
                    "confidence": 0.3,
                    "reason": "Server disconnected (likely exists)"
                }
            except smtplib.SMTPConnectError:
                return {
                    "valid": False,
                    "confidence": 0.0,
                    "reason": "Cannot connect to mail server"
                }
            except Exception as smtp_err:
                logger.warning(f"SMTP verification failed for {email}: {smtp_err}")
                return {
                    "valid": True,
                    "confidence": 0.2,
                    "reason": f"SMTP error: {str(smtp_err)[:50]}"
                }

        except Exception as e:
            logger.error(f"Email verification failed for {email}: {e}")
            return {
                "valid": False,
                "confidence": 0.0,
                "reason": f"Verification error: {str(e)[:50]}"
            }

    def discover_email(
        self, 
        first_name: str, 
        last_name: str, 
        company_domain: str,
        verify: bool = True
    ) -> List[Dict[str, any]]:
        """
        Discover and verify email addresses for a person

        Args:
            first_name: Person's first name
            last_name: Person's last name
            company_domain: Company domain (e.g., 'twitch.tv')
            verify: Whether to verify emails via SMTP

        Returns:
            List of dicts with email candidates and confidence scores
        """
        # Generate patterns
        candidates = self.generate_email_patterns(first_name, last_name, company_domain)

        results = []

        for email in candidates:
            result = {
                "email": email,
                "pattern": self._get_pattern_name(email, first_name, last_name),
                "valid": None,
                "confidence": 0.5,  # Default for unverified
                "reason": "Pattern generated"
            }

            # Verify if requested
            if verify:
                verification = self.verify_email_smtp(email)
                result.update(verification)

            results.append(result)

        # Sort by confidence (highest first)
        results.sort(key=lambda x: x["confidence"], reverse=True)

        logger.info(f"Discovered {len(results)} email candidates for {first_name} {last_name}")
        return results

    def _is_valid_email_format(self, email: str) -> bool:
        """Check if email has valid format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _get_pattern_name(self, email: str, first_name: str, last_name: str) -> str:
        """Get human-readable pattern name"""
        local = email.split('@')[0]
        first = first_name.lower()
        last = last_name.lower() if last_name else ""

        if local == f"{first}.{last}":
            return "first.last"
        elif local == first:
            return "first"
        elif local == f"{first}{last}":
            return "firstlast"
        elif local == f"{first[0]}{last}":
            return "flast"
        elif local == f"{first}.{last[0]}":
            return "first.l"
        elif local == f"{first}_{last}":
            return "first_last"
        elif local == f"{last}.{first}":
            return "last.first"
        else:
            return "other"