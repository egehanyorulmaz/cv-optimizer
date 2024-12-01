from typing import Protocol, Dict

class PrivacyService(Protocol):
    """
    Interface for privacy-related operations.
    """
    
    def anonymize_text(self, text: str) -> tuple[str, Dict[str, str]]:
        """
        Anonymize text by removing/replacing PII.
        
        :param text: Text to anonymize
        :type text: str
        :return: Tuple of (anonymized text, replacement mapping)
        :rtype: tuple[str, Dict[str, str]]
        """
        raise NotImplementedError

    def restore_text(self, text: str, replacement_map: Dict[str, str]) -> str:
        """
        Restore anonymized text using replacement mapping.
        
        :param text: Anonymized text
        :type text: str
        :param replacement_map: Mapping of placeholders to original values
        :type replacement_map: Dict[str, str]
        :return: Restored text
        :rtype: str
        """
        raise NotImplementedError 