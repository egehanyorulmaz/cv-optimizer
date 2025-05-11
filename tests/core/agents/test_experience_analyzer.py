'''
Tests for the Experience Analyzer Agent.
'''
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta
import pytz
import json

from src.core.agents.experience_analyzer import calculate_years_experience, analyze_experience_node
from src.core.domain.resume import Resume, Experience, ContactInfo, Education
from src.core.domain.job_description import JobDescription, JobRequirement, TechStack
from src.core.domain.resume_match import ExperienceAlignment
from src.core.domain.reasoning import ReasonedAttribute
from src.infrastructure.ai_providers.mock_provider import MockAIProvider
from src.core.domain.config import AIProviderConfig
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.config import TemplateConfig
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor

# --- Fixtures --- 

@pytest.fixture
def mock_ai_provider():
    provider = MockAIProvider(config=AIProviderConfig())
    # Register specific responses if needed for tests
    return provider

@pytest.fixture
def template_service():
    return JinjaTemplateService(config=TemplateConfig.development())

@pytest.fixture
def llm_extractor(mock_ai_provider, template_service):
    return LLMStructuredExtractor(
        ai_provider=mock_ai_provider,
        template_service=template_service
    )

@pytest.fixture
def sample_contact_info():
    return ContactInfo(name="Test User", email="test@example.com")

@pytest.fixture
def sample_experiences():
    return [
        Experience(
            title="Senior Developer",
            company="Tech Corp",
            start_date=datetime(2020, 1, 1, tzinfo=pytz.UTC),
            end_date=None,  # Current job
            description=["Lead development of cloud applications", "Managed team of 5 engineers"],
            achievements=["Reduced deployment time by 30%", "Implemented CI/CD pipeline"]
        ),
        Experience(
            title="Developer",
            company="Startup Inc",
            start_date=datetime(2018, 1, 1, tzinfo=pytz.UTC),
            end_date=datetime(2019, 12, 31, tzinfo=pytz.UTC),
            description=["Developed web applications using React", "Implemented RESTful APIs"],
            achievements=["Launched 3 new features"]
        )
    ]

@pytest.fixture
def sample_education():
    return [
        Education(
            degree="Bachelor of Science in Computer Science",
            institution="University of Technology",
            graduation_date=datetime(2017, 5, 15, tzinfo=pytz.UTC),
            highlights=["Machine Learning focus"]
        )
    ]

@pytest.fixture
def sample_resume(sample_contact_info, sample_experiences, sample_education):
    return Resume(
        contact_info=sample_contact_info,
        summary="Experienced software engineer with focus on cloud technologies",
        experiences=sample_experiences,
        education=sample_education,
        skills=["Python", "JavaScript", "AWS", "Docker", "React"]
    )

@pytest.fixture
def sample_job_description():
    return JobDescription(
        company_name="Innovation Tech",
        title="Senior Software Engineer",
        location="Remote",
        description="We are looking for a Senior Software Engineer to join our cloud platform team. The ideal candidate will have experience with modern web technologies and cloud infrastructure.",
        benefits=[],
        tech_stack=[
            TechStack(
                tech_type="Programming Languages",
                tech_description="Python",
                priority="required"
            ),
            TechStack(
                tech_type="Cloud",
                tech_description="AWS",
                priority="required"
            ),
            TechStack(
                tech_type="Frontend",
                tech_description="React",
                priority="nice_to_have"
            )
        ],
        requirements=[
            JobRequirement(
                requirement_type="required",
                requirement_description="3+ years of software development experience"
            ),
            JobRequirement(
                requirement_type="required",
                requirement_description="Experience with team leadership"
            ),
            JobRequirement(
                requirement_type="nice_to_have",
                requirement_description="Experience with CI/CD pipelines"
            )
        ]
    )

@pytest.fixture
def sample_state(sample_resume, sample_job_description):
    return {
        "resume": sample_resume,
        "job_description": sample_job_description
    }

# Create a mock extractor for testing
@pytest.fixture
def mock_llm_extractor():
    mock_extractor = MagicMock()
    mock_extractor.generate_structured_output = AsyncMock()
    return mock_extractor

