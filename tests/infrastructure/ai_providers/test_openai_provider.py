import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from cv_optimizer.infrastructure.ai_providers.openai_provider import OpenAIProvider
from cv_optimizer.infrastructure.ai_providers.exceptions import AIProviderError
from cv_optimizer.core.domain.config import OpenAIConfig

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Setup environment variables before each test"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        yield

@pytest.fixture
def openai_config():
    return OpenAIConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,
    )

@pytest.mark.asyncio
async def test_openai_provider_completion(openai_config):
    """Test OpenAI completion functionality."""
    with patch('openai.AsyncOpenAI') as mock_async_client, \
         patch('openai.OpenAI') as mock_client:
        # Mock the models.list() call in initialization
        mock_client.return_value.models.list = MagicMock()
        
        # Mock the chat completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_async_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        provider = OpenAIProvider(openai_config)
        result = await provider.complete("Test prompt")
        
        assert result == "Test response"
        mock_async_client.return_value.chat.completions.create.assert_called_once_with(
            model=openai_config.model_name,
            temperature=openai_config.temperature,
            max_tokens=openai_config.max_tokens,
            messages=[{"role": "user", "content": "Test prompt"}]
        )

@pytest.mark.asyncio
async def test_openai_provider_embedding(openai_config):
    """Test OpenAI embedding functionality."""
    with patch('openai.AsyncOpenAI') as mock_async_client, \
         patch('openai.OpenAI') as mock_client:
        # Mock the models.list() call in initialization
        mock_client.return_value.models.list = MagicMock()
        
        # Mock embedding response
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        
        mock_async_client.return_value.embeddings.create = AsyncMock(
            return_value=mock_response
        )

        provider = OpenAIProvider(openai_config)
        result = await provider.embed("Test text")
        
        assert result == [0.1, 0.2, 0.3]
        mock_async_client.return_value.embeddings.create.assert_called_once_with(
            model="text-embedding-ada-002",
            input="Test text"
        )

@pytest.mark.asyncio
async def test_openai_provider_error_handling(openai_config):
    """Test error handling in OpenAI provider."""
    with patch('openai.AsyncOpenAI') as mock_async_client, \
         patch('openai.OpenAI') as mock_client:
        # Mock the models.list() call in initialization
        mock_client.return_value.models.list = MagicMock()
        
        mock_async_client.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("API Error")
        )

        provider = OpenAIProvider(openai_config)
        
        with pytest.raises(AIProviderError) as exc_info:
            await provider.complete("Test prompt")
        
        assert "OpenAI API error" in str(exc_info.value)
