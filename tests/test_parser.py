import pytest
import asyncio
from pathlib import Path
from cv_optimizer.infrastructure.parsers.pdf_parser import PDFParser

class TestPDFParser:
    @pytest.fixture
    def parser(self):
        return PDFParser()
    
    @pytest.fixture
    def sample_resume_path(self):
        # Update this path to point to your test resume file
        return Path("./fixtures/sample_resume.pdf")
    
    @pytest.mark.asyncio
    async def test_resume_parsing(self, parser, sample_resume_path):
        content = sample_resume_path.read_bytes()
        resume = await parser.parse(content)
        
        # Assertions to verify parsing
        assert resume.contact_info is not None
        assert resume.contact_info.name != ""
        assert '@' in resume.contact_info.email
        
        
    def print_resume_details(self, resume):
        """Helper method to print resume details for debugging"""
        print("\n=== Parsed Resume Information ===\n")
        
        print("Contact Information:")
        print(f"Name: {resume.contact_info.name}")
        print(f"Email: {resume.contact_info.email}")
        print(f"Phone: {resume.contact_info.phone}")
        print(f"LinkedIn: {resume.contact_info.linkedin}")
        
        print("\nSummary:")
        print(resume.summary)
        
        print("\nSkills:")
        for skill in resume.skills:
            print(f"- {skill}")
        
        print("\nExperience:")
        for exp in resume.experiences:
            print(f"\n- {exp.title} at {exp.company}")
        
        print("\nEducation:")
        for edu in resume.education:
            print(f"\n- {edu.degree} from {edu.institution}")
        
        if resume.certifications:
            print("\nCertifications:")
            for cert in resume.certifications:
                print(f"- {cert}")

# For manual testing and debugging
async def debug_resume_parsing(file_path: str):
    parser = PDFParser()
    content = Path(file_path).read_bytes()
    
    try:
        resume = await parser.parse(content)
        TestPDFParser().print_resume_details(resume)
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "tests/fixtures/sample_resume.pdf"
    
    print(f"Debugging resume parsing for file: {file_path}")
    asyncio.run(debug_resume_parsing(file_path))