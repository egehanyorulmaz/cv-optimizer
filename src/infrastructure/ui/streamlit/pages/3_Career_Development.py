"""
Career Development page for CV Optimizer.

This module provides the UI for career development suggestions and planning.
"""

import streamlit as st
from src.core.domain.career_development import CareerDevelopment

def show_career_development():
    """
    Display the career development interface.
    """
    st.title("Career Development")
    
    if not st.session_state.get('resume_obj'):
        st.warning("Please provide your resume in the home page first.")
        return
    
    resume = st.session_state.resume_obj
    
    # Career Goals
    st.subheader("🎯 Career Goals")
    col1, col2 = st.columns(2)
    
    with col1:
        target_role = st.text_input("What is your target role?")
    with col2:
        target_industry = st.text_input("What industry are you targeting?")
    
    # Experience Level
    experience_level = st.selectbox(
        "What is your current experience level?",
        ["Entry Level", "Mid Level", "Senior Level", "Lead/Manager", "Executive"]
    )
    
    if st.button("Get Career Advice"):
        with st.spinner("Analyzing career path..."):
            try:
                # Create career development instance
                career_dev = CareerDevelopment(
                    current_role=resume.current_role,
                    target_role=target_role,
                    target_industry=target_industry,
                    experience_level=experience_level,
                    skills=resume.skills
                )
                
                # Get career advice
                advice = career_dev.get_career_advice()
                
                # Create tabs for different types of advice
                career_tab, skills_tab, certs_tab, other_tab = st.tabs([
                    "Career Path", "Skill Gaps", "Certifications", "Additional Advice"
                ])
                
                # Display Career Path
                with career_tab:
                    if advice.career_path:
                        for i, step in enumerate(advice.career_path, 1):
                            st.write(f"{i}. {step}")
                    else:
                        st.info("No specific career path recommendations available.")
                
                # Display Skill Gaps
                with skills_tab:
                    if advice.skill_gaps:
                        for skill in advice.skill_gaps:
                            st.warning(f"📊 {skill}")
                    else:
                        st.success("No critical skill gaps identified!")
                
                # Display Certifications
                with certs_tab:
                    if advice.recommended_certifications:
                        for cert in advice.recommended_certifications:
                            st.info(f"📜 {cert}")
                    else:
                        st.info("No specific certifications recommended at this time.")
                
                # Display Additional Recommendations
                with other_tab:
                    if advice.additional_recommendations:
                        for rec in advice.additional_recommendations:
                            st.write(f"💡 {rec}")
                    else:
                        st.info("No additional recommendations at this time.")
                
            except Exception as e:
                st.error(f"Error generating career advice: {str(e)}")

if __name__ == "__main__":
    show_career_development() 