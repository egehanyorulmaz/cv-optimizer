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
        Initialize OpenAI provider with API key.
        
        :param config: OpenAI configuration
        :type config: OpenAIConfig
        :raises AIProviderError: If API key is not provided or found in environment
        """
        load_dotenv()
        
        self.config = config
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise AIProviderError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            
        try:
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
            client = openai.OpenAI(api_key=self.api_key)
            client.models.list()
        except Exception as e:
            raise AIProviderError(f"Failed to initialize OpenAI client: {str(e)}")

    async def complete(self, prompt: str) -> str:
        """
        Generate completion using OpenAI API.
        
        :param prompt: Input prompt
        :type prompt: str
        :return: Generated completion text
        :rtype: str
        :raises AIProviderError: If API call fails.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
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
