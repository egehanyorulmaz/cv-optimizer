from src.core.ports.secondary.resume_matcher import ResumeMatcher
from src.core.ports.secondary.ai_provider import AIProvider, AIOptions
from src.core.ports.secondary.template_service import TemplateService
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.resume_match import ResumeMatchResult
from src.infrastructure.utils.llm_utils import clean_llm_json_response
import logging

logger = logging.getLogger(__name__)

class LLMResumeMatcher(ResumeMatcher):
    """
    LLM-based implementation of resume matching service.

    :param ai_provider: Provider for LLM interactions
    :type ai_provider: AIProvider
    :param template_service: Service for rendering prompts
    :type template_service: TemplateService
    :param template_path: Path to the matching prompt template
    :type template_path: str
    """

    def __init__(
        self,
        ai_provider: AIProvider,
        template_service: TemplateService,
        template_path: str
    ):
        self._ai_provider = ai_provider
        self._template_service = template_service
        self._template_path = template_path

    def _parse_response(self, response: str) -> ResumeMatchResult:
        """
        Parse LLM response into ResumeMatchResult model.
        
        :param response: JSON string from LLM
        :type response: str
        :return: Parsed match result
        :rtype: ResumeMatchResult
        :raises ValueError: If response cannot be parsed into the model
        """
        try:
            cleaned_response = clean_llm_json_response(response)
            return ResumeMatchResult.model_validate_json(cleaned_response)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")

    async def match_resume_to_job(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> ResumeMatchResult:
        """
        Match resume to job description using LLM analysis.

        :param resume: The candidate's resume
        :type resume: Resume
        :param job_description: The target job description
        :type job_description: JobDescription
        :return: Detailed matching results and suggestions
        :rtype: ResumeMatchResult
        :raises ValueError: If the LLM response cannot be parsed
        """
        # Prepare the prompt with resume and job description
        prompt = self._template_service.render_prompt(
            self._template_path,
            resume=resume.model_dump_json(indent=4, exclude_none=True),
            job_description=job_description.model_dump_json(indent=4, exclude_none=True)
        )

        options = AIOptions(temperature=0.2)
        response = await self._ai_provider.complete(prompt, options)
        return self._parse_response(response)

if __name__ == "__main__":
    # Example usage
    from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
    from src.infrastructure.template.jinja_template_service import JinjaTemplateService
    from src.core.domain.config import AIProviderConfig, TemplateConfig
    from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor
    from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH
    import asyncio

    async def main():
        # Initialize dependencies
        ai_config = AIProviderConfig()
        template_config = TemplateConfig.development()
        
        # Initialize extractors for both resume and job description
        resume_extractor = LLMStructuredExtractor(
            ai_provider=OpenAIProvider(config=ai_config),
            template_service=JinjaTemplateService(config=template_config),
            output_model=Resume,
            template_path="prompts/parsing/resume_extractor.j2"
        )
        
        job_extractor = LLMStructuredExtractor(
            ai_provider=OpenAIProvider(config=ai_config),
            template_service=JinjaTemplateService(config=template_config),
            output_model=JobDescription,
            template_path="prompts/parsing/job_description_extractor.j2"
        )
        
        # Parse input files
        resume = await resume_extractor.parse(TEST_RESUME_FILE_PATH)
        job_description = await job_extractor.parse(TEST_JOB_DESCRIPTION_FILE_PATH)
        
        # Initialize and use the matcher
        matcher = LLMResumeMatcher(
            ai_provider=OpenAIProvider(config=ai_config),
            template_service=JinjaTemplateService(config=template_config),
            template_path="prompts/matching/resume_matcher.j2"
        )
        
        result = await matcher.match_resume_to_job(resume, job_description)
        print(result.model_dump_json(indent=2))

    asyncio.run(main()) 