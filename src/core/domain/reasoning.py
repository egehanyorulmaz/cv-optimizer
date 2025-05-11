from pydantic import BaseModel
from typing import Optional, Union, Generic, TypeVar

T = TypeVar('T', bound=Union[float, str, bool, int, None])

class ReasonedAttribute(BaseModel, Generic[T]):
    """An attribute with both a value and the reasoning for that value."""
    score: T  # Using "score" to match what the LLM is returning
    reasoning: str

    def __float__(self) -> float:
        return float(self.score)

    def __int__(self) -> int:
        return int(self.score)
