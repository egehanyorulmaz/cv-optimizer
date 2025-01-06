"""File validation utilities for the Streamlit application."""

from typing import Union
import magic
import logging

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain'
}

def validate_file(file_content: Union[bytes, str], file_type: str) -> bool:
    """
    Validate file content and type.
    
    :param file_content: Content of the file
    :type file_content: Union[bytes, str]
    :param file_type: Expected file type extension
    :type file_type: str
    :return: True if file is valid, False otherwise
    :rtype: bool
    """
    try:
        if not file_content or not file_type:
            return False
        
        # Special handling for text files
        if file_type.lower() == 'txt':
            try:
                # Try to decode as text
                if isinstance(file_content, bytes):
                    file_content.decode('utf-8')
                return True
            except UnicodeDecodeError:
                logger.warning("File content is not valid UTF-8 text")
                return False
        
        # For other file types, use MIME type validation
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(file_content)
        
        # Check if file type matches expected MIME type
        expected_mime_type = ALLOWED_MIME_TYPES.get(file_type.lower())
        if not expected_mime_type:
            logger.warning(f"Unsupported file type: {file_type}")
            return False
        
        if file_mime_type != expected_mime_type:
            logger.warning(f"MIME type mismatch. Expected: {expected_mime_type}, Got: {file_mime_type}")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        return False 