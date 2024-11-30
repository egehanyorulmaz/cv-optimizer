from pathlib import Path
from typing import Union, List
import json
import re

from cv_optimizer.core.domain.resume import Resume
from cv_optimizer.core.ports.ai_provider import AIProvider, AIOptions
from cv_optimizer.core.ports.template_service import TemplateService
from cv_optimizer.infrastructure.template_service.jinja_template_service import JinjaTemplateService
from cv_optimizer.infrastructure.ai_providers.openai_provider import OpenAIProvider
from cv_optimizer.core.domain.config import OpenAIConfig, TemplateConfig
from cv_optimizer.infrastructure.parsers.pdf_parser import PDFParser

class LLMResumeParser:
    """
    This class uses LLMs to parse resume documents into structured data.

    :param ai_provider: An implementation of AIProvider for LLM interactions
    :type ai_provider: AIProvider
    :param template_service: An implementation of TemplateService for prompt rendering
    :type template_service: TemplateService
    """
    def __init__(self, ai_provider: AIProvider, template_service: TemplateService):
        self._ai_provider = ai_provider
        self._template_service = template_service
        self._supported_formats = [".pdf"]
        self._parsers = {".pdf": PDFParser()}

    @property
    def supported_formats(self) -> List[str]:
        """List of file extensions this parser supports.

        :return: Supported file extensions including the dot (e.g., ['.txt', '.pdf'])
        :rtype: List[str]
        """
        return self._supported_formats

    async def parse(self, content: Union[Path, bytes, str]) -> Resume:
        """Parse document content into a Resume object using LLM.

        :param content: Either a Path to the resume file or raw bytes content
        :type content: Union[Path, bytes, str]

        :return: Structured resume data object
        :rtype: Resume

        :raises ValueError: If the file format is not supported or content cannot be parsed
        :raises NotImplementedError: If PDF or DOCX parsing is not yet implemented
        :raises TemplateNotFoundError: If the parsing template is not found
        :raises TemplateRenderError: If template rendering fails
        """
        # Convert content to text
        if isinstance(content, Path):
            text = await self._read_file(content)

        elif isinstance(content, bytes) or isinstance(content, str):
            text = content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported content type: {type(content)}")

        # Create prompt using template service
        prompt = self._template_service.render_prompt(
            "prompts/parsing/resume_extractor.j2",
            resume_text=text
        )
        
        # Get structured data from LLM
        options = AIOptions(temperature=0.0)
        response = await self._ai_provider.complete(prompt, options)
        
        return Resume.parse_raw_json(response)

    async def _read_file(self, path: Path) -> str:
        """Read and extract text from various file formats.
        
        Handles different file formats appropriately.
        
        :param path: Path to the file to read
        :type path: Path
        :return: Extracted text content
        :rtype: str
        :raises ValueError: If the file format is not supported
        :raises NotImplementedError: If parsing is not yet implemented
        """
        if path.suffix == '.txt':
            return path.read_text()
        elif path.suffix in self._supported_formats:
            parser = self._parsers[path.suffix]
            return await parser.extract_text(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
