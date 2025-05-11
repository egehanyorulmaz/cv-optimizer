from typing import List, Optional, Dict, Any
import os
import json
from src.core.ports.secondary.ai_provider import AIProvider, AIOptions
from src.core.domain.config import AIProviderConfig
from langsmith import traceable

class MockAIProvider(AIProvider):
    """Mock implementation of the AI provider interface for testing."""
    
    def __init__(self, config: AIProviderConfig):
        """
        Initialize Mock AI provider with configuration.
        
        :param config: Configuration for AI provider containing global options
        :type config: AIProviderConfig
        """
        self.global_options = AIOptions(
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        self.model_name = config.model_name
        self.responses = {}  # Can be populated with predefined responses for testing
        self.default_structured_responses = {
            # Default response for experience alignment
            "experience_analyzer": json.dumps({
                "years_overlap": {"score": 3.0, "reasoning": "The candidate has 3 years of relevant experience"},
                "role_similarity": {"score": 0.8, "reasoning": "The roles align well"},
                "domain_relevance": {"score": 0.7, "reasoning": "The domain experience is relevant"},
                "tech_stack_overlap": {"score": 0.85, "reasoning": "Good tech stack overlap"},
                "leadership_alignment": {"score": 0.75, "reasoning": "Candidate has relevant leadership experience"}
            })
        }

    @traceable(run_type="llm")
    async def complete(self, prompt: str, prompt_specific_options: AIOptions = None) -> str:
        """
        Mock completion that returns predefined responses or a default response.
        
        :param prompt: Input prompt
        :type prompt: str
        :param prompt_specific_options: Options specific to this prompt call
        :type prompt_specific_options: AIOptions, optional
        :return: Generated completion text
        :rtype: str
        """
        # Return exact match if found
        if prompt in self.responses:
            return self.responses[prompt]
        
        # Check for partial matches in template paths
        for key, template_type in [
            ("experience_analyzer", "prompts/agents/experience_analyzer.j2"),
            # Add other template types as needed
        ]:
            if template_type in prompt and key in self.default_structured_responses:
                return self.default_structured_responses[key]
        
        # Return a default mock response
        return '{"score": 0.75, "reasoning": "This is a mock response for testing."}'

    @traceable(run_type="llm")
    async def embed(self, text: str) -> List[float]:
        """
        Generate mock embeddings for the given text.
        
        :param text: Text to embed
        :type text: str
        :return: Mock embedding vector (simplified for testing)
        :rtype: List[float]
        """
        # Return a simple mock embedding
        return [0.1, 0.2, 0.3, 0.4, 0.5]

    def register_response(self, prompt: str, response: str):
        """
        Register a specific response for a given prompt.
        Useful for controlling test behavior.
        
        :param prompt: The prompt to match
        :type prompt: str
        :param response: The response to return
        :type response: str
        """
        self.responses[prompt] = response
    
    def register_structured_response(self, template_type: str, response_data: Dict[str, Any]):
        """
        Register a structured response for a specific template type.
        
        :param template_type: The type of template (e.g., "experience_analyzer")
        :type template_type: str
        :param response_data: The response data to return (will be JSON-encoded)
        :type response_data: Dict[str, Any]
        """
        self.default_structured_responses[template_type] = json.dumps(response_data) 