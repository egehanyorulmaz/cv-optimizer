from src.core.ports.secondary.ai_provider import AIProvider
from src.core.ports.secondary.template_service import TemplateService
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor

# Initialize the AI provider
ai_provider: AIProvider = OpenAIProvider(config=AIProviderConfig())

# Initialize the template service
template_service: TemplateService = JinjaTemplateService(config=TemplateConfig.development())

# Initialize the LLM extractor
llm_extractor: LLMStructuredExtractor = LLMStructuredExtractor(
    ai_provider=ai_provider,
    template_service=template_service
)