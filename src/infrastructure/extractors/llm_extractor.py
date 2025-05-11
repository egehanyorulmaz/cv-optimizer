from pathlib import Path
from typing import Union, List, TypeVar, Type, Generic, Optional
from pydantic import BaseModel
import json
from typing import Dict, Any

from src.core.ports.secondary.ai_provider import AIProvider, AIOptions
from src.core.ports.secondary.template_service import TemplateService
from src.infrastructure.parsers.base_parser import BaseDocumentParser
from src.infrastructure.parsers.pdf_parser import PDFParser

T = TypeVar('T', bound=BaseModel)

class LLMStructuredExtractor:
    """
    Generic extractor that uses LLMs to parse text into structured Pydantic models.
    
    :param ai_provider: An implementation of AIProvider for LLM interactions
    :type ai_provider: AIProvider
    :param template_service: An implementation of TemplateService for prompt rendering
    :type template_service: TemplateService
    :param output_model: The Pydantic model class to parse into
    :type output_model: Type[T]
    :param template_path: Path to the template file for extraction
    :type template_path: str
    """
    def __init__(
        self, 
        ai_provider: AIProvider, 
        template_service: TemplateService,
        document_parsers: Optional[dict[str, BaseDocumentParser]] = None
    ):
        self._ai_provider = ai_provider
        self._template_service = template_service
        self._parsers = document_parsers or {".pdf": PDFParser()}

        self._supported_formats = list(self._parsers.keys()) if self._parsers else []

    @property
    def supported_formats(self) -> List[str]:
        """
        List of file extensions this parser supports.

        :return: Supported file extensions including the dot (e.g., ['.txt', '.pdf'])
        :rtype: List[str]
        """
        return self._supported_formats

    async def parse_document(self, content: Union[Path, bytes, str],
                           output_model: Type[T],
                           template_path: str) -> T:
        """
        Parse a document into a structured Pydantic object using LLM.

        :param content: Either a Path to the file, raw bytes, or string content
        :type content: Union[Path, bytes, str]
        :param output_model: The Pydantic model class to parse into
        :type output_model: Type[T]
        :param template_path: Path to the template file for document extraction
        :type template_path: str
        :return: Structured data object of type T
        :rtype: T
        :raises ValueError: If the content format is not supported or cannot be parsed
        """
        # Convert content to text
        text = await self._get_text_content(content)

        # Create prompt using template service
        prompt = self._template_service.render_prompt(
            template_path,
            input_text=text
        )
        
        # Get structured data from LLM
        options = AIOptions(temperature=0.0)
        response = await self._ai_provider.complete(prompt, options)
        
        return self._parse_response(response, output_model)

    async def generate_structured_output(self,
                                        template_path: str,
                                        template_vars: Dict[str, Any],
                                        output_model: Type[T],
                                        options: Optional[AIOptions] = None) -> T:
        """
        Generate structured output using template variables without document parsing.
        Useful for agent interactions where data is already in memory.

        :param template_path: Path to the template file
        :type template_path: str
        :param template_vars: Variables to pass to the template
        :type template_vars: Dict[str, Any]
        :param output_model: The Pydantic model class to parse into
        :type output_model: Type[T]
        :param options: Custom AIOptions for this specific call (optional)
        :type options: AIOptions, optional
        :return: Structured data object of type T
        :rtype: T
        :raises ValueError: If the output cannot be parsed into the model
        """
        # Create prompt using template service
        prompt = self._template_service.render_prompt(
            template_path,
            **template_vars
        )
        
        # Get structured data from LLM
        ai_options = options or AIOptions(temperature=0.0)
        response = await self._ai_provider.complete(prompt, ai_options)
        
        return self._parse_response(response, output_model)
    
    async def _get_text_content(self, content: Union[Path, bytes, str]) -> str:
        """
        Extract text content from various input types.
        
        :param content: Input content in various formats
        :type content: Union[Path, bytes, str]
        :return: Extracted text content
        :rtype: str
        :raises ValueError: If content type is not supported
        """
        if isinstance(content, str):
            return content
        elif isinstance(content, Path):
            if content.suffix == '.txt':
                return content.read_text()
            elif content.suffix in self._supported_formats:
                parser = self._parsers[content.suffix]
                return await parser.extract_text(content)
            else:
                raise ValueError(f"Unsupported file format: {content.suffix}")
        elif isinstance(content, bytes):
            # For PDF content in bytes, use the PDF parser
            if '.pdf' in self._supported_formats:
                parser = self._parsers['.pdf']
                return await parser.extract_text(content)
            # For other types, try UTF-8 decode
            return content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported content type: {type(content)}")

    def _parse_response(self, response: str, output_model: Type[T]) -> T:
        """
        Parse LLM response into the target Pydantic model.
        
        :param response: JSON string from LLM
        :type response: str
        :return: Parsed model instance
        :rtype: T
        :raises ValueError: If response cannot be parsed into the model
        """
        try:
            # Clean up potential markdown formatting
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]

            return output_model.model_validate_json(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")

if __name__ == "__main__":
    from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
    from src.core.domain.config import AIProviderConfig, TemplateConfig
    from src.infrastructure.template.jinja_template_service import JinjaTemplateService
    from src.core.domain.resume import Resume
    from src.core.domain.job_description import JobDescription
    import asyncio
    from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH

    async def main():
        ai_config = AIProviderConfig()
        template_config = TemplateConfig.development()
        extractor = LLMStructuredExtractor(
            ai_provider=OpenAIProvider(config=ai_config), 
            template_service=JinjaTemplateService(config=template_config)
        )
        parsed_data = await extractor.parse_document(
            content=TEST_RESUME_FILE_PATH,
            output_model=Resume,
            template_path="prompts/parsing/resume_extractor.j2"
        )
        print(parsed_data)

    asyncio.run(main())
