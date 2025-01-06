import asyncio
from pathlib import Path
from typing import Union
import io
import pdfplumber

from src.infrastructure.parsers.base_parser import BaseDocumentParser

class PDFParser(BaseDocumentParser):
    """PDF document parser implementation.
    
    Handles extraction of text content from PDF documents using pdfplumber,
    with proper async/sync separation for CPU-bound operations.
    """

    def __init__(self):
        self._supported_formats = [".pdf"]
    
    async def extract_text(self, content: Union[Path, bytes]) -> str:
        """Asynchronously extract text from PDF content.
        
        :param content: Either a Path to the PDF file or raw bytes content
        :type content: Union[Path, bytes]
        :return: Extracted text content
        :rtype: str
        :raises ValueError: If the PDF cannot be parsed
        """
        try:
            return await asyncio.to_thread(self._extract_text_sync, content)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}") from e

    def _extract_text_sync(self, content: Union[Path, bytes]) -> str:
        """Synchronous implementation of PDF text extraction.

        :param content: Either a Path to the PDF file or raw bytes content
        :type content: Union[Path, bytes]
        :return: Extracted text content
        :rtype: str
        :raises Exception: If PDF parsing fails
        """
        # Convert bytes to BytesIO if needed
        pdf_content = io.BytesIO(content) if isinstance(content, bytes) else content
        
        with pdfplumber.open(pdf_content) as pdf:
            text_content = []
            for page in pdf.pages:
                if page_text := page.extract_text():
                    text_content.append(page_text)
            return "\n".join(text_content)

if __name__ == "__main__":
    import asyncio
    from src.core.domain.constants import TEST_RESUME_FILE_PATH
    
    async def main():
        parser = PDFParser()
        text = await parser.extract_text(Path(TEST_RESUME_FILE_PATH))
        print(text)
        
    asyncio.run(main())