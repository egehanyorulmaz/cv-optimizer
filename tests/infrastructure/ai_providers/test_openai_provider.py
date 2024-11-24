import pytest
import os
from cv_optimizer.core.ports.ai_provider import AIOptions
from cv_optimizer.infrastructure.ai_providers.openai_provider import OpenAIProvider
from cv_optimizer.infrastructure.ai_providers.exceptions import AIProviderError


@pytest.mark.asyncio
async def test_openai_provider_completion():
    """Test OpenAI completion functionality."""
    provider = OpenAIProvider()
    options = AIOptions(
        temperature=0.7,
        max_tokens=100,
        stop_sequences=None
    )
    
    result = await provider.complete(
        "Write a one-sentence summary of what AI is:",
        options
    )
    
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_openai_provider_embedding():
    """Test OpenAI embedding functionality."""
    provider = OpenAIProvider()
    test_text = "This is a test sentence."
    
    result = await provider.embed(test_text)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(x, float) for x in result)


@pytest.mark.asyncio
async def test_openai_provider_error_handling():
    """Test error handling in OpenAI provider."""
    provider = OpenAIProvider()
    options = AIOptions(
        temperature=0.7,
        max_tokens=100,
        stop_sequences=None
    )
    
    # Test with empty prompt
    with pytest.raises(AIProviderError, match="Empty prompt provided"):
        await provider.complete("   ", options)
    
    # Test with extremely long text for embedding
    with pytest.raises(AIProviderError, match="Text too long for embedding"):
        await provider.embed("a" * 10000)