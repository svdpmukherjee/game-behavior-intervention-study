"""
Results view module.
Contains functions for displaying the final results view.
"""

import streamlit as st
from utils.helpers import export_messages_to_file
from workflow.state_manager import save_results_to_file, reset_session_state

def display_results_view():
    """Display the final results view."""
    if 'workflow' not in st.session_state or not st.session_state.workflow.final_messages:
        st.error("No results to display. Please complete the workflow first.")
        st.session_state.current_view = "setup"
        st.rerun()
        return
    
    workflow = st.session_state.workflow
    
    with st.container(border=True):
        st.markdown('<div class="sub-header">Workflow Complete! 🎉</div>', unsafe_allow_html=True)
        st.success(f"You've successfully generated {len(workflow.final_messages)} messages for the {workflow.concept_name} concept!")
        
        # Display iterations summary
        if workflow.iterations_per_message:
            iterations_data = [{"message": i+1, "iterations": count} for i, count in enumerate(workflow.iterations_per_message)]
            st.text(f"Total iterations: {sum(workflow.iterations_per_message)}")
    
    # Display workflow parameters
    with st.container(border=True):
        st.markdown('<div class="section-header">Workflow Parameters</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Concept Information**")
            st.markdown(f"- **Concept:** {workflow.concept_name}")
            st.markdown(f"- **Task Context:** {workflow.context[:100]}...")
        
        with col2:
            st.markdown("**Message Parameters**")
            st.markdown(f"- **Focus:** {workflow.diversity_focus}")
            st.markdown(f"- **Tone:** {workflow.tone}")
            st.markdown(f"- **Style:** {workflow.message_style.split(' ')[-1] if workflow.message_style else 'Default'}")
    
    # Display final messages
    with st.container(border=True):
        st.markdown('<div class="section-header">Final Messages</div>', unsafe_allow_html=True)
        
        for i, message in enumerate(workflow.final_messages, 1):
            st.markdown(f"**Message {i}**")
            st.markdown(f'<div class="message-box">{message}</div>', unsafe_allow_html=True)
    
    # Export options
    with st.container(border=True):
        st.markdown('<div class="section-header">Export Results</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Messages as Text", type="primary", use_container_width=True, key="export_text_btn"):
                export_path = export_messages_to_file(workflow.final_messages, workflow.concept_name)
                if export_path:
                    st.success(f"Messages exported to: {export_path}")
                else:
                    st.error("Failed to export messages.")
        
        with col2:
            if st.button("Save Complete Results", type="secondary", use_container_width=True, key="save_results_btn"):
                save_path = save_results_to_file()
                if save_path:
                    st.success(f"Results saved to: {save_path}")
                else:
                    st.error("Failed to save results.")
        
        # Start new workflow button
        if st.button("Start New Workflow", type="primary", use_container_width=True, key="new_workflow_results_btn"):
            reset_session_state()
            st.rerun()