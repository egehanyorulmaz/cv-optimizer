from typing import List
import pdfplumber
from datetime import datetime
import re
from ...core.ports.document_parser import DocumentParser
from ...core.domain.resume import Resume, ContactInfo, Experience, Education

class PDFParser(DocumentParser):
    def __init__(self):
        self._supported_formats = ['.pdf']
        
    @property
    def supported_formats(self) -> List[str]:
        return self._supported_formats

    async def parse(self, content: bytes) -> Resume:
        with pdfplumber.open(content) as pdf:
            text = '\n'.join(page.extract_text() for page in pdf.pages)
            
        # Parse sections
        sections = self._split_into_sections(text)
        
        contact_info = self._parse_contact_info(sections.get('contact', ''))
        summary = sections.get('summary', '').strip()
        experiences = self._parse_experiences(sections.get('experience', ''))
        education = self._parse_education(sections.get('education', ''))
        skills = self._parse_skills(sections.get('skills', ''))
        certifications = self._parse_certifications(sections.get('certifications', ''))

        return Resume(
            contact_info=contact_info,
            summary=summary,
            experiences=experiences,
            education=education,
            skills=skills,
            certifications=certifications
        )

    async def reconstruct(self, resume: Resume) -> bytes:
        # This would require a PDF generation library like ReportLab
        # For now, we'll raise NotImplementedError
        raise NotImplementedError("PDF reconstruction not yet implemented")

    def _split_into_sections(self, text: str) -> dict[str, str]:
        """Split resume text into sections based on common headers"""
        common_headers = {
            'contact': r'(?i)(contact|personal) information',
            'summary': r'(?i)(summary|profile|objective)',
            'experience': r'(?i)(experience|work history|employment)',
            'education': r'(?i)education',
            'skills': r'(?i)(skills|technical skills)',
            'certifications': r'(?i)(certifications|certificates)'
        }
        
        sections = {}
        current_section = None
        current_text = []
        
        for line in text.split('\n'):
            matched_section = None
            for section, pattern in common_headers.items():
                if re.match(pattern, line.strip()):
                    matched_section = section
                    break
            
            if matched_section:
                if current_section:
                    sections[current_section] = '\n'.join(current_text)
                current_section = matched_section
                current_text = []
            elif current_section:
                current_text.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_text)
        
        return sections

    def _parse_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information using regex patterns"""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        linkedin = re.search(linkedin_pattern, text)
        
        # First line is usually the name
        name = text.split('\n')[0].strip()
        
        return ContactInfo(
            name=name,
            email=email.group(0) if email else "",
            phone=phone.group(0) if phone else None,
            linkedin=linkedin.group(0) if linkedin else None
        )

    def _parse_experiences(self, text: str) -> List[Experience]:
        """Parse work experience sections"""
        experiences = []
        # Split into individual positions (implementation details omitted for brevity)
        # This would involve complex regex patterns to identify job entries
        return experiences

    def _parse_education(self, text: str) -> List[Education]:
        """Parse education sections"""
        education = []
        # Similar to experiences parsing
        return education

    def _parse_skills(self, text: str) -> List[str]:
        """Extract skills from skills section"""
        if not text:
            return []
        
        # Remove common headers and split by common delimiters
        skills_text = re.sub(r'(?i)(skills|technical skills):', '', text)
        skills = [
            skill.strip()
            for skill in re.split(r'[,•|\n]', skills_text)
            if skill.strip()
        ]
        return skills

    def _parse_certifications(self, text: str) -> List[str]:
        """Extract certifications from certifications section"""
        if not text:
            return None
        
        certs = [
            cert.strip()
            for cert in text.split('\n')
            if cert.strip() and not re.match(r'(?i)certification', cert)
        ]
        return certs if certs else None 