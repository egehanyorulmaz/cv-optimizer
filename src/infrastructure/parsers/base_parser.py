from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class BaseDocumentParser(ABC):
    """
    Abstract base class for document parsers.
    
    This class defines the interface for basic document parsing operations.
    Implementations should handle specific file formats and provide appropriate
    text extraction logic.
    
    :ivar supported_formats: List of file extensions this parser supports
    :type supported_formats: list[str]
    """

    def __init__(self):
        """Initialize the document parser."""
        self._supported_formats = []

    @property
    def supported_formats(self) -> list[str]:
        """
        Get list of supported file formats.
        
        :return: List of supported file extensions (e.g., ['.pdf', '.docx'])
        :rtype: list[str]
        """
        return self._supported_formats

    @abstractmethod
    async def extract_text(self, content: Union[Path, bytes]) -> str:
        """
        Extract text content from a document.
        
        :param content: Either a Path to the document file or raw bytes content
        :type content: Union[Path, bytes]
        :return: Extracted text content
        :rtype: str
        :raises ValueError: If the content cannot be parsed
        :raises NotImplementedError: If parsing is not implemented for this format
        """
        pass

    def supports_format(self, file_extension: str) -> bool:
        """
        Check if this parser supports the given file format.
        
        :param file_extension: File extension to check (e.g., '.pdf')
        :type file_extension: str
        :return: True if format is supported, False otherwise
        :rtype: bool
        """
        return file_extension.lower() in [fmt.lower() for fmt in self.supported_formats]

    async def _read_file(self, path: Path) -> bytes:
        """
        Read file content into bytes.
        
        :param path: Path to the file to read
        :type path: Path
        :return: File content as bytes
        :rtype: bytes
        :raises FileNotFoundError: If the file doesn't exist
        :raises IOError: If the file cannot be read
        """
        try:
            return await path.read_bytes()
        except Exception as e:
            raise IOError(f"Failed to read file {path}: {str(e)}") from e 