
from typing import Optional
from app.models.email import EmailDiscoveryResult
from app.services.verification.email_verifier import EmailVerifier
from app.services.scraping.email_pattern import EmailPatternDetector
from app.services.scraping.linkedin_scraper import LinkedInScraper

class EmailDiscoveryService:
    '''
    Waterfall email discovery service
    Tries multiple methods to find and verify emails
    '''
    
    def __init__(self):
        self.verifier = EmailVerifier()
        self.pattern_detector = EmailPatternDetector()
    
    async def discover_email(
        self,
        first_name: str,
        last_name: str,
        company: str,
        company_domain: Optional[str] = None,
        linkedin_url: Optional[str] = None
    ) -> EmailDiscoveryResult:
        '''
        Discover email using multiple methods
        1. Try LinkedIn search
        2. Generate email patterns from company domain
        3. Verify with highest confidence
        '''
        
        result = EmailDiscoveryResult(
            first_name=first_name,
            last_name=last_name,
            company=company
        )
        
        # If no domain provided, try to guess from company name
        if not company_domain:
            # Simple heuristic: company.com
            company_domain = f'{company.lower().replace(" ", "")}.com'
        
        # Method 1: Try LinkedIn search (optional)
        if not linkedin_url:
            try:
                with LinkedInScraper(headless=True) as scraper:
                    linkedin_url = scraper.search_profile(
                        f'{first_name} {last_name}',
                        company
                    )
                    if linkedin_url:
                        result.linkedin_url = linkedin_url
            except Exception as e:
                print(f'LinkedIn search failed: {e}')
        
        # Method 2: Generate email patterns
        possible_emails = self.pattern_detector.generate_email(
            first_name,
            last_name,
            company_domain
        )
        
        # Method 3: Verify each possible email
        best_email = None
        best_confidence = 0.0
        best_pattern = None
        
        for email, pattern in possible_emails:
            is_valid, confidence, message = self.verifier.verify(email)
            
            if is_valid and confidence > best_confidence:
                best_email = email
                best_confidence = confidence
                best_pattern = pattern
        
        # Update result
        if best_email:
            result.email = best_email
            result.confidence = best_confidence
            result.verified = True
            result.source = f'pattern:{best_pattern}'
        else:
            result.error = 'No valid email found'
            result.confidence = 0.0
        
        return result
