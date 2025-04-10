"""
Next message view module.
Contains functions for displaying options for the next message.
"""

import streamlit as st
from workflow.state_manager import save_results_to_file, reset_session_state

def display_next_message_view():
    """Display options for the next message."""
    if 'workflow' not in st.session_state:
        st.error("Workflow not initialized. Please set up the workflow first.")
        st.session_state.current_view = "setup"
        st.rerun()
        return
    
    workflow = st.session_state.workflow
    
    with st.container(border=True):
        st.markdown('<div class="sub-header">Message Accepted</div>', unsafe_allow_html=True)
        st.success(f"Message #{workflow.current_message_number - 1} has been finalized!")
        
        # Display accepted message
        st.markdown('<div class="message-box">' + workflow.final_messages[-1] + '</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Choose How to Proceed</div>', unsafe_allow_html=True)
        
        # Options for the next message
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Use Same Parameters", type="primary", use_container_width=True, key="use_same_params_btn"):
                # Keep the same parameters, move to generation view
                st.session_state.current_view = "generation"
                st.rerun()
        
        with col2:
            if st.button("Change Message Parameters", type="secondary", use_container_width=True, key="new_params_btn"):
                # Show parameter selection
                st.session_state.current_view = "change_focus"
                st.rerun()
        
        # Show previously generated messages
        if len(workflow.final_messages) > 1:
            with st.expander("View Previous Messages", expanded=False):
                for i, msg in enumerate(workflow.final_messages[:-1], 1):
                    st.markdown(f"**Message {i}**")
                    st.markdown(f'<div class="message-box">{msg}</div>', unsafe_allow_html=True)
        
        # Option to start completely new
        if st.button("Start New Workflow", use_container_width=True, key="start_new_workflow_btn"):
            if st.session_state.get("confirm_new"):
                # Save current results
                save_results_to_file()
                
                # Reset session state
                reset_session_state()
                st.rerun()
            else:
                st.session_state.confirm_new = True
                st.warning("Click again to confirm. Current messages will be saved, but you'll start a new workflow.")