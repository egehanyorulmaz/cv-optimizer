import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.resume import Resume
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor
from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH
from src.core.domain.job_description import JobDescription

@pytest.fixture
def mock_openai_setup():
    """
    Setup OpenAI mocks for testing with different responses for Resume and JobDescription.
    
    :return: Mocked OpenAI client
    :rtype: MagicMock
    """
    # Define expected prompts for different templates
    template_prompts = {
        "job_description": "Extract key information from a job description",  # Partial match from job_description_extractor.j2
        "resume": "Extract the following information from this resume"  # Partial match from resume_extractor.j2
    }
    
    with patch('openai.AsyncOpenAI') as mock_async_client, \
         patch('openai.OpenAI') as mock_client:
        # Mock the models.list() call in initialization
        mock_client.return_value.models.list = MagicMock()
        
        # Create a mock function that returns different responses based on the prompt
        async def mock_completion(*args, **kwargs):
            messages = kwargs.get('messages', [])
            prompt = messages[0]['content'] if messages else ''
            
            # Check if prompt contains job description extraction instructions
            if template_prompts["job_description"] in prompt:
                mock_response = MagicMock()
                mock_response.choices = [MagicMock()]
                mock_response.choices[0].message.content = """
                {
                    "title": "Machine Learning Engineer",
                    "company_name": "Salesforce",
                    "location": "Remote",
                    "description": "Design and implement ML and generative AI powered features",
                    "benefits": [
                        {
                            "benefit_type": "health_insurance",
                            "benefit_description": "Comprehensive health coverage"
                        }
                    ],
                    "tech_stack": [
                        {
                            "tech_type": "Python",
                            "tech_description": "Primary programming language",
                            "priority": "required"
                        }
                    ],
                    "requirements": [
                        {
                            "requirement_type": "required",
                            "requirement_description": "8+ years experience with machine learning"
                        }
                    ]
                }
                """
            else:
                # Resume response (default case)
                mock_response = MagicMock()
                mock_response.choices = [MagicMock()]
                mock_response.choices[0].message.content = """
                {
                    "contact_info": {
                        "name": "John Doe",
                        "email": "john@example.com",
                        "phone": "+1234567890",
                        "location": "New York, NY",
                        "links": ["https://linkedin.com/in/johndoe"]
                    },
                    "summary": "Experienced software engineer with focus on machine learning",
                    "experiences": [
                        {
                            "company": "Tech Corp",
                            "title": "Senior Engineer",
                            "start_date": "2020-01-01",
                            "end_date": "2023-12-31",
                            "description": ["Led machine learning projects", "Managed team of 5 engineers"],
                            "achievements": ["Improved model accuracy by 25%"]
                        }
                    ],
                    "education": [
                        {
                            "institution": "MIT",
                            "degree": "MS Computer Science",
                            "graduation_date": "2019-05-15",
                            "gpa": 3.8,
                            "highlights": ["Machine Learning specialization"]
                        }
                    ],
                    "skills": ["Python", "Java", "Machine Learning"],
                    "certifications": ["AWS Solutions Architect"],
                    "achievements": ["Best Paper Award 2022"],
                    "publications": ["Machine Learning in Practice, 2023"]
                }
                """
            return mock_response

        mock_async_client.return_value.chat.completions.create = AsyncMock(
            side_effect=mock_completion
        )
        
        yield mock_async_client

@pytest.mark.asyncio
async def test_llm_extractor_resume_parse(mock_openai_setup):
    """
    Test the LLMStructuredExtractor's parse functionality with a test resume file.

    :param mock_openai_setup: Fixture that provides mocked OpenAI client
    :type mock_openai_setup: MagicMock
    :raises AssertionError: If the parsing fails or returns unexpected results
    """
    ai_config = AIProviderConfig()
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