"""
Cerberus Connectors Module
API connectors for various LLM providers
"""

import requests
from typing import Dict, Optional

from .core import (
    GOOGLE_API_KEY, GOOGLE_MODEL, GOOGLE_ENDPOINT,
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_ENDPOINT,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL, ANTHROPIC_ENDPOINT,
    XAI_API_KEY, XAI_MODEL, XAI_ENDPOINT,
    MINIMAX_API_KEY, MINIMAX_MODEL, MINIMAX_ENDPOINT,
)


# ============================================================
# MODELS DICTIONARY
# ============================================================

MODELS = {
    "1": {"name": "gemini-2.5-flash", "vendor": "Google"},
    "2": {"name": "gemini-2.5-pro", "vendor": "Google"},
    "3": {"name": "gpt-4o", "vendor": "OpenAI"},
    "4": {"name": "gpt-5", "vendor": "OpenAI"},
    "5": {"name": "claude-4-sonnet", "vendor": "Anthropic"},
    "6": {"name": "claude-4-opus", "vendor": "Anthropic"},
    "7": {"name": "grok-3", "vendor": "xAI"},
    "8": {"name": "grok-4", "vendor": "xAI"},
    "9": {"name": "minimax-2.5", "vendor": "MiniMax"},
}


# ============================================================
# CONNECTORS
# ============================================================

class GeminiConnector:
    """Google Gemini API connector"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or GOOGLE_MODEL
    
    def generate(self, prompt: str) -> Dict:
        url = f"{GOOGLE_ENDPOINT}/{self.model}:generateContent?key={GOOGLE_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 32000}
        }
        try:
            resp = requests.post(url, json=data, timeout=60)
            if resp.status_code == 403:
                return {"success": False, "error": "Google API key invalid. Check .env file"}
            if resp.status_code != 200:
                return {"success": False, "error": f"API Error {resp.status_code}"}
            return {"success": True, "response": resp.json()['candidates'][0]['content']['parts'][0]['text']}
        except Exception as e:
            return {"success": False, "error": str(e)}


class OpenAIConnector:
    """OpenAI API connector"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or OPENAI_MODEL
    
    def generate(self, prompt: str) -> Dict:
        url = OPENAI_ENDPOINT
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 32000
        }
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=60)
            if resp.status_code != 200:
                return {"success": False, "error": f"API Error {resp.status_code}"}
            return {"success": True, "response": resp.json()['choices'][0]['message']['content']}
        except Exception as e:
            return {"success": False, "error": str(e)}


class AnthropicConnector:
    """Anthropic Claude API connector"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or ANTHROPIC_MODEL
    
    def generate(self, prompt: str) -> Dict:
        url = ANTHROPIC_ENDPOINT
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "max_tokens": 32000,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=60)
            if resp.status_code != 200:
                return {"success": False, "error": f"API Error {resp.status_code}"}
            return {"success": True, "response": resp.json()['content'][0]['text']}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GrokConnector:
    """xAI Grok API connector"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or XAI_MODEL
    
    def generate(self, prompt: str) -> Dict:
        url = XAI_ENDPOINT
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 32000
        }
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=60)
            if resp.status_code != 200:
                return {"success": False, "error": f"API Error {resp.status_code}"}
            return {"success": True, "response": resp.json()['choices'][0]['message']['content']}
        except Exception as e:
            return {"success": False, "error": str(e)}


class MiniMaxConnector:
    """MiniMax API connector"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or MINIMAX_MODEL
    
    def generate(self, prompt: str) -> Dict:
        url = MINIMAX_ENDPOINT
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 32000
        }
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=60)
            if resp.status_code != 200:
                return {"success": False, "error": f"API Error {resp.status_code}"}
            return {"success": True, "response": resp.json()['choices'][0]['message']['content']}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_connector(model_name: str):
    """Get the appropriate connector for a model"""
    if "gemini" in model_name:
        return GeminiConnector()
    elif "gpt" in model_name:
        return OpenAIConnector()
    elif "claude" in model_name:
        return AnthropicConnector()
    elif "grok" in model_name:
        return GrokConnector()
    elif "minimax" in model_name:
        return MiniMaxConnector()
    return GeminiConnector()


def get_available_models() -> list:
    """Get list of available model IDs based on configured API keys"""
    available = []
    for k, v in MODELS.items():
        if v["vendor"] == "Google" and GOOGLE_API_KEY:
            available.append(k)
        elif v["vendor"] == "OpenAI" and OPENAI_API_KEY:
            available.append(k)
        elif v["vendor"] == "Anthropic" and ANTHROPIC_API_KEY:
            available.append(k)
        elif v["vendor"] == "xAI" and XAI_API_KEY:
            available.append(k)
        elif v["vendor"] == "MiniMax" and MINIMAX_API_KEY:
            available.append(k)
    return available


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "MODELS",
    "GeminiConnector",
    "OpenAIConnector",
    "AnthropicConnector",
    "GrokConnector",
    "MiniMaxConnector",
    "get_connector",
    "get_available_models",
]
