import pytest
from pathlib import Path

from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.resume import Resume
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor
from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH
from src.core.domain.job_description import JobDescription

@pytest.mark.asyncio
async def test_llm_extractor_resume_parse():
    """
    Test the LLMStructuredExtractor's parse functionality with a test resume file.

    :raises AssertionError: If the parsing fails or returns unexpected results
    """
    ai_config = AIProviderConfig(model_name="gpt-4o-mini")
    template_config = TemplateConfig.development()
    extractor = LLMStructuredExtractor(
        ai_provider=OpenAIProvider(config=ai_config),
        template_service=JinjaTemplateService(config=template_config),
        output_model=Resume,
        template_path="prompts/parsing/resume_extractor.j2"
    )

    result = await extractor.parse(TEST_RESUME_FILE_PATH)

    # Basic validation that we got some data
    assert isinstance(result, Resume)
    assert result.contact_info.name is not None  
    assert result.experiences is not None
    assert len(result.experiences) > 0


@pytest.mark.asyncio
async def test_llm_extractor_job_description_parse():
    """
    Test the LLMStructuredExtractor's parse functionality with a test resume file.

    :raises AssertionError: If the parsing fails or returns unexpected results
    """
    ai_config = AIProviderConfig(model_name="gpt-4o-mini")
    template_config = TemplateConfig.development()
    extractor = LLMStructuredExtractor(
        ai_provider=OpenAIProvider(config=ai_config),
        template_service=JinjaTemplateService(config=template_config),
        output_model=JobDescription,
        template_path="prompts/parsing/job_description_extractor.j2"
    )

    result = await extractor.parse(TEST_JOB_DESCRIPTION_FILE_PATH)

    # Basic validation that we got some data
    assert isinstance(result, JobDescription)
    assert result.title is not None  
    assert result.description is not None
    assert len(result.description) > 0