from typing import List, Optional, TypedDict, Dict

from src.core.domain.company_search import CompanyInfo
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.resume_match import (
    SkillMatch, 
    ExperienceAlignment, 
    ProjectMatch, 
    KeywordFrequency, 
    PriorityImprovement
)


class AgentState(TypedDict):
    ''' 
    Represents the shared state that flows through the LangGraph.
    Keys are dynamically added and updated by different agent nodes.
    '''
    resume_path: str
    job_description_path: str
    
    # Initial inputs
    resume: Resume
    job_description: JobDescription
    
    # Enriched data
    resume_company_info: Optional[Dict[str, CompanyInfo]]
    job_description_company_info: Optional[Dict[str, CompanyInfo]]
    
    # Analysis results (populated by agents)
    skill_matches: Optional[List[SkillMatch]]
    experience_alignment: Optional[ExperienceAlignment]
    project_matches: Optional[List[ProjectMatch]]
    education_alignment: Optional[float]
    keyword_analysis: Optional[List[KeywordFrequency]]
    critical_missing_keywords: Optional[List[str]]
    
    # Synthesis results
    top_strengths: Optional[List[str]]
    critical_gaps: Optional[List[str]]
    overall_match_percentage: Optional[float]
    interview_probability: Optional[float]
    
    # Suggestions
    priority_improvements: Optional[List[PriorityImprovement]]
    general_suggestions: Optional[List[str]]

    # Potential intermediate data (optional)
    # e.g., raw extracted skills, error messages
    error_messages: Optional[List[str]] 