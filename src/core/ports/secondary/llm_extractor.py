from typing import Protocol, TypeVar, Type, Dict, Any, Optional
from pydantic import BaseModel
from src.core.ports.secondary.ai_provider import AIOptions

T = TypeVar('T', bound=BaseModel)

class LLMExtractor(Protocol):
    """Port for LLM extraction operations."""
    
    async def generate_structured_output(
        self,
        template_path: str,
        template_vars: Dict[str, Any],
        output_model: Type[T],
        options: Optional[AIOptions] = None
    ) -> T:
        """
        Generate structured output using template variables.
        
        :param template_path: Path to the template file
        :param template_vars: Variables to pass to the template
        :param output_model: The Pydantic model class to parse into
        :param options: Custom AIOptions for this specific call (optional)
        :return: Structured data object of type T
        :raises ValueError: If the output cannot be parsed into the model
        """
        ...
