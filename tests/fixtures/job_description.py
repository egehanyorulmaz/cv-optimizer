# tests/fixtures/job_descriptions.py
from datetime import datetime
import pytz
from src.core.domain.job_description import JobDescription, JobRequirement, TechStack, JobBenefit

def create_sample_software_engineer_job():
    """
    Create a sample Software Engineer job description for testing.
    
    :return: A fully populated JobDescription object
    :rtype: JobDescription
    """
    return JobDescription(
        company_name="TechInnovators Inc.",
        title="Senior Software Engineer",
        location="San Francisco, CA (Remote Option)",
        description="""
        TechInnovators Inc. is seeking a Senior Software Engineer to join our growing team.
        The ideal candidate will be passionate about building scalable, high-performance
        applications and have expertise in cloud infrastructure and modern software
        development practices.
        
        You will work closely with product managers, designers, and other engineers to
        design, develop, and deploy new features and improvements to our platform.
        """,
        benefits=[
            JobBenefit(
                benefit_type="other",
                benefit_description="Competitive salary and equity package"
            ),
            JobBenefit(
                benefit_type="health_insurance",
                benefit_description="Comprehensive health, dental, and vision insurance"
            ),
            JobBenefit(
                benefit_type="other",
                benefit_description="Flexible work hours and remote work options"
            ),
            JobBenefit(
                benefit_type="other",
                benefit_description="Professional development budget"
            ),
            JobBenefit(
                benefit_type="retirement_fund",
                benefit_description="401(k) matching"
            )
        ],
        tech_stack=[
            TechStack(
                tech_type="Programming Languages",
                tech_description="Python, TypeScript, Go",
                priority="required"
            ),
            TechStack(
                tech_type="Frontend",
                tech_description="React, Next.js, Redux",
                priority="required"
            ),
            TechStack(
                tech_type="Backend",
                tech_description="FastAPI, Django, Node.js",
                priority="required"
            ),
            TechStack(
                tech_type="Database",
                tech_description="PostgreSQL, MongoDB, Redis",
                priority="required"
            ),
            TechStack(
                tech_type="Cloud",
                tech_description="AWS, GCP, Docker, Kubernetes",
                priority="required"
            ),
            TechStack(
                tech_type="DevOps",
                tech_description="CI/CD, GitHub Actions, Terraform",
                priority="nice_to_have"
            ),
            TechStack(
                tech_type="Testing",
                tech_description="Pytest, Jest, Cypress",
                priority="nice_to_have"
            )
        ],
        requirements=[
            JobRequirement(
                requirement_type="required",
                requirement_description="5+ years of professional software development experience"
            ),
            JobRequirement(
                requirement_type="required",
                requirement_description="Strong experience with Python and at least one frontend framework"
            ),
            JobRequirement(
                requirement_type="required",
                requirement_description="Experience building and maintaining REST APIs"
            ),
            JobRequirement(
                requirement_type="required", 
                requirement_description="Experience with cloud services (AWS, GCP, or Azure)"
            ),
            JobRequirement(
                requirement_type="nice_to_have",
                requirement_description="Experience with machine learning or data science"
            ),
            JobRequirement(
                requirement_type="nice_to_have",
                requirement_description="Open source contributions"
            ),
            JobRequirement(
                requirement_type="nice_to_have",
                requirement_description="Experience working in a startup environment"
            )
        ],
        salary_range="$120,000 - $180,000",
        posting_date=datetime(2023, 6, 15, tzinfo=pytz.UTC),
        application_deadline=datetime(2023, 8, 15, tzinfo=pytz.UTC)
    )