"""
Job Matching page for CV Optimizer.

This module provides the UI for matching resumes against job descriptions.
"""

import streamlit as st
from src.core.domain.resume_match import ResumeMatcher
from src.infrastructure.ui.streamlit.components import (
    render_skill_match_comparison,
    render_progress_metrics,
    render_action_card
)

def show_job_matching():
    """
    Display the job matching interface.
    """
    st.title("Job Description Matching")
    
    if not st.session_state.get('resume_obj') or not st.session_state.get('job_obj'):
        st.warning("Please provide both your resume and job description in the home page first.")
        return
    
    # Display job details
    job = st.session_state.job_obj
    render_action_card(
        title=job.title,
        description=f"""
        🏢 Company: {job.company}
        📍 Location: {job.location}
        💼 Experience Level: {job.experience_level}
        """
    )
    
    if st.button("Analyze Match"):
        with st.spinner("Analyzing match..."):
            try:
                # Create matcher instance
                matcher = ResumeMatcher()
                
                # Get match results
                match_result = matcher.match(
                    st.session_state.resume_content,
                    st.session_state.job_obj
                )
                
                # Create tabs for different analyses
                overview_tab, skills_tab, recommendations_tab = st.tabs([
                    "Match Overview", "Skills Analysis", "Recommendations"
                ])
                
                with overview_tab:
                    st.subheader("Match Analysis")
                    
                    # Display key metrics
                    metrics = {
                        "Overall Match": match_result.match_score,
                        "Skills Match": match_result.skills_match_score,
                        "Experience Match": match_result.experience_match_score,
                        "Education Match": match_result.education_match_score
                    }
                    render_progress_metrics(metrics)
                    
                    # Display key strengths and gaps
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🎯 Key Strengths")
                        for strength in match_result.key_strengths:
                            st.success(strength)
                    
                    with col2:
                        st.subheader("🎯 Areas to Improve")
                        for gap in match_result.key_gaps:
                            st.warning(gap)
                
                with skills_tab:
                    st.subheader("Skills Analysis")
                    render_skill_match_comparison(
                        matched_skills=match_result.matched_skills,
                        missing_skills=match_result.missing_skills,
                        partial_matches=match_result.partial_matches
                    )
                
                with recommendations_tab:
                    st.subheader("💡 Optimization Recommendations")
                    
                    # Group recommendations by category
                    for category, recs in match_result.recommendations.items():
                        st.write(f"### {category}")
                        for rec in recs:
                            render_action_card(
                                title=rec.title,
                                description=rec.description,
                                action_button="Apply Suggestion" if rec.can_apply else None
                            )
                
            except Exception as e:
                st.error(f"Error during matching: {str(e)}")

if __name__ == "__main__":
    show_job_matching() 