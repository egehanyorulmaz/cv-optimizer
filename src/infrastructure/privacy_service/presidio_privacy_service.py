from src.core.ports.privacy_filter import BasePrivacyFilter
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import re
from typing import Dict, Tuple


class PrivacyService(BasePrivacyFilter):
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.[A-Z|a-z]{2,}\b'

        self.professional_domains = [
            "linkedin",
            "github",
            "gitlab",
            "stackoverflow",
            "behance",
            "dribbble",
            "medium",
            "kaggle",
        ]

    def _clean_and_normalize_email(self, email: str) -> str:
        """Clean and normalize email addresses for consistent processing.
        
        :param email: Raw email string that might contain whitespace or irregular formatting
        :type email: str
        :return: Cleaned and normalized email string
        :rtype: str
        """
        email = re.sub(r'\s+', '', email)  # Remove all whitespace
        email = email.lower()
        email = re.sub(r'(\+[^@]*)@', '@', email)  # Remove any characters after '+' in local part
        return email

    def _process_emails(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Extract and process emails, returning the masked text and email mapping.
        
        :param text: Input text containing email addresses
        :type text: str
        :return: Tuple containing (masked text, dictionary of email mappings)
        :rtype: tuple[str, dict[str, str]]
        """
        email_mapping = {}
        
        def replace_email(match):
            potential_email = match.group(0)
            cleaned_email = self._clean_and_normalize_email(potential_email)
            placeholder = f"<EMAIL_{len(email_mapping)}>"
            email_mapping[placeholder] = cleaned_email
            return placeholder

        masked_text = re.sub(self.email_pattern, replace_email, text)
        return masked_text, email_mapping

    def anonymize_cv(self, text: str) -> str:
        """Anonymize CV text while preserving professional URLs.
        
        :param text: Original CV text
        :type text: str
        :return: Anonymized CV text with preserved professional URLs
        :rtype: str
        """
        # Step 1: Extract and save professional URLs
        professional_urls = self._extract_professional_urls(text)

        # Step 2: Process emails with custom handling
        text, email_mapping = self._process_emails(text)

        # Step 3: Detect remaining PII entities
        results = self.analyzer.analyze(
            text=text,
            language="en",
            entities=["PERSON", "PHONE_NUMBER"],
        )

        # Step 4: Anonymize the CV text
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
            },
        )

        # Step 5: Restore professional URLs
        final_text = self._restore_professional_urls(
            anonymized_result.text, professional_urls
        )

        return final_text

    def _extract_professional_urls(self, text: str) -> Dict[str, str]:
        """Extract professional URLs and domain references to preserve them.
        
        :param text: Input text containing URLs and domain references
        :type text: str
        :return: Dictionary mapping placeholders to original URLs/references
        :rtype: dict[str, str]
        """
        urls = {}
        # Pattern for full URLs
        url_pattern = (
            r"https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)(?:/[^\s]*)?"
        )
        # Pattern for domain references (e.g., github/username or linkedin/in/username)
        domain_ref_pattern = (
            r"(?:(?:^|\s)(?:"
            + "|".join(self.professional_domains)
            + r")\/\S+|(?:^|\s)(?:"
            + "|".join(self.professional_domains)
            + r")\.com\/\S+)"
        )
        # Extract full URLs
        for match in re.finditer(url_pattern, text):
            url = match.group(0)
            if any(domain in url.lower() for domain in self.professional_domains):
                placeholder = f"<PROF_URL_{len(urls)}>"
                urls[placeholder] = url

        # Extract domain references
        for match in re.finditer(domain_ref_pattern, text, re.IGNORECASE):
            ref = match.group(0).strip()
            placeholder = f"<PROF_URL_{len(urls)}>"
            urls[placeholder] = ref

        return urls

    def _restore_professional_urls(self, text: str, urls: Dict[str, str]) -> str:
        """Restore professional URLs after anonymization.
        
        :param text: Anonymized text with URL placeholders
        :type text: str
        :param urls: Dictionary mapping placeholders to original URLs
        :type urls: dict[str, str]
        :return: Text with restored professional URLs
        :rtype: str
        """
        restored_text = text
        for placeholder, url in urls.items():
            restored_text = restored_text.replace("<URL>", url, 1)
        return restored_text
