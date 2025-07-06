import asyncio
from typing import Dict, Optional
from langsmith import traceable
from src.core.agents.utils.state import AgentState
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.core.domain.company_search import CompanySearchResponse
from src.infrastructure.components import llm_extractor
from src.core.ports.secondary.llm_extractor import LLMExtractor
from src.core.ports.secondary.template_service import TemplateService
from src.core.agents.search_agents import search_company_info

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
                                   model_name="gpt-4o") -> Dict[str, Optional[CompanySearchResponse]]:
    """
    Search for information about a company and return structured data.
    """
    company_names = [experience.company for experience in state["resume"].experiences]

    tasks = [search_company_info(company, template_service, model_name) for company in company_names]
    results = await asyncio.gather(*tasks)
    company_info_list = [result for result in results if result is not None]
    print(f"Retrieved information for {len(company_info_list)} out of {len(company_names)} companies.")
    return {"company_info": company_info_list}