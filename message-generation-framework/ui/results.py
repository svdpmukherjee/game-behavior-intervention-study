"""
Results view module.
Contains functions for displaying the final results view.
"""

import streamlit as st
import base64
import json
from datetime import datetime
from workflow.state_manager import save_results_to_file, reset_session_state

def export_messages_as_text(messages, concept_name):
    """
    Export messages as a text file and create a download link.
    
    Args:
        messages: List of messages to export
        concept_name: Name of the concept for filename
        
    Returns:
        HTML for download link
    """
    if not messages:
        return None
    
    # Create content
    content = ""
    for i, message in enumerate(messages, 1):
        content += f"Message {i}:\n{message}\n\n"
    
    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{concept_name}_messages_{timestamp}.txt"
    
    # Create download link
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Messages as Text</a>'
    
    return href

def display_results_view():
    """Display the final results view."""
    if 'workflow' not in st.session_state or not st.session_state.workflow.final_messages:
        st.error("No results to display. Please complete the workflow first.")
        st.session_state.current_view = "setup"
        st.rerun()
        return
    
    workflow = st.session_state.workflow
    
    with st.container(border=True):
        # st.markdown('<div class="sub-header">Workflow Complete!</div>', unsafe_allow_html=True)
        st.success(f"You have successfully generated {len(workflow.final_messages)} message(s) for the {workflow.concept_name} concept! The generated message is stored in our database.")
        
        # Display iterations summary
        if workflow.iterations_per_message:
            iterations_data = [{"message": i+1, "iterations": count} for i, count in enumerate(workflow.iterations_per_message)]
            st.text(f"Total iterations: {sum(workflow.iterations_per_message)}")
    
    # Display workflow parameters
    # with st.container(border=True):
    #     st.markdown('<div class="section-header">Context and Parameters Used for This Concept</div>', unsafe_allow_html=True)
        
    #     col1, col2 = st.columns(2)
        
    #     with col1:
    #         # st.markdown("**Concept Information**")
    #         st.markdown(f"- **Concept:** {workflow.concept_name}")
    #         st.markdown(f"- **Task Context:** {workflow.context[:100]}...")
        
    #     with col2:
    #         st.markdown("**Message Parameters**")
    #         st.markdown(f"- **Focus:** {workflow.diversity_focus}")
    #         st.markdown(f"- **Tone:** {workflow.tone}")
    #         st.markdown(f"- **Style:** {workflow.message_style}")
    
    # Display final messages
    with st.container(border=True):
        st.markdown('<div class="section-header">Message(s) Generated for the Concept</div>', unsafe_allow_html=True)
        
        for i, message in enumerate(workflow.final_messages, 1):
            # st.markdown(f"**Message {i}**")
            st.markdown(f'<div class="message-box">{message}</div>', unsafe_allow_html=True)
        # Start new workflow button
        if st.button("Move to the Next Concept", type="primary", use_container_width=True, key="new_workflow_results_btn"):
            reset_session_state()
            st.rerun()
    
    # Export options
    # with st.container(border=True):
    #     st.markdown('<div class="section-header">Export Results</div>', unsafe_allow_html=True)
        
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     if st.button("Export Messages as Text", type="primary", use_container_width=True, key="export_text_btn"):
        #         # Create download link for messages as text
        #         download_link = export_messages_as_text(workflow.final_messages, workflow.concept_name)
        #         if download_link:
        #             st.markdown(download_link, unsafe_allow_html=True)
        #         else:
        #             st.error("Failed to create download link for messages.")
        
        # with col2:
        #     if st.button("Save Complete Results", type="secondary", use_container_width=True, key="save_results_btn"):
        #         # Save complete results and provide download link
        #         save_path = save_results_to_file()
        #         if save_path:
        #             st.success("Results prepared for download.")
        #         else:
        #             st.error("Failed to prepare results for download.")
        
