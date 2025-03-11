"""
Browser management and web interaction tools
"""
import os
import time
import random
from typing import Dict, List, Any, Optional
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default values
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
DEFAULT_HEADERS = ["h1", "h2", "h3"]
DEFAULT_CONTENT = ["p", "article"]


class WebBrowser:
    """Class for managing browser and web interactions"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
    
    def __enter__(self):
        """Initialization when entering context manager"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting context manager"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
    
    def navigate(self, url: str):
        """Navigate to specified URL"""
        try:
            self.page.goto(url, timeout=DEFAULT_TIMEOUT * 1000)
            return True
        except Exception:
            return False
    
    def emulate_human(self):
        """Emulate human behavior to bypass bot detection"""
        # Random pause
        time.sleep(random.uniform(1, 3))
        
        # Random scrolling
        self.page.mouse.wheel(0, random.randint(300, 700))
        time.sleep(random.uniform(0.5, 1.5))
        
        # Random mouse movement
        self.page.mouse.move(
            random.randint(100, 500),
            random.randint(100, 500)
        )
    
    def extract_content(self, header_selectors: List[str] = None, 
                       content_selectors: List[str] = None) -> Dict[str, Any]:
        """Extract content from page using specified selectors"""
        if not header_selectors:
            header_selectors = DEFAULT_HEADERS
        if not content_selectors:
            content_selectors = DEFAULT_CONTENT
            
        # Extract text by selectors
        headers = []
        for selector in header_selectors:
            try:
                elements = self.page.query_selector_all(selector)
                headers.extend([el.text_content().strip() for el in elements])
            except Exception:
                continue
                
        paragraphs = []
        for selector in content_selectors:
            try:
                elements = self.page.query_selector_all(selector)
                paragraphs.extend([el.text_content().strip() for el in elements])
            except Exception:
                continue
                
        return {
            "url": self.page.url,
            "content": {
                "headers": headers,
                "paragraphs": paragraphs
            }
        }
    
    def google_search(self, query: str) -> List[str]:
        """Perform Google search and return results"""
        # Go to Google
        self.navigate("https://www.google.com")
        
        # Accept cookies if needed
        try:
            accept_button = self.page.get_by_role(
                "button",
                name="Accept all"
            )
            accept_button.click()
        except Exception:
            pass
            
        # Perform search
        self.page.fill('textarea[name="q"]', query)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("networkidle")
        
        # Extract results
        results = []
        for result in self.page.query_selector_all("div.g"):
            try:
                link = result.query_selector("a")
                if link and link.get_attribute("href"):
                    url = link.get_attribute("href")
                    if url.startswith("http"):
                        results.append(url)
            except Exception:
                continue
                
        return results[:5]  # Return top 5 results
    
    def visit_news_site(self, url: str) -> Dict[str, Any]:
        """Visit news site and collect content"""
        if not self.navigate(url):
            return {
                "url": url,
                "content": {
                    "headers": [],
                    "paragraphs": []
                }
            }
            
        # Define selectors based on site
        header_selectors = DEFAULT_HEADERS
        content_selectors = DEFAULT_CONTENT
        
        domain = url.split("//")[-1].split("/")[0]
        
        # Site-specific selectors
        if "bbc" in domain:
            content_selectors = ["article", ".article__body-content"]
        elif "reuters" in domain:
            content_selectors = ["article", ".article-body"]
        elif "bloomberg" in domain:
            content_selectors = ["article", ".body-content"]
            
        return self.extract_content(header_selectors, content_selectors)