import os
from src.core.ports.secondary.ai_provider import AIProvider
from src.core.ports.secondary.template_service import TemplateService
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.ai_providers.mock_provider import MockAIProvider
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor

def create_ai_provider() -> AIProvider:
    """
    Create the appropriate AI provider based on environment.
    
    :return: An implementation of AIProvider
    :rtype: AIProvider
    """
    config = AIProviderConfig()
    
    # Use MockAIProvider for testing environment
    if os.getenv("TESTING", "false").lower() == "true":
        return MockAIProvider(config=config)
    
    # Use OpenAIProvider for production
    return OpenAIProvider(config=config)

def create_template_service() -> TemplateService:
    """
    Create the template service.
    
    :return: An implementation of TemplateService
    :rtype: TemplateService
    """
    config = TemplateConfig.development()
    return JinjaTemplateService(config=config)

def create_llm_extractor(
    ai_provider: AIProvider = None,
    template_service: TemplateService = None
) -> LLMStructuredExtractor:
    """
    Create the LLM extractor with appropriate dependencies.
    
    :param ai_provider: Optional AI provider, created if not provided
    :type ai_provider: AIProvider, optional
    :param template_service: Optional template service, created if not provided
    :type template_service: TemplateService, optional
    :return: An instance of LLMStructuredExtractor
    :rtype: LLMStructuredExtractor
    """
    ai_provider = ai_provider or create_ai_provider()
    template_service = template_service or create_template_service()
    
    return LLMStructuredExtractor(
        ai_provider=ai_provider,
        template_service=template_service
    )

# Initialize components for easy access
ai_provider: AIProvider = create_ai_provider()
template_service: TemplateService = create_template_service()
llm_extractor: LLMStructuredExtractor = create_llm_extractor(
    ai_provider=ai_provider,
    template_service=template_service
)