"""
Change focus view module.
Contains functions for displaying the change message focus view.
"""

import streamlit as st
from ui.common import get_custom_focuses, get_custom_styles

def display_change_focus_view():
    """Display view for changing message focus and style."""
    if 'workflow' not in st.session_state:
        st.error("Workflow not initialized. Please set up the workflow first.")
        st.session_state.current_view = "setup"
        st.rerun()
        return
    
    workflow = st.session_state.workflow
    
    with st.container(border=True):
        st.markdown('<div class="sub-header">Change Message Parameters</div>', unsafe_allow_html=True)
        st.markdown(f"For Message #{workflow.current_message_number} of the {workflow.concept_name} workflow")
        
        # Create separate containers for each parameter with clear boundaries
        
        # Message Focus Section
        with st.container(border=True):
            st.markdown('<div class="parameter-header">Message Focus</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Select the specific aspect of the concept to emphasize in your message</div>', unsafe_allow_html=True)
            
            # Get custom focuses
            custom_focuses = get_custom_focuses()
            
            # Find current focus in custom focuses
            current_focus_text = workflow.diversity_focus
            current_focus_id = next((focus["id"] for focus in custom_focuses if focus["text"] == current_focus_text), custom_focuses[0]["id"] if custom_focuses else None)
            
            # Get the list of focus IDs
            focus_ids = [focus["id"] for focus in custom_focuses]
            
            # Create selection box for new focus
            new_focus_id = st.selectbox(
                "Select New Message Focus",
                options=focus_ids,
                index=focus_ids.index(current_focus_id) if current_focus_id in focus_ids else 0,
                key="new_focus_select"
            )
            
            # Get the text of the selected focus
            new_focus_text = next((focus["text"] for focus in custom_focuses if focus["id"] == new_focus_id), "")
            
            # Display the full text of the selected focus
            st.text_area(
                "Focus Description",
                value=new_focus_text,
                height=100,
                disabled=True,
                key="new_focus_full_text"
            )
        
        # Message Style Section
        with st.container(border=True):
            st.markdown('<div class="parameter-header">Message Style</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Select the structural format for your message</div>', unsafe_allow_html=True)
            
            # Get custom styles
            custom_styles = get_custom_styles()
            
            # Find current style in custom styles
            current_style_text = workflow.message_style
            current_style_id = next((style["id"] for style in custom_styles if style["text"] == current_style_text), custom_styles[0]["id"] if custom_styles else None)
            
            # Get the list of style IDs
            style_ids = [style["id"] for style in custom_styles]
            
            # Create selection box for new style
            new_style_id = st.selectbox(
                "Select New Message Style",
                options=style_ids,
                index=style_ids.index(current_style_id) if current_style_id in style_ids else 0,
                key="new_style_select"
            )
            
            # Get the text of the selected style
            new_style_text = next((style["text"] for style in custom_styles if style["id"] == new_style_id), "")
            
            # Display the full text of the selected style
            st.text_area(
                "Style Description",
                value=new_style_text,
                height=70,
                disabled=True,
                key="new_style_full_text"
            )
        
        # Message Length Section
        with st.container(border=True):
            st.markdown('<div class="parameter-header">Message Length</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Adjust the number of sentences in your generated message</div>', unsafe_allow_html=True)
            
            current_length = getattr(workflow, "message_length", 3)
            new_message_length = st.slider(
                "Number of Sentences",
                min_value=1,
                max_value=8,
                value=current_length,
                step=1,
                help="Select the desired length of the generated message in sentences",
                key="change_message_length_slider"
            )
            
            # Add visual indicator for length classification
            length_category = "Short" if new_message_length <= 2 else ("Medium" if new_message_length <= 5 else "Long")
            st.markdown(f'<div class="length-indicator">Length Category: <span class="length-{length_category.lower()}">{length_category}</span> ({new_message_length} sentences)</div>', unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown('<div class="action-buttons-section"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Confirm & Generate", type="primary", use_container_width=True, key="confirm_new_params_btn"):
                workflow.diversity_focus = new_focus_text
                workflow.message_style = new_style_text
                workflow.message_length = new_message_length
                
                # Move to generation view
                st.session_state.current_view = "generation"
                st.rerun()
        
        with col2:
            if st.button("Cancel", type="secondary", use_container_width=True, key="cancel_focus_change_btn"):
                st.session_state.current_view = "next_message"
                st.rerun()