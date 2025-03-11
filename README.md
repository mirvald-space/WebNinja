# WebNinja 🥷

My personal project for automating web research using modern language models. This agent can independently search for information on the internet, analyze it, and provide structured reports.

## 🚀 What can WebNinja do?

- 🌐 Automatically collects information from web pages
- 🧠 Uses Grok or GPT-4 for content analysis
- 🛡️ Bypasses bot protection systems
- 🎭 Emulates human behavior
- 📊 Creates structured reports
- ⚡ Works fast and efficiently

## 🛠️ Technologies

- Python 3.11+
- Playwright for browser automation
- Grok API (X.AI) / OpenAI API
- Requests for API handling
- Python-dotenv for configuration

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/web-ninja.git
cd web-ninja

# Create virtual environment
python -m venv .myenv
source .myenv/bin/activate  # for Linux/Mac
# or .myenv\Scripts\activate  # for Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## ⚙️ Configuration

1. Create `.env` file in the project root
2. Add your API keys:
```env
GROK_API_KEY=xai-your-key
# or
OPENAI_API_KEY=sk-your-key
```

## 🎮 How to Use

### Simple Example
```python
from src.agent import WebAgent

# Create agent
agent = WebAgent(
    api_key="your-api-key",
    provider="grok",  # or "openai"
    headless=False    # False to see the browser
)

# Start research
result = agent.research(
    topic="polish card in 2025",
    depth=3,           # Check 3 sources
    max_time=180       # Maximum 3 minutes
)

print(result)
```

### Advanced Features

- Customize search depth with `depth` parameter
- Choose between Grok and OpenAI
- Set time limits for research
- Supports both headless and visual modes
- Smart content analysis and summarization
- Automatic data structuring


## 🤝 Contributing

Got ideas to make WebNinja better? Create an issue or send a pull request. I'm always excited to discuss new features!

## 📄 License

MIT - do whatever you want, just mention the author 😉

## 👨‍💻 Author

Developed for personal needs but decided to share with the community. Feel free to reach out with any questions!