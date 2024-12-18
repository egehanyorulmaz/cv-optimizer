from typing import Protocol, Union
from abc import abstractmethod
from pathlib import Path
from src.core.domain.resume import Resume


class DocumentParser(Protocol):
    """Interface for parsing different document formats into our Resume domain model"""

    @abstractmethod
    async def parse(self, content: Union[Path, bytes]) -> Resume:
        """Parse document content into a Resume object"""
        pass

    @abstractmethod
    async def reconstruct(self, resume: Resume) -> bytes:
        """Convert Resume object back into document format"""
        pass

    @property
    @abstractmethod
    def supported_formats(self) -> list[str]:
        """List of file extensions this parser supports"""
        pass
