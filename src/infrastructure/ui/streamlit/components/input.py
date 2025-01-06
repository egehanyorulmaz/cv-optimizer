"""Input section components for the Streamlit application."""

import streamlit as st
import asyncio
from pathlib import Path
from typing import Optional, Awaitable, TypeVar, Any
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json
import hashlib

from src.infrastructure.ui.streamlit.utils.file_validator import validate_file
from src.infrastructure.extractors.llm_extractor import LLMStructuredExtractor
from src.infrastructure.parsers.pdf_parser import PDFParser
from src.infrastructure.ai_providers.openai_provider import OpenAIProvider
from src.infrastructure.template.jinja_template_service import JinjaTemplateService
from src.core.domain.config import AIProviderConfig, TemplateConfig
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription
from src.infrastructure.ui.streamlit.components import render_action_card
from src.infrastructure.ui.streamlit.state.session import (
    get_resume, get_job_description, get_service,
    set_resume, set_job_description, set_service
)
from src.infrastructure.ui.streamlit.utils.storage import save_json, load_json, clear_data

T = TypeVar('T')

def _compute_file_hash(content: bytes) -> str:
    """Compute SHA-256 hash of file content.
    
    :param content: File content
    :type content: bytes
    :return: Hex digest of hash
    :rtype: str
    """
    return hashlib.sha256(content).hexdigest()

async def _parse_content(content: Any, service_name: str) -> Any:
    """Parse content using the appropriate service.
    
    :param content: The content to parse
    :type content: Any
    :param service_name: Name of the service to use for parsing
    :type service_name: str
    :return: Parsed object
    :rtype: Any
    """
    parser = get_service(service_name)
    if not parser:
        raise ValueError(f"Parser service '{service_name}' not found")
    return await parser.parse(content)

def _read_file_content(file: UploadedFile) -> bytes:
    """Read file content and store it in memory for multiple uses.
    
    :param file: The uploaded file
    :type file: UploadedFile
    :return: File content as bytes
    :rtype: bytes
    """
    content = file.read()
    file.seek(0)
    return content

def render_input_section() -> None:
    """Render the input section for resume and job description."""
    # Load saved data from files
    resume_data = load_json('resume')
    job_data = load_json('job')
    
    if resume_data:
        try:
            set_resume(Resume.model_validate(resume_data))
        except Exception as e:
            st.warning(f"Failed to load saved resume: {str(e)}")
            clear_data('resume')  # Clear invalid data
    
    if job_data:
        try:
            set_job_description(JobDescription.model_validate(job_data))
        except Exception as e:
            st.warning(f"Failed to load saved job description: {str(e)}")
            clear_data('job')  # Clear invalid data
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_resume_upload()
    
    with col2:
        _render_job_description_input()
    
    # Show debug view
    with st.expander("🔍 Debug View", expanded=False):
        _render_debug_view()

