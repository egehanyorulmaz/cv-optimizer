from abc import ABC, abstractmethod


class BasePrivacyFilter(ABC):
    @abstractmethod
    def anonymize_cv(self, text: str) -> str: ...
