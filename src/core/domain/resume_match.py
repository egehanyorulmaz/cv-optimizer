from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Literal
from enum import Enum
from src.core.domain.reasoning import ReasonedAttribute

class JobCategory(str, Enum):
    """
    Enumeration of job categories to better classify skill requirements.
    
    :cvar TECHNICAL: Technical or hard skills like programming languages
    :cvar DOMAIN: Domain-specific knowledge like finance or healthcare
    :cvar SOFT: Soft skills like communication or leadership
    :cvar TOOL: Knowledge of specific tools or platforms
    :cvar METHODOLOGY: Methodologies like Agile or Six Sigma
    """
    TECHNICAL = "technical"
    DOMAIN = "domain"
    SOFT = "soft"
    TOOL = "tool"
    METHODOLOGY = "methodology"


class SkillLevel(str, Enum):
    """
    Enumeration representing skill proficiency levels.
    
    :cvar BEGINNER: Basic understanding of concepts
    :cvar INTERMEDIATE: Working knowledge and some practical experience
    :cvar ADVANCED: Deep understanding and significant experience
    :cvar EXPERT: Mastery of the skill, capable of teaching others
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class CompanyAlignment(BaseModel):
    """
    Represents the alignment between the candidate's past companies and the target company.

    :ivar size_alignment: Alignment of the candidate's past companies' size with the target company's size
    :ivar industry_alignment: Alignment of the candidate's past companies' industry with the target company's industry
    """
    size_alignment: ReasonedAttribute[float]
    industry_alignment: ReasonedAttribute[float]


class SkillRelationship(BaseModel):
    """
    Represents relationships between skills and potential learning paths.
    
    :ivar related_skills: List of related skills to the primary skill
    :ivar transferability_score: How transferable knowledge is between skills (0-1)
    """
    related_skills: List[str]
    transferability_score: float = Field(ge=0, le=1)
    learning_curve_estimate: str
    learning_resources: Optional[List[str]] = None


class SkillMatch(BaseModel):
    """
    Detailed analysis of a skill match between resume and job description.
    
    :ivar skill: Name of the skill
    :ivar present_in_resume: Whether the skill is found in the resume
    :ivar importance: Importance of the skill for the job (1-5)
    :ivar priority: Whether the skill is required or nice-to-have
    :ivar category: Category of the skill (technical, domain, soft, etc.)
    :ivar skill_level_required: Required proficiency level
    :ivar skill_level_inferred: Inferred level from resume
    :ivar skill_relationships: Related skills and learning paths
    :ivar suggested_improvement: Specific suggestion for improvement
    :ivar keyword_variations: Alternative terms for the skill
    """
    skill: str
    present_in_resume: bool
    importance: int = Field(ge=1, le=5)
    priority: Literal["required", "nice_to_have"] = "required"
    category: JobCategory
    skill_level_required: Optional[SkillLevel] = None
    skill_level_inferred: Optional[SkillLevel] = None
    skill_relationships: Optional[SkillRelationship] = None
    suggested_improvement: Optional[str] = None
    keyword_variations: Optional[List[str]] = None
    
    @field_validator('importance')
    def validate_importance(cls, v, values):
        """
        Validates that required skills have appropriate importance.
        
        :param v: The importance value
        :param values: Other field values
        :return: The validated importance value
        :raises ValueError: If a required skill has importance < 3
        """
        if values.get('priority') == 'required' and v < 3:
            raise ValueError("Required skills must have importance of at least 3")
        return v


class ExperienceAlignment(BaseModel):
    """
    Model representing alignment between resume experience and job requirements.
    
    :ivar years_overlap: Years of relevant experience
    :ivar role_similarity: Similarity score between roles (0-1)
    :ivar domain_relevance: Relevance of domain experience (0-1)
    :ivar tech_stack_overlap: Overlap in technology stack (0-1)
    :ivar leadership_alignment: Alignment on leadership experience (0-1)
    :ivar company_size_relevance: Relevance of company size experience (0-1)
    """
    years_overlap: ReasonedAttribute[float]
    role_similarity: ReasonedAttribute[float]
    domain_relevance: ReasonedAttribute[float]
    tech_stack_overlap: ReasonedAttribute[float]
    leadership_alignment: Optional[ReasonedAttribute[float]] = None 
    company_alignment: Optional[CompanyAlignment] = None

    def get_years_overlap_value(self) -> float:
        """Get the numeric value of years_overlap."""
        return self.years_overlap.score

    def get_role_similarity_value(self) -> float:
        """Get the numeric value of role_similarity."""
        return self.role_similarity.score


class ProjectAlignment(BaseModel):
    """
    Detailed alignment metrics for projects against job requirements.
    
    :ivar technical_stack: Score for technology stack overlap (0-1)
    :ivar domain_relevance: Score for domain knowledge relevance (0-1)
    :ivar role_similarity: Score for role responsibilities similarity (0-1)
    :ivar scale_appropriateness: Score for project scale relevance (0-1)
    :ivar problem_complexity: Score for problem complexity alignment (0-1)
    """
    technical_stack: float = Field(ge=0, le=1)
    domain_relevance: float = Field(ge=0, le=1)
    role_similarity: float = Field(ge=0, le=1)
    scale_appropriateness: float = Field(ge=0, le=1, default=0.5)
    problem_complexity: float = Field(ge=0, le=1, default=0.5)


class ProjectMatch(BaseModel):
    """
    Comprehensive analysis of how a project matches job requirements.
    
    :ivar project_name: Name or description of the project
    :ivar company: Company where project was completed
    :ivar timeline: Project timeline information
    :ivar relevance_score: Overall relevance score (1-5)
    :ivar matching_keywords: Keywords from job description found in project
    :ivar missing_keywords: Important keywords not found in project
    :ivar enhancement_suggestion: Suggestion for improving project description
    :ivar alignment_score: Detailed alignment metrics
    :ivar highlight_recommendation: Specific aspects to highlight
    """
    project_name: str
    company: Optional[str] = None
    timeline: Optional[str] = None
    relevance_score: int = Field(ge=1, le=5)
    matching_keywords: List[str]
    missing_keywords: List[str]
    enhancement_suggestion: str
    alignment_score: ProjectAlignment
    highlight_recommendation: Optional[str] = None


class ImprovementPriority(str, Enum):
    """
    Priority levels for improvement recommendations.
    
    :cvar CRITICAL: Must be addressed to have a chance at the position
    :cvar HIGH: Strongly recommended to improve chances
    :cvar MEDIUM: Should be addressed but not urgent
    :cvar LOW: Minor enhancement that would help slightly
    """
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PriorityImprovement(BaseModel):
    """
    Prioritized improvement recommendation for the candidate.
    
    :ivar action: Specific action to take
    :ivar section: Resume section to improve
    :ivar priority: Importance level of the improvement
    :ivar timeframe: Estimated time to implement
    :ivar impact: Expected impact on application success
    :ivar reasoning: Explanation of why this matters
    :ivar examples: Optional example implementations
    """
    action: str
    section: Literal["skills", "experience", "education", "summary", "projects", "certifications", "achievements"]
    priority: ImprovementPriority
    timeframe: str
    impact: str
    reasoning: str
    examples: Optional[List[str]] = None


class KeywordFrequency(BaseModel):
    """
    Analysis of keyword frequency in the job description.
    
    :ivar keyword: The keyword or phrase
    :ivar count: Number of occurrences
    :ivar sections: Sections where the keyword appears
    :ivar prominence: Score indicating prominence (0-1)
    """
    keyword: str
    count: int
    sections: List[str]
    prominence: float = Field(ge=0, le=1)


class SectionAnalysis(BaseModel):
    """
    Analysis of how well a resume section matches job requirements.
    
    :ivar section: Resume section name
    :ivar match_score: Score indicating match quality (0-1)
    :ivar strengths: Identified strengths in the section
    :ivar weaknesses: Identified weaknesses in the section
    :ivar improvement_suggestions: Specific improvement suggestions
    """
    section: str
    match_score: float = Field(ge=0, le=1)
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]


class ResumeMatchResult(BaseModel):
    """
    Comprehensive result of matching a resume against a job description.
    
    :ivar overall_match_percentage: Overall match percentage (0-100)
    :ivar interview_probability: Estimated probability of getting an interview (0-100)
    :ivar job_overview: Overview of the job position
    :ivar top_strengths: Top strengths of the candidate for this position
    :ivar critical_gaps: Critical gaps in the candidate's profile
    :ivar skill_matches: Detailed skill match analysis
    :ivar experience_alignment: Analysis of experience alignment
    :ivar project_matches: Analysis of project relevance
    :ivar education_alignment: Analysis of education alignment
    :ivar keyword_analysis: Analysis of keyword frequency and coverage
    :ivar section_analysis: Section-by-section analysis
    :ivar priority_improvements: Prioritized improvement recommendations
    :ivar general_suggestions: General enhancement suggestions
    :ivar ideal_candidate_profile: Profile of an ideal candidate
    """
    overall_match_percentage: float = Field(ge=0, le=100)
    interview_probability: float = Field(ge=0, le=100)
    top_strengths: List[str]
    critical_gaps: List[str]
    skill_matches: List[SkillMatch]
    experience_alignment: Optional[ExperienceAlignment] = None
    project_matches: List[ProjectMatch]
    education_alignment: Optional[float] = Field(default=None, ge=0, le=1)
    company_alignment: Optional[CompanyAlignment] = None
    keyword_analysis: Optional[List[KeywordFrequency]] = None
    section_analysis: Optional[List[SectionAnalysis]] = None
    priority_improvements: List[PriorityImprovement]
    general_suggestions: List[str]
    ideal_candidate_profile: Optional[Dict[str, List[str]]] = None