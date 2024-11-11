from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ContactInfo:
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None


@dataclass
class Experience:
    title: str
    company: str
    start_date: datetime
    end_date: Optional[datetime]
    description: List[str]
    achievements: List[str]


@dataclass
class Education:
    degree: str
    institution: str
    graduation_date: datetime
    gpa: Optional[float] = None
    highlights: List[str] = None


@dataclass
class Resume:
    contact_info: ContactInfo
    summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: Optional[List[str]] = None

    def to_dict(self) -> dict:
        # serialization
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Resume":
        # deserialization
        pass
