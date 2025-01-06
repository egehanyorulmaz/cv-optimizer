"""Session state management for the Streamlit application.

This module handles the initialization and management of session state variables
across the Streamlit application.
"""

import streamlit as st
from typing import Optional, Dict, Any
from src.core.domain.resume import Resume
from src.core.domain.job_description import JobDescription

def initialize_session_state():
    """Initialize all session state variables for the application.
    
    This function ensures all necessary session state variables are properly
    initialized when the application starts or reloads.
    """
    _init_content_states()
    _init_object_states()
    _init_processing_states()
    _init_analysis_states()
    _init_service_states()

def _init_content_states():
    """Initialize content-related session states."""
    if 'resume_content' not in st.session_state:
        st.session_state.resume_content = None
    if 'job_content' not in st.session_state:
        st.session_state.job_content = None

def _init_object_states():
    """Initialize parsed object states."""
    if 'resume_obj' not in st.session_state:
        st.session_state.resume_obj = None
    if 'job_obj' not in st.session_state:
        st.session_state.job_obj = None

def _init_processing_states():
    """Initialize processing flag states."""
    if 'resume_parsing' not in st.session_state:
        st.session_state.resume_parsing = False
    if 'job_parsing' not in st.session_state:
        st.session_state.job_parsing = False
    if 'analyzing' not in st.session_state:
        st.session_state.analyzing = False

def _init_analysis_states():
    """Initialize analysis result states."""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'optimization_suggestions' not in st.session_state:
        st.session_state.optimization_suggestions = None

def _init_service_states():
    """Initialize shared service instances."""
    if 'services' not in st.session_state:
        st.session_state.services = {}

def get_resume() -> Optional[Resume]:
    """Get the current resume object from session state.

    :return: The current Resume object if it exists, None otherwise
    :rtype: Resume or None
    """
    return st.session_state.get('resume_obj')

def get_job_description() -> Optional[JobDescription]:
    """Get the current job description object from session state.

    :return: The current JobDescription object if it exists, None otherwise
    :rtype: JobDescription or None
    """
    return st.session_state.get('job_obj')

def get_analysis_results() -> Optional[Dict[str, Any]]:
    """Get the current analysis results from session state.

    :return: The current analysis results if they exist, None otherwise
    :rtype: dict or None
    """
    return st.session_state.get('analysis_results')

def get_service(service_name: str) -> Optional[Any]:
    """Get a shared service instance from session state.

    :param service_name: Name of the service to retrieve
    :type service_name: str
    :return: The requested service instance if it exists, None otherwise
    :rtype: Any or None
    """
    return st.session_state.services.get(service_name)

def set_resume(resume: Resume) -> None:
    """Set the resume object in session state.

    :param resume: The Resume object to store
    :type resume: Resume
    """
    st.session_state.resume_obj = resume
    st.session_state.resume_parsing = False

def set_job_description(job: JobDescription) -> None:
    """Set the job description object in session state.

    :param job: The JobDescription object to store
    :type job: JobDescription
    """
    st.session_state.job_obj = job
    st.session_state.job_parsing = False

def set_service(service_name: str, service_instance: Any) -> None:
    """Store a shared service instance in session state.

    :param service_name: Name to identify the service
    :type service_name: str
    :param service_instance: The service instance to store
    :type service_instance: Any
    """
    st.session_state.services[service_name] = service_instance

def clear_analysis_states() -> None:
    """Clear all analysis-related states."""
    st.session_state.analysis_results = None
    st.session_state.optimization_suggestions = None
    st.session_state.analyzing = False