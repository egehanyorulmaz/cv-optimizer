import asyncio
from typing import Dict, Optional, Literal, List
from langsmith import traceable
import logging

from src.core.agents.utils.state import AgentState
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.company_search import CompanyInfo
from src.infrastructure.components import llm_extractor
from src.core.ports.secondary.llm_extractor import LLMExtractor
from src.core.ports.secondary.template_service import TemplateService
from src.core.agents.search_agents import search_company_info

logger = logging.getLogger("core.agents.nodes")

@traceable(run_type="llm")
async def parse_resume_node(state: AgentState, extractor: LLMExtractor):
    resume = await extractor.parse_document(
        content=state["resume_path"],
        output_model=Resume,
        template_path="prompts/parsing/resume_extractor.j2"
    )
    return {"resume": resume}


@traceable(run_type="llm")
async def parse_job_description_node(state: AgentState, extractor: LLMExtractor):
    job_description = await extractor.parse_document(
        content=state["job_description_path"],
        output_model=JobDescription,
        template_path="prompts/parsing/job_description_extractor.j2"
    )
    return {"job_description": job_description}


@traceable(run_type="tool")
async def search_company_info_node(state: AgentState, 
                                   template_service: TemplateService, 
                                   branch: Literal["resume", "job_desription"] = "job_description",
                                   model_name="gpt-4.1-mini") -> Dict[str, Optional[CompanyInfo]]:
    if branch == "resume":
        companies = state["resume"].company_names
    elif branch == "job_description":
        companies = [state["job_description"].company_name]
    else:
        raise ValueError("This branch is not supported.")
    
    tasks = [search_company_info(company_name=company_name, 
                                 model_name=model_name, 
                                 template_service=template_service) for company_name in companies]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    results = {result.name: result for result in results if isinstance(result, CompanyInfo)}
    logger.info(f"Retrieved information for branch {branch} with length {len(results)} companies.")

    return {f"{branch}_company_info": results}