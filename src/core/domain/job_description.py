from pydantic import BaseModel
from typing import Literal, List

class JobBenefit(BaseModel):
    benefit_type: Literal["health_insurance", "retirement_fund", "stock_options", "bonus", "other"]
    benefit_description: str

class TechStack(BaseModel):
    tech_type: str
    tech_description: str
    priority: Literal["required", "nice_to_have"]

class JobRequirement(BaseModel):
    requirement_type: Literal["required", "nice_to_have"]
    requirement_description: str

class JobDescription(BaseModel):
    company_name: str
    title: str
    location: str
    description: str
    benefits: List[JobBenefit]
    tech_stack: List[TechStack]
    requirements: List[JobRequirement]