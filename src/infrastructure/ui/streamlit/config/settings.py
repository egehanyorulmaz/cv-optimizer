"""Page configuration settings for the Streamlit application."""

import streamlit as st

def setup_page_config():
    """Configure the main page settings."""
    st.set_page_config(
        page_title="CV Optimizer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/egehanyorulmaz/cv-optimizer',
            'Report a bug': "https://github.com/egehanyorulmaz/cv-optimizer/issues",
            'About': "# CV Optimizer\nIntelligent resume enhancement system."
        }
    ) 