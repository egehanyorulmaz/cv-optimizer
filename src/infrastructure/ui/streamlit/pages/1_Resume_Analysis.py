"""
Resume Analysis page for CV Optimizer.

This module provides the UI for resume analysis functionality.
"""

import streamlit as st
from src.infrastructure.ui.streamlit.components import (
    render_skill_radar,
    render_timeline,
    render_action_card
)

def show_resume_analysis():
    """
    Display the resume analysis interface.
    """
    st.title("Resume Analysis")
    
    if not st.session_state.get('resume_obj'):
        st.warning("Please provide your resume in the home page first.")
        return
    
    resume = st.session_state.resume_obj
    
    # Create tabs for different sections
    overview_tab, skills_tab, experience_tab, education_tab = st.tabs([
        "Overview", "Skills Analysis", "Experience", "Education"
    ])
    
    with overview_tab:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Personal Information")
            render_action_card(
                title=resume.personal_info.get('name', 'Not found'),
                description=f"""
                📧 {resume.personal_info.get('email', 'No email')}
                📱 {resume.personal_info.get('phone', 'No phone')}
                📍 {resume.personal_info.get('location', 'No location')}
                """
            )
        
        with col2:
            st.subheader("Profile Completeness")
            completeness = calculate_profile_completeness(resume)
            st.progress(completeness / 100)
            st.metric("Profile Score", f"{completeness}%")
    
    with skills_tab:
        st.subheader("Skills Analysis")
        if resume.skills:
            # Convert skills to dict with mock scores for visualization
            skill_scores = {skill: 85 for skill in resume.skills}  # Mock scores
            render_skill_radar(skill_scores, "Skill Proficiency")
            
            # Group skills by category
            st.subheader("Skills by Category")
            col1, col2 = st.columns(2)
            with col1:
                st.write("💻 Technical Skills")
                for skill in resume.technical_skills:
                    st.write(f"• {skill}")
            with col2:
                st.write("🤝 Soft Skills")
                for skill in resume.soft_skills:
                    st.write(f"• {skill}")
        else:
            st.info("No skills found in your resume. Consider adding relevant skills to enhance your profile.")
    
    with experience_tab:
        st.subheader("Professional Experience")
        if resume.experience:
            # Convert experience to timeline format
            experience_timeline = [
                {
                    'date': exp.get('date', 'No date'),
                    'title': exp.get('title', 'No title'),
                    'description': exp.get('description', 'No description')
                }
                for exp in resume.experience
            ]
            render_timeline(experience_timeline)
        else:
            st.info("No professional experience found in your resume.")
    
    with education_tab:
        st.subheader("Education History")
        if resume.education:
            for edu in resume.education:
                render_action_card(
                    title=edu.get('degree', 'Degree'),
                    description=f"""
                    🏫 {edu.get('institution', 'Institution')}
                    📅 {edu.get('date', 'Date')}
                    📊 {edu.get('gpa', 'GPA not specified')}
                    """
                )
        else:
            st.info("No education history found in your resume.")

def calculate_profile_completeness(resume) -> float:
    """
    Calculate the completeness score of the resume profile.
    
    :param resume: Resume object
    :return: Completeness score (0-100)
    """
    score = 0
    total_checks = 5
    
    # Basic info check
    if resume.personal_info.get('name'): score += 1
    if resume.personal_info.get('email'): score += 1
    
    # Skills check
    if resume.skills: score += 1
    
    # Experience check
    if resume.experience: score += 1
    
    # Education check
    if resume.education: score += 1
    
    return (score / total_checks) * 100

if __name__ == "__main__":
    show_resume_analysis() 