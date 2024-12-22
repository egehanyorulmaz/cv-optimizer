from pydantic import BaseModel
from typing import Literal, List, Optional

class SalaryRange(BaseModel):
    min: float
    max: float
    currency: str

class WorkArrangement(BaseModel):
    work_arrangement_type: Optional[Literal["remote", "hybrid", "in_office"]]
    work_arrangement_description: str

class JobBenefit(BaseModel):
    benefit_type: Literal["health_insurance", "retirement_fund", "stock_options", "bonus", "other"]
    benefit_description: str

class TechStack(BaseModel):
    tech_type: str
    tech_description: str
    required_years_of_experience: Optional[int]
    priority: Literal["required", "nice_to_have"]

class JobRequirement(BaseModel):
    requirement_type: Literal["required", "nice_to_have"]
    required_years_of_experience: Optional[int]
    requirement_description: str

class JobDescription(BaseModel):
    company_name: str
    title: str
    location: str
    description: str
    salary_range: Optional[SalaryRange]
    work_arrangement: Optional[WorkArrangement]
    benefits: List[JobBenefit]
    tech_stack: List[TechStack]
    requirements: List[JobRequirement]