import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any, List, Literal
import logging

from src.core.ports.secondary.template_service import TemplateService
from src.core.agents.utils.state import AgentState
from src.core.domain.company_search import CompanyInfo

logger = logging.getLogger("core.agents.search_agents")

def get_search_tool(max_results=3, time_range="month"):
    """
    Create a Tavily search tool optimized for recent and accurate company information.
    
    Args:
        max_results: Maximum number of search results to return
        time_range: Time range for search results (day, week, month, year)
        
    Returns:
        Configured TavilySearchResults tool
    """
    return TavilySearchResults(
        max_results=max_results,
        include_answer=True,
        include_raw_content=False,  # Keep this False to reduce token usage
        time_range=time_range,      # Prioritize recent information
        topic="general",           # Use "general" for company information
    )

def create_company_search_agent(response_format: Type[BaseModel], 
                                template_service: TemplateService,
                                model_name="gpt-3.5-turbo"):
    """
    Create a company information search agent that prioritizes web searches.
    
    Args:
        response_format: Pydantic model defining the structured output format
        model_name: Name of the OpenAI model to use
    
    Returns:
        A LangGraph agent that can search for company information
    """
    search_tool = get_search_tool()
    
    model = ChatOpenAI(
        model=model_name, 
        temperature=0.2,
    )
    
    system_prompt = template_service.render_prompt(
        "prompts/company_search/system_prompt.j2"
    )
                        
    agent = create_react_agent(
        model=model,
        tools=[search_tool],
        response_format=response_format,
        prompt=system_prompt,
    )

    return agent

async def search_company_info(company_name: str, 
                        template_service: TemplateService, 
                        model_name="gpt-3.5-turbo") -> Optional[CompanyInfo]:
    """
    Search for up-to-date information about a company and return structured data.
    """
    logger.info(f"Collecting more details on {company_name}")
    # TODO: Retry on OpenAI rate limit errors
    search_query = template_service.render_prompt(
        "prompts/company_search/search_query.j2",
        **{"company_name": company_name, "search_result_format": CompanyInfo.model_json_schema()}
    )
    
    try:
        agent = create_company_search_agent(CompanyInfo, template_service, model_name)
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": search_query}]}
        )
        
        if "structured_response" in response:
            result = response["structured_response"]
            return CompanyInfo.model_validate(result)
        else:
            print("No structured response found in agent output")
            return None
    except Exception as e:
        print(f"Error searching for company info: {str(e)}")
        return None




if __name__ == "__main__":
    import asyncio
    from src.core.domain.config import TemplateConfig
    from src.infrastructure.template.jinja_template_service import JinjaTemplateService
    from dotenv import load_dotenv
    load_dotenv()
    template_config = TemplateConfig.development()
    template_service = JinjaTemplateService(config=template_config)
    
    async def main():
        companies = ["Apple Inc.", "Microsoft", "Google", "A non-existent company", 
                     "NVIDIA", "Tesla", "Amazon", "Meta"]
        concurrency_limit = 5
        
        tasks = [search_company_info(company_name=name, template_service=template_service, 
                                     model_name="gpt-4.1-mini") for name in companies]
        results = await asyncio.gather(*tasks)
        
        company_info_map = {info.name: info for info in results if info}

        for company_name in companies:
            company_info = company_info_map.get(company_name)
            if company_info:
                print("\nCompany Information:")
                print(f"  Name: {company_info.name}")
                print(f"  Industry: {company_info.industry}")
                print(f"  Size: {company_info.size} employees")
                print(f"  Revenue: {company_info.revenue}")
                print(f"  Location: {company_info.location}")
                print(f"  Website: {company_info.website}")
                print(f"  Founded: {company_info.founded_year or 'Unknown'}")
                print(f"  Description: {company_info.description}")
            else:
                print(f"\nCould not retrieve company information for {company_name}.")

    asyncio.run(main())