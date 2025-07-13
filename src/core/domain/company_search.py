from pydantic import BaseModel, Field
from typing import Optional

class CompanyInfo(BaseModel):
    name: str = Field(description="The name of the company")
    description: Optional[str] = Field(None, description="A description of the company") 
    website: Optional[str] = Field(None, description="The website of the company")
    location: Optional[str] = Field(None, description="The location of the company")
    industry: Optional[str] = Field(None, description="The industry of the company")
    size: Optional[int] = Field(None, description="The approximate number of employees at the company")
    revenue: Optional[str] = Field(None, description="The annual revenue of the company")
    founded_year: Optional[int] = Field(None, description="The year the company was founded")


if __name__ == "__main__":
    data_model = CompanyInfo.model_json_schema()
    print(data_model)