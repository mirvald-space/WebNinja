"""
Module for working with various Language Model (LLM) providers
"""
import json
import requests
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a response based on system and user prompts"""
        pass


def get_provider(provider_name: str = "grok", api_key: Optional[str] = None) -> LLMProvider:
    """
    Creates and returns an LLM provider instance based on name
    
    Args:
        provider_name: Provider name ('grok' or 'openai')
        api_key: API key for the provider (optional)
    
    Returns:
        LLMProvider: Instance of the corresponding provider
    """
    if provider_name.lower() == "grok":
        return GrokProvider(api_key)
    elif provider_name.lower() == "openai":
        return OpenAIProvider(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


class GrokProvider(LLMProvider):
    """Integration with Grok API (X.AI)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError("Grok API key is required. Provide it in parameters or in .env file")
        
        self.api_url = "https://api.x.ai/v1/chat/completions"
        
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a response using Grok API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(data),
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return f"Response processing error: {str(e)}"


class OpenAIProvider(LLMProvider):
    """Integration with OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Provide it in parameters or in .env file")
        
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a response using OpenAI API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(data),
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"