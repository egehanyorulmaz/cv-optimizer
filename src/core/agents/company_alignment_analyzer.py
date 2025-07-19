
import logging

from langsmith import traceable

from src.core.agents.utils.state import AgentState
from src.core.domain.resume_match import CompanyAlignment
from src.core.ports.secondary.ai_provider import AIProvider, AIOptions
from src.core.ports.secondary.template_service import TemplateService

logger = logging.getLogger(__name__)

@traceable(run_type="parser")
async def company_alignment_analyzer(state: AgentState, 
                                     ai_provider: AIProvider,
                                     template_service: TemplateService,
                                     model_name: str = "gpt-4.1-mini") -> dict:
    """
    Analyzes the alignment between the candidate's past companies and the target company.

    :param state: The current state of the agent graph.
    :return: The updated state with company alignment feedback.
    """
    logger.info("Starting company alignment analysis.")
    
    resume_companies = state.get("resume_company_info")
    job_company_info = state.get("job_description_company_info")

    prompt = template_service.render_prompt(
        "prompts/agents/company_alignment_analyzer.j2",
        **{"resume_company_info": resume_companies, "job_description_company_info": job_company_info}
    )

    if not job_company_info or not resume_companies:
        logger.warning("Missing company information for alignment analysis. Skipping.")
        return {"company_alignment_feedback": "Could not perform company alignment analysis due to missing information."}

    job_company = next(iter(job_company_info.values()), None)
    if not job_company:
        logger.warning("No main company info found in job description. Skipping.")
        return {"company_alignment_feedback": "Could not perform company alignment analysis due to missing job company information."}

    response = await ai_provider.complete(prompt=prompt)

    logger.info("Completed company alignment analysis.")
    return {"company_alignment": response}