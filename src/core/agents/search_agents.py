import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any, List

from src.core.ports.secondary.template_service import TemplateService
from src.core.agents.utils.state import AgentState
from src.core.domain.company_search import CompanySearchResponse


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

async def create_company_search_agent(response_format: Type[BaseModel], 
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
        model_name=model_name, 
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
                        model_name="gpt-3.5-turbo") -> Optional[CompanySearchResponse]:
    """
    Search for up-to-date information about a company and return structured data.
    """
    search_query = template_service.render_prompt(
        "prompts/company_search/search_query.j2",
        **{"company_name": company_name, "search_result_format": CompanySearchResponse.model_json_schema()}
    )
    
    try:
        agent = await create_company_search_agent(CompanySearchResponse, template_service, model_name)
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": search_query}]}
        )
        
        if "structured_response" in response:
            result = response["structured_response"]
            return CompanySearchResponse.model_validate(result)
        else:
            print("No structured response found in agent output")
            return None
    except Exception as e:
        print(f"Error searching for company info: {str(e)}")
        return None


async def main():
    from src.core.domain.config import TemplateConfig
    from src.infrastructure.template.jinja_template_service import JinjaTemplateService
    template_config = TemplateConfig.development()
    template_service = JinjaTemplateService(config=template_config)
    
    company_info = await search_company_info("Apple Inc.", template_service, model_name="gpt-4o")
    
    if company_info:
        print("\nCompany Information:")
        print(f"Name: {company_info.company_name}")
        print(f"Industry: {company_info.company_industry}")
        print(f"Size: {company_info.company_size} employees")
        print(f"Revenue: {company_info.company_revenue}")
        print(f"Location: {company_info.company_location}")
        print(f"Website: {company_info.company_website}")
        print(f"Founded: {company_info.founded_year or 'Unknown'}")
        print(f"Description: {company_info.company_description}")
    else:
        print("Could not retrieve company information.")