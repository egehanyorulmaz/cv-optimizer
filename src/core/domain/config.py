from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from src.core.domain.constants import PROJECT_ROOT

@dataclass
class TemplateConfig:
    """Configuration for template service"""
    templates_dir: Path
    cache_enabled: bool = True
    cache_ttl: int = 3600
    default_encoding: str = 'utf-8'
    auto_reload: bool = False

    @classmethod
    def default(cls) -> "TemplateConfig":
        """Create default template configuration"""
        return cls(
            templates_dir=PROJECT_ROOT / "src/infrastructure/template/templates",
            cache_enabled=True,
            cache_ttl=3600,
            default_encoding='utf-8',
            auto_reload=False
        )

    @classmethod
    def development(cls) -> "TemplateConfig":
        """Create development configuration"""
        config = cls.default()
        config.auto_reload = True
        config.cache_enabled = False
        return config

    @classmethod
    def testing(cls, templates_dir: Optional[Path] = None) -> "TemplateConfig":
        """Create testing configuration"""
        return cls(
            templates_dir=templates_dir or Path("tests/fixtures/templates"),
            cache_enabled=False,
            auto_reload=True,
            cache_ttl=0
        )

@dataclass
class AIProviderConfig:
    """Base configuration for AI providers with common settings."""
    temperature: float = 0.1
    max_tokens: Optional[int] = None

@dataclass
class OpenAIConfig(AIProviderConfig):
    """OpenAI-specific configuration."""
    model_name: str = "gpt-4o"
    api_version: str = "2024-02-15"

@dataclass
class AnthropicConfig(AIProviderConfig):
    """Anthropic-specific configuration."""
    model_name: str = "claude-3.5-sonnet-20241022"

@dataclass
class GeminiConfig(AIProviderConfig):
    """Gemini-specific configuration."""
    model_name: str = "gemini-2.5-pro"