def _render_debug_view() -> None:
    """Render debug view showing parsed objects as JSON."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Parsed Resume")
        resume = get_resume()
        if resume:
            st.json(resume.model_dump_json(indent=2))
        else:
            st.info("No resume parsed yet")
    
    with col2:
        st.subheader("💼 Parsed Job Description")
        job = get_job_description()
        if job:
            st.json(job.model_dump_json(indent=2))
        else:
            st.info("No job description parsed yet")

def _render_resume_upload() -> None:
    """Render the resume upload section."""
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("Upload your resume", type=["pdf"])
    
    if resume_file:
        _handle_resume_upload(resume_file)

def _handle_resume_upload(resume_file: UploadedFile) -> None:
    """Handle resume file upload and parsing.
    
    :param resume_file: The uploaded resume file
    :type resume_file: UploadedFile
    :raises ValueError: If the file format is invalid or file is corrupted
    :raises Exception: If there's an error during parsing
    """
    try:
        file_type = resume_file.name.split('.')[-1].lower()
        file_content = _read_file_content(resume_file)
        current_hash = _compute_file_hash(file_content)
        
        # Check if we've already parsed this file
        resume_data = load_json('resume')
        if resume_data and resume_data.get('file_hash') == current_hash:
            return
        
        if not validate_file(file_content, file_type):
            raise ValueError(f"Invalid or corrupted {file_type} file")
            
        st.session_state.resume_parsing = True
        
        # Use st.spinner in a separate container to avoid blocking
        status_container = st.empty()
        with status_container:
            with st.spinner("Parsing resume..."):
                # Run async parsing in a background task
                resume_obj = asyncio.run(_parse_content(file_content, 'resume_parser'))
                set_resume(resume_obj)
                
                # Save to file
                resume_data = resume_obj.model_dump_json()
                resume_data['file_hash'] = current_hash
                save_json('resume', resume_data)
                
                _display_resume_overview()
                status_container.empty()
            
    except ValueError as e:
        st.error(str(e))
        st.session_state.resume_parsing = False
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")
        st.session_state.resume_parsing = False

def _render_job_description_input() -> None:
    """Render the job description input section."""
    st.subheader("💼 Job Description")
    input_type = st.radio(
        "Choose input method",
        ["Upload File", "Paste Text"],
        horizontal=True
    )
    
    if input_type == "Upload File":
        _handle_job_description_file()
    else:
        _handle_job_description_text()

def _handle_job_description_file() -> None:
    """Handle job description file upload."""
    job_file = st.file_uploader("Upload job description", type=["pdf", "txt"])
    
    if job_file:
        try:
            file_type = job_file.name.split('.')[-1].lower()
            file_content = _read_file_content(job_file)
            current_hash = _compute_file_hash(file_content)
            
            # Check if we've already parsed this file
            job_data = load_json('job')
            if job_data and job_data.get('file_hash') == current_hash:
                return
            
            if not validate_file(file_content, file_type):
                raise ValueError(f"Invalid or corrupted {file_type} file")
                
            st.session_state.job_parsing = True
            
            # Use st.spinner in a separate container to avoid blocking
            status_container = st.empty()
            with status_container:
                with st.spinner("Parsing job description..."):
                    if file_type == 'pdf':
                        # For PDF files, pass bytes directly
                        job_obj = asyncio.run(_parse_content(file_content, 'job_parser'))
                    else:
                        # For text files, decode to string
                        job_obj = asyncio.run(_parse_content(file_content.decode('utf-8'), 'job_parser'))
                    set_job_description(job_obj)
                    
                    # Save to file
                    job_data = job_obj.model_dump_json()
                    job_data['file_hash'] = current_hash
                    save_json('job', job_data)
                    
                    _display_job_overview()
                    status_container.empty()
                
        except ValueError as e:
            st.error(str(e))
            st.session_state.job_parsing = False
        except Exception as e:
            st.error(f"Error processing job description: {str(e)}")
            st.session_state.job_parsing = False

def _handle_job_description_text() -> None:
    """Handle pasted job description text."""
    job_text = st.text_area(
        "Paste job description",
        height=300,
        placeholder="Paste the job description here..."
    )
    
    if job_text and st.button("Analyze Job Description"):
        try:
            current_hash = _compute_file_hash(job_text.encode())
            
            # Check if we've already parsed this text
            job_data = load_json('job')
            if job_data and job_data.get('text_hash') == current_hash:
                return
                
            st.session_state.job_parsing = True
            
            # Use st.spinner in a separate container to avoid blocking
            status_container = st.empty()
            with status_container:
                with st.spinner("Analyzing job description..."):
                    # Run async parsing in a background task
                    job_obj = asyncio.run(_parse_content(job_text, 'job_parser'))
                    set_job_description(job_obj)
                    
                    # Save to file
                    job_data = job_obj.model_dump_json()
                    job_data['text_hash'] = current_hash
                    save_json('job', job_data)
                    
                    _display_job_overview()
                    status_container.empty()
                
        except Exception as e:
            st.error(f"Error analyzing job description: {str(e)}")
            st.session_state.job_parsing = False

def _display_resume_overview() -> None:
    """Display the parsed resume overview."""
    resume = get_resume()
    if not resume:
        return
        
    st.success("Resume parsed successfully!")
    render_action_card(
        title="Resume Overview",
        description=_get_resume_overview_text(resume)
    )

def _display_job_overview() -> None:
    """Display the parsed job description overview."""
    job = get_job_description()
    if not job:
        return
        
    st.success("Job description parsed successfully!")
    render_action_card(
        title="Job Overview",
        description=_get_job_overview_text(job)
    )

def _get_resume_overview_text(resume: Resume) -> str:
    """Get formatted text for resume overview.
    
    :param resume: The Resume object to format
    :type resume: Resume
    :return: Formatted overview text
    :rtype: str
    """
    return f"""
    Name: {resume.contact_info.name}
    Email: {resume.contact_info.email}
    Skills: {', '.join(resume.skills[:5])}...
    """

def _get_job_overview_text(job: JobDescription) -> str:
    """Get formatted text for job overview.
    
    :param job: The JobDescription object to format
    :type job: JobDescription
    :return: Formatted overview text
    :rtype: str
    """
    return f"""
    Title: {job.title}
    Company: {job.company_name}
    Location: {job.location}
    Required Skills: {', '.join(tech.tech_type for tech in job.tech_stack if tech.priority == 'required')}
    Nice-to-have Skills: {', '.join(tech.tech_type for tech in job.tech_stack if tech.priority == 'nice_to_have')}
    """