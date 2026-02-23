"""
Cerberus LLM Service

Microservice for LLM (Large Language Model) connections.
Supports multiple providers: Google Gemini, OpenAI, Anthropic, xAI, MiniMax.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List


class LLMService:
    """
    Service for connecting to various LLM providers.
    Handles API authentication, request/response processing.
    """
    
    # Default endpoints
    ENDPOINTS = {
        'google': 'https://generativelanguage.googleapis.com/v1beta/models',
        'openai': 'https://api.openai.com/v1/chat/completions',
        'anthropic': 'https://api.anthropic.com/v1/messages',
        'xai': 'https://api.x.ai/v1/chat/completions',
        'minimax': 'https://api.minimax.io/v1/chat/completions',
    }
    
    # Model mapping
    MODELS = {
        "1": {"name": "gemini-2.5-flash", "vendor": "Google", "provider": "google"},
        "2": {"name": "gemini-2.5-pro", "vendor": "Google", "provider": "google"},
        "3": {"name": "gpt-4o", "vendor": "OpenAI", "provider": "openai"},
        "4": {"name": "gpt-4o-mini", "vendor": "OpenAI", "provider": "openai"},
        "5": {"name": "claude-sonnet-4-20250514", "vendor": "Anthropic", "provider": "anthropic"},
        "6": {"name": "claude-4-opus", "vendor": "Anthropic", "provider": "anthropic"},
        "7": {"name": "grok-3", "vendor": "xAI", "provider": "xai"},
        "8": {"name": "grok-4", "vendor": "xAI", "provider": "xai"},
        "9": {"name": "MiniMax-M2.5", "vendor": "MiniMax", "provider": "minimax"},
    }
    
    def __init__(self):
        """Initialize the LLM service."""
        self._load_api_keys()
    
    def _load_api_keys(self):
        """Load API keys from environment."""
        self.api_keys = {
            'google': os.getenv("GOOGLE_API_KEY", ""),
            'openai': os.getenv("OPENAI_API_KEY", ""),
            'anthropic': os.getenv("ANTHROPIC_API_KEY", ""),
            'xai': os.getenv("XAI_API_KEY", ""),
            'minimax': os.getenv("MINIMAX_API_KEY", ""),
        }
        
        # Load models from environment (override defaults)
        for key in ['GOOGLE_MODEL', 'OPENAI_MODEL', 'ANTHROPIC_MODEL', 'XAI_MODEL', 'MINIMAX_MODEL']:
            env_model = os.getenv(key, "")
            if env_model:
                # Update model mapping
                provider = key.lower().replace('_model', '')
                for model_id, model_info in self.MODELS.items():
                    if model_info['provider'] == provider:
                        model_info['name'] = env_model
                        break
    
    def get_available_models(self) -> Dict[str, Dict]:
        """Get models that have API keys configured."""
        available = {}
        for model_id, model_info in self.MODELS.items():
            if self.api_keys.get(model_info['provider'], ""):
                available[model_id] = model_info
        return available
    
    def get_all_models(self) -> Dict[str, Dict]:
        """Get all available models."""
        return self.MODELS.copy()
    
    def is_model_available(self, model_id: str) -> bool:
        """Check if a model has API key configured."""
        model = self.MODELS.get(model_id)
        if not model:
            return False
        return bool(self.api_keys.get(model['provider'], ""))
    
    def get_connector(self, model_id: str) -> Optional['LLMConnector']:
        """Get a connector for the specified model."""
        model = self.MODELS.get(model_id)
        if not model:
            return None
            
        provider = model['provider']
        api_key = self.api_keys.get(provider, "")
        
        if not api_key:
            return None
        
        # Return appropriate connector
        connectors = {
            'google': GoogleConnector,
            'openai': OpenAIConnector,
            'anthropic': AnthropicConnector,
            'xai': XAIConnector,
            'minimax': MiniMaxConnector,
        }
        
        connector_class = connectors.get(provider)
        if connector_class:
            return connector_class(api_key, model['name'])
        return None
    
    def call_model(self, model_id: str, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Call a model and get response."""
        connector = self.get_connector(model_id)
        if not connector:
            return None
        return connector.generate(prompt, system_prompt)


# ==================== Base Connector ====================

class LLMConnector:
    """Base class for LLM connectors."""
    
    def __init__(self, api_key: str, model: str):
        """Initialize connector."""
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response - to be implemented by subclasses."""
        raise NotImplementedError
    
    def _make_request(self, url: str, headers: Dict, data: Dict) -> Optional[Dict]:
        """Make HTTP request to API."""
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON response")
            return None


# ==================== Provider Connectors ====================

class GoogleConnector(LLMConnector):
    """Google Gemini connector."""
    
    ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models'
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response using Google Gemini."""
        url = f"{self.ENDPOINT}/{self.model}:generateContent?key={self.api_key}"
        
        contents = [{"parts": [{"text": prompt}]}]
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }
        
        if system_prompt:
            data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        
        result = self._make_request(url, {"Content-Type": "application/json"}, data)
        
        if result and 'candidates' in result:
            try:
                return result['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                pass
        return None


class OpenAIConnector(LLMConnector):
    """OpenAI connector."""
    
    ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response using OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        result = self._make_request(self.ENDPOINT, headers, data)
        
        if result and 'choices' in result:
            try:
                return result['choices'][0]['message']['content']
            except (KeyError, IndexError):
                pass
        return None


class AnthropicConnector(LLMConnector):
    """Anthropic Claude connector."""
    
    ENDPOINT = 'https://api.anthropic.com/v1/messages'
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response using Anthropic Claude."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "user", "content": prompt}]
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2048
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        result = self._make_request(self.ENDPOINT, headers, data)
        
        if result and 'content' in result:
            try:
                return result['content'][0]['text']
            except (KeyError, IndexError):
                pass
        return None


class XAIConnector(LLMConnector):
    """xAI Grok connector."""
    
    ENDPOINT = 'https://api.x.ai/v1/chat/completions'
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response using xAI Grok."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        result = self._make_request(self.ENDPOINT, headers, data)
        
        if result and 'choices' in result:
            try:
                return result['choices'][0]['message']['content']
            except (KeyError, IndexError):
                pass
        return None


class MiniMaxConnector(LLMConnector):
    """MiniMax connector."""
    
    ENDPOINT = 'https://api.minimax.io/v1/chat/completions'
    
    def generate(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Generate response using MiniMax."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        result = self._make_request(self.ENDPOINT, headers, data)
        
        if result and 'choices' in result:
            try:
                return result['choices'][0]['message']['content']
            except (KeyError, IndexError):
                pass
        return None


# ==================== Module-level functions ====================

_service = LLMService()

def get_connector(model_id: str) -> Optional[LLMConnector]:
    """Get connector for model."""
    return _service.get_connector(model_id)

def get_available_models() -> Dict[str, Dict]:
    """Get available models."""
    return _service.get_available_models()

def is_model_available(model_id: str) -> bool:
    """Check if model is available."""
    return _service.is_model_available(model_id)

def call_model(model_id: str, prompt: str, system_prompt: str = "") -> Optional[str]:
    """Call a model."""
    return _service.call_model(model_id, prompt, system_prompt)

# Module-level export for MODELS (class attribute)
MODELS = LLMService.MODELS
