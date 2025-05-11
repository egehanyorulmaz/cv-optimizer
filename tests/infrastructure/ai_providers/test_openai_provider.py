import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.ai_providers.exceptions import AIProviderError
from src.core.domain.config import OpenAIConfig

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
        
        chat_completion_mock = AsyncMock(return_value=mock_response)
        mock_async_client.return_value.chat.completions.create = chat_completion_mock

        provider = OpenAIProvider(openai_config)
        result = await provider.complete("Test prompt")
        
        assert result == "Test response"
        
        # Check that the mock was called exactly once
        assert chat_completion_mock.call_count == 1
        
        # Check the arguments passed to the mock
        call_args = chat_completion_mock.call_args[1]  # Get kwargs
        assert call_args['model'] == openai_config.model_name
        assert call_args['temperature'] == openai_config.temperature
        assert call_args['max_tokens'] == openai_config.max_tokens
        assert call_args['messages'] == [{"role": "user", "content": "Test prompt"}]

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
