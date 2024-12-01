from dataclasses import dataclass
from typing import Protocol


@dataclass
class PIIReplacement:
    original: str
    replacement: str


class PrivacyFilter(Protocol):
    def anonymize_cv(self, text: str) -> str: ...
