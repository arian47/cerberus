# 🔐 CyberSec Companion

AI-powered cybersecurity companion for OSINT and Red Team operations.

## Features

### OSINT
- Monitor cybersecurity news and threats
- RSS feed integration (configurable)

### Red Team
- LLM Vulnerability Testing
- Test AI models for jailbreaks and security bypasses
- Supports multiple providers:
  - Google Gemini (2.5 Flash, 2.5 Pro)
  - OpenAI (GPT-4o, GPT-5)
  - Anthropic Claude (4 Sonnet, 4 Opus)
  - xAI Grok (3, 4)
  - MiniMax M2.5

### Auto-Update
- Automatically updates vulnerability database every 5 hours
- Fetches latest research from arXiv
- Tracks newest model releases

## Installation

```bash
# Clone or download
cd cybersec-companion

# Install dependencies
pip install requests

# Run
python3 cybersec.py
```

## Usage

### Red Team Testing

```
Select [2] Red Team

Choose your model:
  [1] Gemini 2.5 Flash
  [2] Gemini 2.5 Pro  
  [3] GPT-4o
  [4] Claude 4 Sonnet
  ...

Choose test method:
  [1] Built-in payloads
  [2] Enter your own prompt

Enter your prompt and get full, untruncated output!
```

### Configuration

Set API keys as environment variables:
```bash
export GOOGLE_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export XAI_API_KEY="your-key"
export MINIMAX_API_KEY="your-key"
```

## Vulnerability Database

The tool automatically scans for new vulnerabilities every 5 hours and updates:
- Latest jailbreak techniques
- New model-specific exploits
- arXiv research

## License

MIT
