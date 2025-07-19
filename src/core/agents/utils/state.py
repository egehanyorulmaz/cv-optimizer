from typing import List, Optional, TypedDict, Dict

from src.core.domain.company_search import CompanyInfo
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.resume_match import (
    SkillMatch, 
    ExperienceAlignment, 
    ProjectMatch, 
    KeywordFrequency, 
    PriorityImprovement,
    CompanyAlignment
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
    experience_alignment: Optional[ExperienceAlignment]
    company_alignment: Optional[CompanyAlignment]
    
    # Synthesis results
    overall_match_percentage: Optional[float]
    company_alignment_feedback: Optional[str]
    
    # TODO
    # interview_probability: Optional[float]
    # top_strengths: Optional[List[str]]
    # critical_gaps: Optional[List[str]]
    # skill_matches: Optional[List[SkillMatch]]
    # project_matches: Optional[List[ProjectMatch]]
    # education_alignment: Optional[float]
    # keyword_analysis: Optional[List[KeywordFrequency]]
    # section_analysis: Optional[List[SectionAnalysis]]
    # priority_improvements: Optional[List[PriorityImprovement]]
    # general_suggestions: Optional[List[str]]
    # critical_missing_keywords: Optional[List[str]]

    # Suggestions
    priority_improvements: Optional[List[PriorityImprovement]]
    general_suggestions: Optional[List[str]]

    # Potential intermediate data (optional)
    # e.g., raw extracted skills, error messages
    error_messages: Optional[List[str]] 