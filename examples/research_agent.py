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
    
    print("Checking API key...")
    if not grok_api_key:
        print("Error: GROK_API_KEY not found in environment variables")
        return
    
    print("Creating WebAgent...")
    # Create agent
    agent = WebAgent(
        api_key=grok_api_key,
        provider="grok",
        headless=True
    )
    
    # Define research topic
    research_topic = "Чи замінить AI продукт дизайнерів 2025 року?"
    
    print(f"Starting research on topic: {research_topic}")
    print("This may take a few minutes...")
    
    try:
        # Conduct research
        print("Starting research process...")
        result = agent.research(
            topic=research_topic,
            depth=3,  # Check 3 sources
            max_time=180  # Maximum 3 minutes
        )
        
        print("\n=== RESEARCH RESULTS ===\n")
        print(result)
        print("\n=====================\n")
    except Exception as e:
        print(f"Error during research: {str(e)}")

if __name__ == "__main__":
    main()