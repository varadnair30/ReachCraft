from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup
import time
from typing import Optional, Dict
import re

class LinkedInScraper:
    '''
    Basic LinkedIn profile scraper
    NOTE: LinkedIn has strong anti-bot measures
    This is a simple implementation for educational purposes
    '''
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    def start(self):
        '''Start browser'''
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        
        # Set realistic user agent
        self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def close(self):
        '''Close browser'''
        if self.browser:
            self.browser.close()
    
    def search_profile(self, name: str, company: str) -> Optional[str]:
        '''
        Search for LinkedIn profile URL via Google
        Returns profile URL if found
        '''
        if not self.page:
            self.start()
        
        try:
            # Use Google to find LinkedIn profile
            query = f'site:linkedin.com/in {name} {company}'
            search_url = f'https://www.google.com/search?q={query}'
            
            self.page.goto(search_url, wait_until='networkidle')
            time.sleep(2)
            
            # Extract LinkedIn URLs from results
            content = self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find LinkedIn profile links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'linkedin.com/in/' in href:
                    # Extract clean LinkedIn URL
                    match = re.search(r'https://[a-z]{2,3}\.linkedin\.com/in/[^/&?]+', href)
                    if match:
                        return match.group(0)
            
            return None
        
        except Exception as e:
            print(f'LinkedIn search error: {e}')
            return None
    
    def extract_profile_info(self, profile_url: str) -> Dict[str, Optional[str]]:
        '''
        Extract basic info from LinkedIn profile
        NOTE: Requires login for full access - this is a basic scraper
        '''
        if not self.page:
            self.start()
        
        try:
            self.page.goto(profile_url, wait_until='networkidle')
            time.sleep(2)
            
            content = self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try to extract name, title, company
            # This will only work for public profiles
            name = None
            title = None
            company = None
            
            # Look for name in title or h1
            title_tag = soup.find('title')
            if title_tag:
                # Format: "Name | LinkedIn"
                name = title_tag.text.split('|')[0].strip()
            
            return {
                'name': name,
                'title': title,
                'company': company,
                'linkedin_url': profile_url
            }
        
        except Exception as e:
            print(f'Profile extraction error: {e}')
            return {}
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
