import pytest
from pathlib import Path
from reportlab.pdfgen import canvas

@pytest.fixture(scope="session")
def sample_resume_pdf(tmp_path_factory):
    """
    Create a sample PDF file for testing.
    
    :param tmp_path_factory: Pytest fixture for creating temporary directories
    :returns: Path to the sample PDF file
    :rtype: Path
    """
    tmp_dir = tmp_path_factory.mktemp("test_files")
    pdf_path = tmp_dir / "sample_resume.pdf"
    
    c = canvas.Canvas(str(pdf_path))
    
    # Add test content
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "john.doe@example.com")
    c.drawString(100, 710, "123-456-7890")
    c.save()
    
    return pdf_path

@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for async tests.
    
    :returns: Event loop instance
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 