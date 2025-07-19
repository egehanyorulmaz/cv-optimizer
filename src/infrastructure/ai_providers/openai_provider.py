from typing import Optional
import os
from dotenv import load_dotenv
from langsmith import traceable
import openai
from src.core.ports.secondary.ai_provider import AIProvider, AIOptions, OpenAIOptions
from src.infrastructure.ai_providers.exceptions import AIProviderError
from src.core.domain.config import OpenAIConfig
from langsmith.wrappers import wrap_openai

class OpenAIProvider(AIProvider):
    """OpenAI implementation of the AI provider interface."""
    def __init__(self, config: OpenAIConfig):
        """
        Initialize OpenAI provider with API key and global options.
        
        :param config: Configuration for OpenAI provider containing global options
        :type config: OpenAIConfig
        :raises AIProviderError: If API key is not provided or found in environment
        """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise AIProviderError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            
        try:
            self.client = wrap_openai(openai.AsyncOpenAI(api_key=self.api_key))
            client = openai.OpenAI(api_key=self.api_key)
            client.models.list()
        except Exception as e:
            raise AIProviderError(f"Failed to initialize OpenAI client: {str(e)}")
            
        self.global_options = OpenAIOptions(
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            model=config.model_name
        )
        self.default_model = config.model_name

    @traceable(run_type="llm")
    async def complete(self, prompt: str, 
                       prompt_specific_options: Optional[AIOptions] = None) -> str:
        """
        Generate completion using OpenAI API.
        
        :param prompt: Input prompt
        :type prompt: str
        :param prompt_specific_options: Options specific to this prompt call, overrides global options if provided
        :type prompt_specific_options: AIOptions
        :return: Generated completion text
        :rtype: str
        :raises AIProviderError: If API call fails.
        """
        # Use prompt-specific options if provided, otherwise use global options
        options_to_use = prompt_specific_options if prompt_specific_options else self.global_options
        
        # Determine which model to use
        model_to_use = self.default_model
        if isinstance(options_to_use, OpenAIOptions) and options_to_use.model:
            model_to_use = options_to_use.model
        
        try:
            response = await self.client.chat.completions.create(
                model=model_to_use,
                temperature=options_to_use.temperature,
                max_tokens=options_to_use.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            completion = response.choices[0].message.content
            return completion if completion is not None else ""
        except Exception as e:
            raise AIProviderError(f"OpenAI API error: {str(e)}")