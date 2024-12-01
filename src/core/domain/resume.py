from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator
import json


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    links: Optional[List[str]] = None


class Experience(BaseModel):
    title: str
    company: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: List[str]
    achievements: List[str]

    @field_validator('end_date', mode='before')
    @classmethod
    def validate_end_date(cls, v):
        if isinstance(v, str) and not v:
            return None
        return v


class Education(BaseModel):
    degree: str
    institution: str
    graduation_date: datetime
    gpa: Optional[float] = None
    highlights: List[str] = None

    @field_validator('gpa', mode='before')
    @classmethod
    def validate_gpa(cls, v):
        if isinstance(v, str):
            if not v:
                return None
            try:
                return float(v)
            except ValueError:
                return None
        return v


class Resume(BaseModel):
    contact_info: ContactInfo
    summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    publications: Optional[List[str]] = None

    @classmethod
    def parse_raw_json(cls, json_str: str) -> "Resume":
        """
        Parse a JSON string that might include `json prefix and backticks into a Resume object.

        :param json_str: JSON string potentially with `json prefix and backticks
        :type json_str: str
        :return: A validated Resume object
        :rtype: Resume
        :raises ValueError: If the JSON string is invalid or cannot be parsed
        """
        json_str = json_str.strip()
        if json_str.startswith('```json'):
            json_str = json_str[7:]

        if json_str.endswith('```'):
            json_str = json_str[:-3]

        try:
            return cls.model_validate_json(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {str(e)}")