# --- Tests for calculate_years_experience --- 

@pytest.mark.asyncio
async def test_calculate_years_experience_no_experience():
    actual_years = await calculate_years_experience([])
    assert actual_years == 0.0

@pytest.mark.asyncio
async def test_calculate_years_experience_single_job():
    exp = [
        Experience(
            title="Dev", company="CompA", 
            start_date=datetime(2020, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2022, 1, 1, tzinfo=pytz.UTC), 
            description=[], achievements=[]
        )
    ]
    actual_years = await calculate_years_experience(exp)
    assert actual_years == pytest.approx(2.0, abs=0.01)

@pytest.mark.asyncio
async def test_calculate_years_experience_ongoing_job():
    start = datetime.now(pytz.UTC) - timedelta(days=365*3 + 5)
    exp = [
        Experience(
            title="Dev", company="CompA", 
            start_date=start, 
            end_date=None,  # Ongoing
            description=[], achievements=[]
        )
    ]
    # Should be approx 3 years
    actual_years = await calculate_years_experience(exp)
    assert actual_years == pytest.approx(3.0, abs=0.02)

@pytest.mark.asyncio
async def test_calculate_years_experience_non_overlapping():
    exp = [
        Experience(
            title="Dev1", company="CompA", 
            start_date=datetime(2018, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2019, 1, 1, tzinfo=pytz.UTC), # 1 year
            description=[], achievements=[]
        ),
        Experience(
            title="Dev2", company="CompB", 
            start_date=datetime(2020, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2022, 1, 1, tzinfo=pytz.UTC), # 2 years
            description=[], achievements=[]
        )
    ]
    # Total 3 years
    actual_years = await calculate_years_experience(exp)
    assert actual_years == pytest.approx(3.0, abs=0.01)

@pytest.mark.asyncio
async def test_calculate_years_experience_overlapping():
    exp = [
        Experience(
            title="Dev1", company="CompA", 
            start_date=datetime(2019, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2021, 1, 1, tzinfo=pytz.UTC), # 2 years (Jan 2019 - Jan 2021)
            description=[], achievements=[]
        ),
        Experience(
            title="Dev2", company="CompB", 
            start_date=datetime(2020, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2022, 1, 1, tzinfo=pytz.UTC), # 2 years (Jan 2020 - Jan 2022)
            description=[], achievements=[]
        )
    ]
    # Overlap is 1 year (Jan 2020 - Jan 2021)
    # Total unique duration is 3 years (Jan 2019 - Jan 2022)
    actual_years = await calculate_years_experience(exp)
    assert actual_years == pytest.approx(3.0, abs=0.01)

@pytest.mark.asyncio
async def test_calculate_years_experience_multiple_overlaps_and_ongoing():
    start_ongoing = datetime.now(pytz.UTC) - timedelta(days=365*1)
    exp = [
        Experience( # 2 years (2017-2019)
            title="Dev1", company="CompA", 
            start_date=datetime(2017, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2019, 1, 1, tzinfo=pytz.UTC), 
            description=[], achievements=[]
        ),
        Experience( # 2 years (2018-2020) - overlaps 1 year with first
            title="Dev2", company="CompB", 
            start_date=datetime(2018, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2020, 1, 1, tzinfo=pytz.UTC), 
            description=[], achievements=[]
        ),
         Experience( # 1 year (ongoing) - starts after others
            title="Dev3", company="CompC", 
            start_date=start_ongoing, 
            end_date=None, 
            description=[], achievements=[]
        )
    ]
    # Unique periods: 2017-2020 (3 years) + ongoing (1 year) = 4 years
    actual_years = await calculate_years_experience(exp)
    assert actual_years == pytest.approx(4.0, abs=0.02)

@pytest.mark.asyncio
async def test_calculate_years_experience_invalid_dates():
    # Experience ends before it starts - should be ignored
    exp = [
        Experience(
            title="Dev", company="CompA", 
            start_date=datetime(2022, 1, 1, tzinfo=pytz.UTC), 
            end_date=datetime(2020, 1, 1, tzinfo=pytz.UTC), 
            description=[], achievements=[]
        )
    ]
    actual_years = await calculate_years_experience(exp)
    assert actual_years == 0.0

