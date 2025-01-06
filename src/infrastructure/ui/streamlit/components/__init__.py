"""Shared UI components for the Streamlit application."""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

def render_skill_radar(skills: Dict[str, float], title: str = "Skill Analysis"):
    """Render a radar chart for skills analysis."""
    categories = list(skills.keys())
    values = list(skills.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=title
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_progress_metrics(metrics: Dict[str, float]):
    """Render multiple progress metrics in columns."""
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        with col:
            st.metric(label, f"{value:.1f}%")
            st.progress(value / 100)

def render_action_card(title: str, description: str, actions: List[Dict[str, Any]] = None):
    """Render a card with title, description, and optional actions."""
    with st.container():
        st.subheader(title)
        st.write(description)
        
        if actions:
            cols = st.columns(len(actions))
            for col, action in zip(cols, actions):
                with col:
                    if st.button(action['label'], key=action.get('key')):
                        action['callback']()
