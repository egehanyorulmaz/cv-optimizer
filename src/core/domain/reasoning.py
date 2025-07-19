from pydantic import BaseModel
from typing import Optional, Union, Generic, TypeVar

T = TypeVar('T', bound=Union[float, str, bool, int, None])

class ReasonedAttribute(BaseModel, Generic[T]):
    """An attribute with both a value and the reasoning for that value."""
    score: T
    reasoning: str