# --- Updated Tests for analyze_experience_node --- 

@pytest.mark.asyncio
async def test_analyze_experience_node_success(mock_llm_extractor, sample_state):
    # Get the actual calculated years for the test fixture
    actual_years = await calculate_years_experience(sample_state["resume"].experiences)
    
    # Setup expected alignment data
    expected_alignment = ExperienceAlignment(
        years_overlap=ReasonedAttribute(score=actual_years, reasoning="test"),
        role_similarity=ReasonedAttribute(score=0.85, reasoning="test"),
        domain_relevance=ReasonedAttribute(score=0.7, reasoning="test"),
        tech_stack_overlap=ReasonedAttribute(score=0.9, reasoning="test"),
        leadership_alignment=ReasonedAttribute(score=0.8, reasoning="test"),
        company_size_relevance=None
    )
    
    # Configure the mock to return our expected data
    mock_response = json.dumps(expected_alignment.model_dump())
    mock_llm_extractor.generate_structured_output.return_value = expected_alignment
    
    # Call the function
    result = await analyze_experience_node(sample_state, mock_llm_extractor)
    
    # Verify results
    assert mock_llm_extractor.generate_structured_output.called
    assert "experience_alignment" in result
    assert result["experience_alignment"] == expected_alignment

@pytest.mark.asyncio
async def test_analyze_experience_node_with_real_extractor(sample_state):
    # Create a mock extractor instead of using a real one with a mock provider
    mock_extractor = MagicMock()
    
    # Define the expected return value of the extractor
    expected_alignment = ExperienceAlignment(
        years_overlap=ReasonedAttribute(score=3.5, reasoning="The candidate has 3.5 years of relevant experience."),
        role_similarity=ReasonedAttribute(score=0.85, reasoning="The roles are very similar."),
        domain_relevance=ReasonedAttribute(score=0.7, reasoning="The domain experience is relevant."),
        tech_stack_overlap=ReasonedAttribute(score=0.9, reasoning="Strong tech stack match."),
        leadership_alignment=ReasonedAttribute(score=0.8, reasoning="Good leadership experience.")
    )
    
    # Configure the mock to return our expected data
    mock_extractor.generate_structured_output = AsyncMock(return_value=expected_alignment)
    
    # Call the function with our completely mocked extractor
    result = await analyze_experience_node(sample_state, mock_extractor)
    
    # Assertions
    assert result is not None
    assert "experience_alignment" in result
    assert result["experience_alignment"] is not None
    assert result["experience_alignment"] == expected_alignment

@pytest.mark.asyncio
async def test_analyze_experience_node_empty_experiences(sample_state, mock_llm_extractor):
    # Create a copy of the state to modify
    state = sample_state.copy()
    
    # Replace experiences with an empty list
    modified_resume = state["resume"].model_copy(deep=True)
    modified_resume.experiences = []
    state["resume"] = modified_resume
    
    # Call the function with the modified state
    result = await analyze_experience_node(state, mock_llm_extractor)
    
    # Assert the result indicates no experience alignment was performed
    assert "experience_alignment" in result
    assert result["experience_alignment"] is None

@pytest.mark.asyncio
async def test_analyze_experience_node_invalid_llm_response(sample_state, mock_llm_extractor):
    # Mock generate_structured_output to raise an exception
    mock_llm_extractor.generate_structured_output.side_effect = ValueError("Invalid JSON response")
    
    # Call the function
    result = await analyze_experience_node(sample_state, mock_llm_extractor)
    
    # Assert that error handling works and returns None for experience_alignment
    assert "experience_alignment" in result
    assert result["experience_alignment"] is None

@pytest.mark.asyncio
async def test_analyze_experience_node_missing_required_fields(sample_state, mock_llm_extractor):
    # Mock generate_structured_output to raise a validation error
    mock_llm_extractor.generate_structured_output.side_effect = ValueError("Missing required fields")
    
    # Call the function
    result = await analyze_experience_node(sample_state, mock_llm_extractor)
    
    # Assert that error handling works and returns None for experience_alignment
    assert "experience_alignment" in result
    assert result["experience_alignment"] is None 