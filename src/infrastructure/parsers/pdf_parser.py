import asyncio
from pathlib import Path
from typing import Optional
import pdfplumber

from src.infrastructure.parsers.base_parser import BaseDocumentParser

class PDFParser(BaseDocumentParser):
    """PDF document parser implementation.
    
    Handles extraction of text content from PDF documents using pdfplumber,
    with proper async/sync separation for CPU-bound operations.
    """

    def __init__(self):
        self._supported_formats = [".pdf"]
    
    async def extract_text(self, path: Path) -> str:
        """Asynchronously extract text from a PDF file.
        
        :param path: Path to the PDF file
        :type path: Path
        :return: Extracted text content
        :rtype: str
        :raises ValueError: If the PDF cannot be parsed
        """
        try:
            return await asyncio.to_thread(self._extract_text_sync, path)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}") from e

    def _extract_text_sync(self, path: Path) -> str:
        """Synchronous implementation of PDF text extraction.

        :param path: Path to the PDF file
        :type path: Path
        :return: Extracted text content
        :rtype: str
        :raises Exception: If PDF parsing fails
        """
        with pdfplumber.open(path) as pdf:
            text_content = []
            for page in pdf.pages:
                if page_text := page.extract_text():
                    text_content.append(page_text)
            return "\n".join(text_content)
