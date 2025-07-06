'''
Agent responsible for analyzing the alignment between resume experience and job description using an LLM.
'''

import logging
from typing import Dict, List, Optional
from datetime import datetime
import pytz

from src.core.agents.utils.state import AgentState
from src.core.domain.resume_match import ExperienceAlignment
from src.core.domain.resume import Experience
from src.core.domain.job_description import JobDescription
from langsmith import traceable
from src.core.ports.secondary.llm_extractor import LLMExtractor

logger = logging.getLogger("core.agents.experience_analyzer")

@traceable(run_type="parser")
async def calculate_years_experience(experiences: List[Experience]) -> float:
    '''
    Calculates the total years of professional experience from a list of experiences.
    Handles overlapping time periods by taking the union of intervals.

    :param experiences: List of Experience objects from the resume.
    :type experiences: List[Experience]
    :return: Total years of experience, accounting for overlaps.
    :rtype: float
    '''
    if not experiences:
        return 0.0

    intervals = []
    for exp in experiences:
        if exp.start_date:
            # Use current date for ongoing jobs
            end_date = exp.end_date if exp.end_date else datetime.now(pytz.UTC)
            # Ensure start_date is not in the future and end_date is after start_date
            if exp.start_date < end_date:
                 intervals.append((exp.start_date.timestamp(), end_date.timestamp()))
    
    if not intervals:
        return 0.0

    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])

    merged = []
    if intervals:
        current_start, current_end = intervals[0]
        for next_start, next_end in intervals[1:]:
            if next_start < current_end: # Overlap
                current_end = max(current_end, next_end)
            else: # No overlap
                merged.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        merged.append((current_start, current_end))

    total_duration_seconds = sum(end - start for start, end in merged)
    total_years = total_duration_seconds / (365.25 * 24 * 60 * 60) # Account for leap years
    
    return round(total_years, 2)

@traceable(run_type="parser")
async def format_experiences_for_prompt(experiences: List[Experience]) -> str:
    '''Formats the experience list into a readable string for the LLM prompt.'''
    output = []
    for exp in experiences:
        start_str = exp.start_date.strftime('%Y-%m') if exp.start_date else "N/A"
        end_str = exp.end_date.strftime('%Y-%m') if exp.end_date else "Present"
        desc_str = "\n".join([f"  - {d}" for d in exp.description])
        ach_str = "\n".join([f"  - Achievement: {a}" for a in exp.achievements])
        output.append(
            f"Title: {exp.title}\n"
            f"Company: {exp.company}\n"
            f"Dates: {start_str} to {end_str}\n"
            f"Description:\n{desc_str}\n"
            f"Achievements:\n{ach_str}\n"
            f"---"
        )
    return "\n".join(output)

@traceable(run_type="parser")
async def format_job_details_for_prompt(job: JobDescription) -> Dict[str, str]:
    '''Formats relevant job details into strings for the LLM prompt.'''
    tech_stack_str = "\n".join([f"- {ts.tech_description} ({ts.priority})" for ts in job.tech_stack])
    requirements_str = "\n".join([f"- {req.requirement_description} ({req.requirement_type})" for req in job.requirements])
    return {
        "job_title": job.title,
        "job_location": job.location,
        "job_description_text": job.description,
        "job_tech_stack": tech_stack_str if tech_stack_str else "Not specified",
        "job_requirements": requirements_str if requirements_str else "Not specified"
    }

@traceable(run_type="parser")
async def analyze_experience_node(
    state: AgentState,
    extractor: Optional[LLMExtractor] = None
) -> Dict[str, Optional[ExperienceAlignment]]:
    '''
    Analyzes the resume's experience section against the job description 
    using an LLM to determine alignment scores.

    :param state: The current state of the LangGraph execution.
    :type state: AgentState
    :param extractor: The LLM extractor to use for structured output generation, created if None
    :type extractor: LLMExtractor, optional
    :return: A dictionary containing the updated ExperienceAlignment or None if analysis fails.
    :rtype: Dict[str, Optional[ExperienceAlignment]]
    '''
    logger.info("--- Analyzing Experience Alignment (LLM) ---")
    resume = state['resume']
    job_description = state['job_description']
    
    if not resume.experiences:
        logger.warning("No experience found in resume. Skipping experience analysis.")
        return {"experience_alignment": None} 

    # 1. Prepare data for the prompt
    total_years = await calculate_years_experience(resume.experiences)
    experiences_text = await format_experiences_for_prompt(resume.experiences)

    try:
        # Call the LLM and parse the response
        alignment = await extractor.generate_structured_output(
            template_path="prompts/agents/experience_analyzer.j2",
            template_vars={"resume_experiences": experiences_text,
                          "job_description": job_description,
                          "total_years_experience": total_years},
            output_model=ExperienceAlignment
        )
        
        # Validate years_overlap for consistency
        if abs(float(alignment.years_overlap.score) - total_years) > 0.01:
            logger.warning(f"LLM years_overlap ({alignment.years_overlap.score}) doesn't match calculated {total_years}. Using calculated value.")
            alignment.years_overlap.score = total_years

        logger.info(f"EXPERIENCE ANALYZER: Determined experience alignment: {alignment}")
        # Return the alignment results
        return {"experience_alignment": alignment}
        
    except Exception as e:
        logger.error(f"Failed to analyze experience alignment: {str(e)}")
        return {"experience_alignment": None}