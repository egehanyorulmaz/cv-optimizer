"""
Skills Analysis page for CV Optimizer.

This module provides the UI for analyzing skill relationships and trends.
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from src.core.domain.skill_relationship import SkillRelationship

def show_skills_analysis():
    """
    Display the skills analysis interface.
    """
    st.title("Skills Analysis")
    
    # Get skills from resume if available
    resume_skills = []
    if st.session_state.get('resume_obj'):
        resume_skills = st.session_state.resume_obj.skills
    
    # Skill Input
    st.subheader("🎯 Core Skills")
    
    # Option to use resume skills
    use_resume_skills = False
    if resume_skills:
        use_resume_skills = st.checkbox("Use skills from my resume", value=True)
    
    if use_resume_skills and resume_skills:
        skills = resume_skills
        st.info(f"Using skills from your resume: {', '.join(skills)}")
    else:
        skill_input = st.text_input(
            "Enter your core skills (comma-separated)",
            help="Example: Python, Machine Learning, Data Analysis"
        )
        skills = [s.strip() for s in skill_input.split(",")] if skill_input else []
    
    if skills:
        if st.button("Analyze Skills"):
            with st.spinner("Analyzing skill relationships..."):
                try:
                    # Create skill relationship analyzer
                    skill_analyzer = SkillRelationship(skills)
                    
                    # Get related skills and relationships
                    analysis = skill_analyzer.analyze()
                    
                    # Create tabs for different analyses
                    related_tab, graph_tab, trends_tab, resources_tab = st.tabs([
                        "Related Skills", "Skill Graph", "Industry Trends", "Learning Resources"
                    ])
                    
                    # Display Related Skills
                    with related_tab:
                        if analysis.related_skills:
                            col1, col2 = st.columns(2)
                            skills_sorted = sorted(
                                analysis.related_skills.items(),
                                key=lambda x: x[1],
                                reverse=True
                            )
                            mid = len(skills_sorted) // 2
                            
                            with col1:
                                for skill, relevance in skills_sorted[:mid]:
                                    st.metric(skill, f"{relevance:.1f}% relevance")
                            
                            with col2:
                                for skill, relevance in skills_sorted[mid:]:
                                    st.metric(skill, f"{relevance:.1f}% relevance")
                        else:
                            st.info("No related skills found.")
                    
                    # Display Skill Graph
                    with graph_tab:
                        if analysis.skill_graph:
                            # Create graph visualization
                            G = nx.Graph()
                            
                            # Add nodes and edges
                            for skill in skills:
                                G.add_node(skill, node_type="core")
                            for skill, related in analysis.skill_graph.items():
                                for related_skill, weight in related.items():
                                    G.add_edge(skill, related_skill, weight=weight)
                            
                            # Create plot
                            plt.figure(figsize=(12, 8))
                            pos = nx.spring_layout(G, k=1, iterations=50)
                            
                            # Draw the graph
                            nx.draw(G, pos,
                                   with_labels=True,
                                   node_color='lightblue',
                                   node_size=2000,
                                   font_size=8,
                                   font_weight='bold',
                                   edge_color='gray',
                                   width=1,
                                   alpha=0.7)
                            
                            # Display the plot
                            st.pyplot(plt)
                        else:
                            st.info("No skill relationships to visualize.")
                    
                    # Display Industry Trends
                    with trends_tab:
                        if analysis.industry_trends:
                            for trend in analysis.industry_trends:
                                st.info(f"📈 {trend}")
                        else:
                            st.info("No industry trends available.")
                    
                    # Display Learning Resources
                    with resources_tab:
                        if analysis.learning_resources:
                            for resource in analysis.learning_resources:
                                st.write(f"📚 {resource}")
                        else:
                            st.info("No learning resources available.")
                    
                except Exception as e:
                    st.error(f"Error analyzing skills: {str(e)}")
    else:
        st.warning("Please enter at least one skill to analyze.")

if __name__ == "__main__":
    show_skills_analysis() 