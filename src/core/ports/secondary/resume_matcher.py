from abc import ABC, abstractmethod
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.resume_match import ResumeMatchResult

class ResumeMatcher(ABC):
    """
    Port interface for resume matching service.
    """
    
    @abstractmethod
    async def match_resume_to_job(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> ResumeMatchResult:
        """
        Match a resume against a job description and provide detailed feedback.

        :param resume: The candidate's resume
        :type resume: Resume
        :param job_description: The target job description
        :type job_description: JobDescription
        :return: Detailed matching results and suggestions
        :rtype: ResumeMatchResult
        :raises ValueError: If either resume or job description is invalid
        """
        pass 