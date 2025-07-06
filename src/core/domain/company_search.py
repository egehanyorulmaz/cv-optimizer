from pydantic import BaseModel, Field
from typing import Optional

class CompanySearchResponse(BaseModel):
    company_name: str = Field(description="The name of the company")
    company_description: Optional[str] = Field(None, description="A description of the company") 
    company_website: Optional[str] = Field(None, description="The website of the company")
    company_location: Optional[str] = Field(None, description="The location of the company")
    company_industry: Optional[str] = Field(None, description="The industry of the company")
    company_size: Optional[int] = Field(None, description="The approximate number of employees at the company")
    company_revenue: Optional[str] = Field(None, description="The annual revenue of the company")
    founded_year: Optional[int] = Field(None, description="The year the company was founded")


if __name__ == "__main__":
    data_model = CompanySearchResponse.model_json_schema()
    print(data_model)