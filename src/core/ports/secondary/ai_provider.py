from dataclasses import dataclass
from typing import Protocol, Optional, List, Union
from abc import ABC, abstractmethod

@dataclass
class AIOptions:
    """Generic AI options that are common across all providers."""
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    stop_sequences: Optional[List[str]] = None

@dataclass
class OpenAIOptions(AIOptions):
    """OpenAI-specific options including model selection."""
    model: Optional[str] = None

@dataclass
class AnthropicOptions(AIOptions):
    """Anthropic-specific options including model selection."""
    model: Optional[str] = None

@dataclass
class GeminiOptions(AIOptions):
    """Gemini-specific options including model selection."""
    model: Optional[str] = None

class AIProvider(Protocol):
    """Base protocol for AI providers."""
    
    async def complete(self, prompt: str, 
                       prompt_specific_options: Optional[AIOptions] = None) -> str:
        """Generate completion for the given prompt"""
        raise NotImplementedError("AIProvider.complete is not implemented")