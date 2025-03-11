"""
Example of using WebAgent for news gathering
"""
import os
from dotenv import load_dotenv
from src.agent import WebAgent

# Load environment variables
load_dotenv()

def main():
    # Get the keys from the environment variables
    grok_api_key = os.getenv("GROK_API_KEY")
    
    # Create an agent
    agent = WebAgent(
        api_key=grok_api_key,
        provider="grok",
        headless=True  # True for hidden mode, False for browser display
    )
    
    # Requesting the latest technology news
    result = agent.run("latest technology news")
    
    print("\n=== AGENT RESULT ===\n")
    print(result)
    print("\n=======================\n")

if __name__ == "__main__":
    main()