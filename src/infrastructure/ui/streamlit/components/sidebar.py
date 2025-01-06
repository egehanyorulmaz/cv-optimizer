"""Sidebar components for the Streamlit application."""

import streamlit as st

def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        _render_app_info()
        _render_settings()
        _render_export_options()

def _render_app_info():
    """Render application information in sidebar."""
    st.title("CV Optimizer")
    st.markdown("""
    Optimize your resume with AI-powered analysis and suggestions.
    
    ### Features
    - 📄 Resume Analysis
    - 🎯 Job Matching
    - ✨ Content Optimization
    - 🤖 ATS Compatibility
    """)

def _render_settings():
    """Render application settings in sidebar."""
    st.subheader("Settings")
    
    with st.expander("Analysis Settings"):
        st.checkbox("Enable detailed analysis", value=True)
        st.checkbox("Include AI suggestions", value=True)
        st.select_slider(
            "Analysis depth",
            options=["Basic", "Standard", "Detailed"],
            value="Standard"
        )
    
    with st.expander("Privacy Settings"):
        st.checkbox("Enable PII detection", value=True)
        st.checkbox("Anonymize personal data", value=False)

def _render_export_options():
    """Render export options in sidebar."""
    st.subheader("Export Options")
    
    if st.session_state.get('resume_obj'):
        col1, col2 = st.columns(2)
        with col1:
            st.button("Export Analysis", key="export_analysis")
        with col2:
            st.button("Export Resume", key="export_resume")
    else:
        st.info("Upload a resume to enable export options") 