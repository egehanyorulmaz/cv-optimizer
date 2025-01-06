"""
Shared resources management for the Streamlit application.
"""

import logging
from typing import Optional
from src.core.ports.primary.resource_provider import ResourceProvider
from src.core.domain.exceptions.resource_exceptions import (
    ResourceNotInitializedError,
    ResourceInitializationError
)
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor
from src.infrastructure.parsers.pdf_parser import PDFParser
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription

logger = logging.getLogger(__name__)

class AIProviderResource(ResourceProvider[OpenAIProvider]):
    """Manages the AI provider resource."""
    
    def __init__(self):
        self._provider: Optional[OpenAIProvider] = None
    
    def initialize(self) -> None:
        """
        Initialize the AI provider.
        
        :raises ResourceInitializationError: If initialization fails
        """
        try:
            config = AIProviderConfig()
            self._provider = OpenAIProvider(config=config)
            logger.info("AI provider initialized successfully")
        except Exception as e:
            raise ResourceInitializationError(f"Failed to initialize AI provider: {str(e)}")
    
    def get_resource(self) -> OpenAIProvider:
        """
        Get the AI provider instance.
        
        :return: Configured AI provider
        :rtype: OpenAIProvider
        :raises ResourceNotInitializedError: If provider is not initialized
        """
        if self._provider is None:
            raise ResourceNotInitializedError("AI provider not initialized")
        return self._provider

class TemplateServiceResource(ResourceProvider[JinjaTemplateService]):
    """Manages the template service resource."""
    
    def __init__(self):
        self._service: Optional[JinjaTemplateService] = None

    def initialize(self) -> None:
        """
        Initialize the template service.
        
        :raises ResourceInitializationError: If initialization fails
        """
        try:
            config = TemplateConfig.development()
            self._service = JinjaTemplateService(config=config)
            logger.info("Template service initialized successfully")
        except Exception as e:
            raise ResourceInitializationError(f"Failed to initialize template service: {str(e)}")
    
    def get_resource(self) -> JinjaTemplateService:
        """
        Get the template service instance.
        
        :return: Configured template service
        :rtype: JinjaTemplateService
        :raises ResourceNotInitializedError: If service is not initialized
        """
        if self._service is None:
            raise ResourceNotInitializedError("Template service not initialized")
        return self._service

class ResumeParserResource(ResourceProvider[LLMStructuredExtractor]):
    """Manages the resume parser resource."""
    
    def __init__(self):
        self._parser: Optional[LLMStructuredExtractor] = None

    def initialize(self) -> None:
        """
        Initialize the resume parser.
        
        :raises ResourceInitializationError: If initialization fails
        """
        try:
            ai_config = AIProviderConfig()
            template_config = TemplateConfig.development()
            
            self._parser = LLMStructuredExtractor(
                ai_provider=OpenAIProvider(config=ai_config),
                template_service=JinjaTemplateService(config=template_config),
                output_model=Resume,
                template_path="prompts/parsing/resume_extractor.j2",
                document_parsers={".pdf": PDFParser()}
            )
            logger.info("Resume parser initialized successfully")
        except Exception as e:
            raise ResourceInitializationError(f"Failed to initialize resume parser: {str(e)}")
    
    def get_resource(self) -> LLMStructuredExtractor:
        """
        Get the resume parser instance.
        
        :return: Configured resume parser
        :rtype: LLMStructuredExtractor
        :raises ResourceNotInitializedError: If parser is not initialized
        """
        if self._parser is None:
            raise ResourceNotInitializedError("Resume parser not initialized")
        return self._parser

class JobParserResource(ResourceProvider[LLMStructuredExtractor]):
    """Manages the job description parser resource."""
    
    def __init__(self):
        self._parser: Optional[LLMStructuredExtractor] = None

    def initialize(self) -> None:
        """
        Initialize the job description parser.
        
        :raises ResourceInitializationError: If initialization fails
        """
        try:
            ai_config = AIProviderConfig()
            template_config = TemplateConfig.development()
            
            self._parser = LLMStructuredExtractor(
                ai_provider=OpenAIProvider(config=ai_config),
                template_service=JinjaTemplateService(config=template_config),
                output_model=JobDescription,
                template_path="prompts/parsing/job_description_extractor.j2",
                document_parsers={".pdf": PDFParser()}
            )
            logger.info("Job description parser initialized successfully")
        except Exception as e:
            raise ResourceInitializationError(f"Failed to initialize job description parser: {str(e)}")
    
    def get_resource(self) -> LLMStructuredExtractor:
        """
        Get the job description parser instance.
        
        :return: Configured job description parser
        :rtype: LLMStructuredExtractor
        :raises ResourceNotInitializedError: If parser is not initialized
        """
        if self._parser is None:
            raise ResourceNotInitializedError("Job description parser not initialized")
        return self._parser

class SharedResources:
    """
    Central management of shared application resources.
    """
    
    _instance: Optional['SharedResources'] = None
    
    def __init__(self):
        """Initialize resource managers."""
        if SharedResources._instance is not None:
            raise RuntimeError("Use get_instance() to access SharedResources")
        
        self.ai_provider = AIProviderResource()
        self.template_service = TemplateServiceResource()
        self.resume_parser = ResumeParserResource()
        self.job_parser = JobParserResource()
        self._initialize_resources()
    
    def _initialize_resources(self) -> None:
        """
        Initialize all managed resources.
        
        :raises ResourceInitializationError: If any resource fails to initialize
        """
        try:
            self.ai_provider.initialize()
            self.template_service.initialize()
            self.resume_parser.initialize()
            self.job_parser.initialize()
        except Exception as e:
            logger.error(f"Failed to initialize resources: {str(e)}")
            raise ResourceInitializationError(str(e))
    
    @classmethod
    def get_instance(cls) -> 'SharedResources':
        """
        Get the singleton instance of SharedResources.
        
        :return: SharedResources instance
        :rtype: SharedResources
        """
        if cls._instance is None:
            cls._instance = SharedResources()
        return cls._instance 