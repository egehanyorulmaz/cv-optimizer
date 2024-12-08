from pydantic import BaseModel

class JobDescription(BaseModel):
    company_name: st
    title: str
    description: str
