from cv_optimizer.core.ports.privacy_filter import BasePrivacyFilter
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import importlib.resources as pkg_resources
from cv_optimizer import data
import PyPDF2
import re
from typing import Dict


class PrivacyService(BasePrivacyFilter):
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        self.professional_domains = [
            'linkedin.com',
            'github.com',
            'gitlab.com',
            'stackoverflow.com',
            'behance.net',
            'dribbble.com',
            'medium.com',
            'dev.to',
            'kaggle.com'
        ]
    
    def anonymize_cv(self, text: str) -> str:
        # Step 1: Extract and save professional URLs
        professional_urls = self._extract_professional_urls(text)
        
        # Step 2: Detect PII entities
        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=[
                "PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", 
                "LOCATION", "URL"
            ]
        )

        # Step 3: Anonymize the CV text
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
                "URL": OperatorConfig("replace", {"new_value": "<URL>"}),
                "LOCATION": OperatorConfig("replace", {"new_value": "<LOCATION>"}),
                "DEFAULT": OperatorConfig("replace", {"new_value": "<MASKED>"})
            }
        )

        # Step 4: Restore professional URLs
        final_text = self._restore_professional_urls(
            anonymized_result.text, 
            professional_urls
        )
        
        return final_text

    def _extract_professional_urls(self, text: str) -> Dict[str, str]:
        """Extract professional URLs to preserve them"""
        urls = {}
        url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)(?:/[^\s]*)?'
        
        for match in re.finditer(url_pattern, text):
            url = match.group(0)
            if any(domain in url.lower() for domain in self.professional_domains):
                placeholder = f"<PROF_URL_{len(urls)}>"
                urls[placeholder] = url
        
        return urls

    def _restore_professional_urls(self, text: str, urls: Dict[str, str]) -> str:
        """Restore professional URLs after anonymization"""
        restored_text = text
        for placeholder, url in urls.items():
            restored_text = restored_text.replace("<URL>", url, 1)
        return restored_text