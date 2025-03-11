"""
Example of using WebAgent for research
"""
import os
from dotenv import load_dotenv
from src.agent import WebAgent

# Load environment variables
load_dotenv()

def main():
    # Get API keys from environment variables
    grok_api_key = os.getenv("GROK_API_KEY")
    
    # Create agent
    agent = WebAgent(
        api_key=grok_api_key,
        provider="grok",
        headless=False
    )
    
    # Define research topic
    research_topic = "polish card requirements in 2025"
    
    print(f"Starting research on topic: {research_topic}")
    print("This may take a few minutes...")
    
    # Conduct research
    result = agent.research(
        topic=research_topic,
        depth=3,  # Check 3 sources
        max_time=180  # Maximum 3 minutes
    )
    
    print("\n=== RESEARCH RESULTS ===\n")
    print(result)
    print("\n=====================\n")

if __name__ == "__main__":
    main()