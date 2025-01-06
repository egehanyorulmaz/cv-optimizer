"""
Main Streamlit application for CV Optimizer.

This module serves as the entry point for the Streamlit UI, providing access to various
CV optimization functionalities through a user-friendly interface.
"""

import streamlit as st
from src.infrastructure.ui.streamlit.state.session import initialize_session_state
from src.infrastructure.ui.streamlit.config.settings import setup_page_config
from src.infrastructure.ui.streamlit.components.sidebar import render_sidebar
from src.infrastructure.ui.streamlit.components.input import render_input_section
from src.infrastructure.ui.streamlit.core.resources import SharedResources

class StreamlitApp:
    """Main Streamlit application class managing resources and UI."""
    
    def __init__(self):
        """Initialize the application and its resources."""
        self.resources = SharedResources.get_instance()
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize and store services in session state."""
        if 'services' not in st.session_state:
            st.session_state.services = {
                'ai_provider': self.resources.ai_provider.get_resource(),
                'template_service': self.resources.template_service.get_resource(),
                'resume_parser': self.resources.resume_parser.get_resource(),
                'job_parser': self.resources.job_parser.get_resource()
            }
    
    def run(self):
        """Run the Streamlit application."""
        setup_page_config()
        initialize_session_state()
        self.render_ui()
    
    def render_ui(self):
        """Render the main UI components."""
        render_sidebar()
        
        tabs = st.tabs(["Input", "Analysis", "Optimization"])
        
        with tabs[0]:
            render_input_section()

if __name__ == "__main__":
    app = StreamlitApp()
    app.run() 