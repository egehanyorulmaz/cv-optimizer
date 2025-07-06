# In your graph builder file (e.g., src/core/agents/graph_builder.py)
from src.core.agents.experience_analyzer import analyze_experience_node
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.config import AIProviderConfig, TemplateConfig

from src.core.domain.job_description import JobDescription
from src.core.domain.constants import TEST_RESUME_FILE_PATH, TEST_JOB_DESCRIPTION_FILE_PATH

# agent
from langgraph.graph import StateGraph, START, END
from langchain.schema.runnable import RunnableMap
from langgraph.types import CachePolicy
from src.core.agents.utils.nodes import parse_resume_node, parse_job_description_node, search_company_info_node
from src.core.agents.utils.state import AgentState
import logging
from src.infrastructure.components import llm_extractor
from functools import partial

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("core.agents.graph_builder")

def build_resume_analysis_graph():
    workflow = StateGraph(AgentState)
    logger.info("Building workflow...")

    # Use functools.partial to inject dependencies into the nodes
    workflow.add_node("parse_resume", partial(parse_resume_node, extractor=llm_extractor))
    workflow.add_node("company_research", partial(search_company_info_node, template_service=template_service, model_name="gpt-4o"))
    workflow.add_node("parse_job_description", partial(parse_job_description_node, extractor=llm_extractor))
    workflow.add_node("experience_analyzer", partial(analyze_experience_node, extractor=llm_extractor))
    # Connect nodes sequentially
    workflow.add_edge(START, "parse_resume")
    workflow.add_edge("parse_resume", "company_research")
    workflow.add_edge("company_research", "parse_job_description")
    workflow.add_edge("parse_job_description", "experience_analyzer")
    workflow.add_edge("experience_analyzer", END)
    
    # Compile and return the graph
    return workflow.compile()

if __name__ == "__main__":
    import asyncio
    
    logger.info("Building graph...")
    ai_provider = OpenAIProvider(config=AIProviderConfig())
    template_service = JinjaTemplateService(config=TemplateConfig.development())

    # Accept file paths from command line or use defaults
    resume_path = TEST_RESUME_FILE_PATH
    job_description_path = TEST_JOB_DESCRIPTION_FILE_PATH

    agent_state = {
        "resume_path": resume_path,
        "job_description_path": job_description_path
    }
    app = build_resume_analysis_graph()

    print("\n--- LangGraph ASCII Diagram ---")
    print(app.get_graph().draw_ascii())

    asyncio.run(app.ainvoke(agent_state))