from typing import List
import os
from dotenv import load_dotenv
import openai
from cv_optimizer.core.ports.ai_provider import AIProvider, AIOptions
from cv_optimizer.infrastructure.ai_providers.exceptions import AIProviderError
from cv_optimizer.core.domain.config import OpenAIConfig


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
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
            client = openai.OpenAI(api_key=self.api_key)
            client.models.list()
        except Exception as e:
            raise AIProviderError(f"Failed to initialize OpenAI client: {str(e)}")
            
        self.global_options = AIOptions(
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        self.model_name = config.model_name

    async def complete(self, prompt: str, prompt_specific_options: AIOptions = None) -> str:
        """
        Generate completion using OpenAI API.
        
        :param prompt: Input prompt
        :type prompt: str
        :param prompt_specific_options: Options specific to this prompt call, overrides global options if provided
        :type prompt_specific_options: AIOptions, optional
        :return: Generated completion text
        :rtype: str
        :raises AIProviderError: If API call fails.
        """
        # Use prompt-specific options if provided, otherwise use global options
        options_to_use = prompt_specific_options if prompt_specific_options is not None else self.global_options
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                temperature=options_to_use.temperature,
                max_tokens=options_to_use.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise AIProviderError(f"OpenAI API error: {str(e)}")

    async def embed(self, text: str) -> List[float]:
        """
        Generate embeddings using OpenAI API.
        
        :param text: Input text
        :type text: str
        :return: Text embedding vector
        :rtype: List[float]
        :raises AIProviderError: If API call fails or text is too long
        """
        if len(text) > 8000:
            raise AIProviderError("Text too long for embedding")
            
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise AIProviderError(f"OpenAI embedding error: {str(e)}")
