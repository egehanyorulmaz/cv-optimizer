import asyncio
from langsmith import traceable
from src.core.agents.utils.state import AgentState
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.infrastructure.components import llm_extractor
from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH

@traceable(run_type="llm")
async def parse_resume_node(state: AgentState):
    resume = await llm_extractor.parse_document(
        content=state["resume_path"],
        output_model=Resume,
        template_path="prompts/parsing/resume_extractor.j2"
    )
    return {"resume": resume}


@traceable(run_type="llm")
async def parse_job_description_node(state: AgentState):
    job_description = await llm_extractor.parse_document(
        content=state["job_description_path"],
        output_model=JobDescription,
        template_path="prompts/parsing/job_description_extractor.j2"
    )
    return {"job_description": job_description}