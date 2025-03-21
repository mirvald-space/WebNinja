"""
Web Agent Main Class
"""
import os
import time
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv

from src.llm_providers import get_provider, LLMProvider
from src.web_tools import WebBrowser

# Load environment variables
load_dotenv()

# Default values
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "grok")
DEFAULT_NEWS_SITE = os.getenv("DEFAULT_NEWS_SITE", "https://www.reuters.com/technology")

# Reliable sources for AI and technology research
RESEARCH_SOURCES = [
    "https://www.wired.com/tag/artificial-intelligence",
    "https://www.technologyreview.com/topic/artificial-intelligence",
    "https://venturebeat.com/category/ai",
    "https://www.reuters.com/technology",
    "https://techcrunch.com/category/artificial-intelligence"
]

class WebAgent:
    """A core class of agent for collecting and analyzing web information"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = DEFAULT_PROVIDER, 
                 headless: bool = True, user_agent: Optional[str] = None):
        """
        Web Agent Initialization
        
        Args:
            api_key: API key for the language model
            provider: LLM provider name ('grok' or 'openai')
            headless: Run the browser in the background
            user_agent: Custom User-Agent
        """
        self.api_key = api_key
        self.provider_name = provider
        self.headless = headless
        self.user_agent = user_agent
        
        # Initialize LLM provider
        self.llm_provider = get_provider(provider, api_key)
    
    def run(self, task: str) -> str:
        """
        Performs a task by gathering information from the internet
        
        Args:
            task: Text description of the task
            
        Returns:
            str: The result of the task execution
        """
        # Open browser
        with WebBrowser(headless=self.headless, user_agent=self.user_agent) as browser:
            # Visit news site or determine strategy based on task
            if "news" in task.lower():
                content = browser.visit_news_site(DEFAULT_NEWS_SITE)
            else:
                # Search for information on Google
                results = browser.google_search(task)
                if results:
                    browser.navigate(results[0])
                    content = browser.extract_content()
                else:
                    content = {"error": "No relevant results found"}
            
            # Form system prompt
            system_prompt = f"""
            You're an expert at analyzing web content. Analyze the information provided and give a concise, 
            informative answer to the problem: "{task}".
            """
            
            # Form user prompt with content
            user_prompt = f"Task: {task}\n\nData from page {content.get('url', 'unknown URL')}:\n"
            
            if 'error' in content:
                user_prompt += f"Error collecting data: {content['error']}"
            else:
                # Add headers
                if 'content' in content and 'headers' in content['content']:
                    user_prompt += "Headers:\n"
                    headers = content['content']['headers'][:10]  # Limit quantity
                    user_prompt += "\n".join([f"- {header}" for header in headers])
                    user_prompt += "\n\n"
                
                # Add paragraphs
                if 'content' in content and 'paragraphs' in content['content']:
                    user_prompt += "Content:\n"
                    paragraphs = content['content']['paragraphs'][:15]  # Limit quantity
                    user_prompt += "\n\n".join(paragraphs)
            
            # Generate response through LLM
            response = self.llm_provider.generate_response(system_prompt, user_prompt)
            return response
    
    def research(self, topic: str, depth: int = 3, max_time: int = 300) -> str:
        """
        Conducts research on a given topic by visiting multiple sources
        
        Args:
            topic: Research topic
            depth: Number of sources to check
            max_time: Maximum execution time in seconds
            
        Returns:
            str: Research results
        """
        start_time = time.time()
        all_content = []
        
        with WebBrowser(headless=self.headless, user_agent=self.user_agent) as browser:
            # Use predefined sources instead of search
            print(f"Using {depth} trusted sources for research...")
            sources = RESEARCH_SOURCES[:depth]
            
            for i, url in enumerate(sources, 1):
                print(f"Processing source {i}/{len(sources)}: {url}")
                # Check time limit
                if time.time() - start_time > max_time:
                    print("Time limit exceeded")
                    all_content.append({
                        "url": "Time limit exceeded",
                        "content": "Research was interrupted due to time limit"
                    })
                    break
                
                # Navigate to source
                print(f"Navigating to {url}")
                if browser.navigate(url):
                    # Extract content
                    print("Extracting content...")
                    content = browser.extract_content()
                    all_content.append({
                        "url": url,
                        "content": content
                    })
                else:
                    print(f"Failed to navigate to {url}")
            
            print("Preparing research report...")
            # Form system prompt for research
            system_prompt = f"""
            You are an experienced researcher and technology analyst. Analyze the provided information about "{topic}".
            Create a structured report in Ukrainian language including:
            1. Key facts and data about AI in design and product development
            2. Expert opinions and predictions for 2025
            3. Current trends and potential impact
            4. Conclusions and recommendations
            
            Base your analysis on the available information, even if it's not directly about the specific question.
            Extrapolate current trends and developments to make informed predictions about 2025.
            """
            
            # Form user prompt with data from all sources
            user_prompt = f"Research topic: {topic}\n\n"
            
            for i, source in enumerate(all_content):
                user_prompt += f"--- SOURCE {i+1}: {source.get('url', 'URL not specified')} ---\n"
                
                if isinstance(source['content'], dict) and 'content' in source['content']:
                    # Add headers
                    if 'headers' in source['content']['content']:
                        headers = source['content']['content']['headers'][:8]
                        user_prompt += "Main headers:\n"
                        user_prompt += "\n".join([f"- {h}" for h in headers])
                        user_prompt += "\n\n"
                    
                    # Add paragraphs
                    if 'paragraphs' in source['content']['content']:
                        paragraphs = source['content']['content']['paragraphs'][:10]
                        user_prompt += "Key excerpts:\n"
                        user_prompt += "\n\n".join(paragraphs[:500])  # Limit size
                        user_prompt += "\n\n"
                else:
                    user_prompt += "Failed to extract structured content\n\n"
                
                user_prompt += "---\n\n"
            
            print("Generating final report...")
            # Generate final report
            response = self.llm_provider.generate_response(system_prompt, user_prompt)
            return response