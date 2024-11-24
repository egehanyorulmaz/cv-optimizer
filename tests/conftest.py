import pytest
from pathlib import Path
from reportlab.pdfgen import canvas
from cv_optimizer.core.domain.constants import PROJECT_ROOT

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