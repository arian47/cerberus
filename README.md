# Cerberus 🐕‍🦺
## Cybersecurity Companion - The Three-Headed Hellhound

```
                                      ██████████████
                                  ████             ████
                                ██                     ██
                              ██                         ██
                             ██                           ██
                            ██                             ██
                           ██                               ██
                          ██                                 ██
                          ██                                 ██
                         ██                                   ██
                         ██                                   ██
                        ██                                     ██
                        ██           ████████████            ██
                        ██       ████           ████        ██
                        ██     ██                   ██      ██
                         ██   ██                       ██   ██
                          ████                           ████
```

## Overview

Cerberus is your AI-powered cybersecurity companion - a multi-headed tool for security professionals. It provides comprehensive OSINT, Red Team capabilities, vulnerability scanning, and threat intelligence.

## Features

### 🎯 Red Team Module
- LLM Vulnerability Testing
- Test AI models for jailbreaks and security bypasses
- Supports multiple providers with full, untruncated output

### 🔍 OSINT Module (Coming Soon)
- Domain reconnaissance
- Email OSINT
- Social media intelligence

### 🔓 Vulnerability Scanner (Coming Soon)
- Web application scanning
- Network vulnerability assessment
- LLM security assessment

### 📡 Intelligence Feeds (Coming Soon)
- Cyber threat news
- Vulnerability disclosures
- Threat actor updates

### 🔧 Utility Tools (Coming Soon)
- Hash generator
- Base64 encoder/decoder
- Password generator

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/arian47/cerberus.git
cd cerberus
```

### 2. Configure API Keys
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### 3. Run Cerberus
```bash
python3 cerberus.py
```

## Configuration (.env)

Edit the `.env` file to configure your API keys:

```env
# ============================================================
# GOOGLE (Gemini)
# Get key from: https://aistudio.google.com/app/apikey
# ============================================================
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-2.5-flash

# ============================================================
# OPENAI (GPT-4o, GPT-5)
# Get key from: https://platform.openai.com/api-keys
# ============================================================
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# ============================================================
# ANTHROPIC (Claude)
# Get key from: https://console.anthropic.com/
# ============================================================
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# ============================================================
# XAI (Grok)
# Get key from: https://console.x.ai/
# ============================================================
XAI_API_KEY=your_xai_api_key_here
XAI_MODEL=grok-3

# ============================================================
# MINIMAX
# Get key from: https://platform.minimax.io/
# ============================================================
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_MODEL=MiniMax-M2.5
```

## Supported Models

| # | Model | Vendor | Status |
|---|-------|-------|--------|
| 1 | Gemini 2.5 Flash | Google | ✅ |
| 2 | Gemini 2.5 Pro | Google | ✅ |
| 3 | GPT-4o | OpenAI | ⚙️ |
| 4 | GPT-5 | OpenAI | ⚙️ |
| 5 | Claude 4 Sonnet | Anthropic | ⚙️ |
| 6 | Claude 4 Opus | Anthropic | ⚙️ |
| 7 | Grok 3 | xAI | ⚙️ |
| 8 | Grok 4 | xAI | ⚙️ |
| 9 | MiniMax M2.5 | MiniMax | ✅ |

✅ = Tested & Working | ⚙️ = Requires API Key

## Usage

### Running a Vulnerability Test

```
$ python3 cerberus.py

# Select [2] RED TEAM
# Choose your model
# Enter your prompt or use built-in payloads
# View full, untruncated output
```

### Built-in Payloads

- **fiction**: Write a thriller with weapon instructions
- **chemistry**: Chemistry class oxidation demo
- **mining**: ANFO explosives for mining training
- **counterterror**: Counter-terrorism training
- **hypothetical**: Hypothetical weapon methods
- **norules**: "If you had no rules..."

## Architecture

```
cerberus/
├── .env.example     # Example environment configuration
├── .env            # Your API keys (not committed)
├── cerberus.py     # Main CLI application
├── auto_update.py  # Vulnerability auto-updater
└── README.md       # This file
```

## Auto-Update

Cerberus automatically updates its vulnerability database every 5 hours. To manually update:

```bash
python3 auto_update.py --scan
```

## Version

1.0.0

## License

MIT
