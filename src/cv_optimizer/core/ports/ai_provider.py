from dataclasses import dataclass
from typing import Protocol, Optional, List


@dataclass
class AIOptions:
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stop_sequences: Optional[List[str]] = None


class AIProvider(Protocol):
    async def complete(self, prompt: str, options: AIOptions) -> str:
        """Generate completion for the given prompt"""
        raise NotImplementedError("AIProvider.complete is not implemented")

    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for the given text"""
        raise NotImplementedError("AIProvider.embed is not implemented")
