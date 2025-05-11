import pytest
from pathlib import Path
from reportlab.pdfgen import canvas
import os

@pytest.fixture(scope="session")
def sample_resume_pdf(tmp_path_factory):
    """
    Create a sample PDF file for testing.
    
    :param tmp_path_factory: Pytest fixture for creating temporary directories
    :returns: Path to the sample PDF file
    :rtype: Path
    """
    # Create a temporary directory that persists for the session
    tmp_dir = tmp_path_factory.mktemp("test_files")
    pdf_path = tmp_dir / "sample_resume.pdf"
    
    # Create a test PDF
    c = canvas.Canvas(str(pdf_path))
    
    # Add test content
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "john.doe@example.com")
    c.drawString(100, 710, "123-456-7890")
    
    # Add sections
    c.drawString(100, 650, "Summary")
    c.drawString(100, 630, "Experienced software engineer")
    
    c.drawString(100, 590, "Experience")
    c.drawString(100, 570, "Senior Developer at Tech Corp")
    
    c.save()
    
    return pdf_path

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up the test environment with necessary environment variables."""
    # Store original env vars
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["OPENAI_API_KEY"] = "test_key_for_ci"
    
    yield
    
    # Restore original env vars
    for key, value in original_env.items():
        os.environ[key] = value
    
    # Remove any env vars that were added but weren't in the original set
    for key in list(os.environ.keys()):
        if key not in original_env:
            del os.environ[key]