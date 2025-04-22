"""
Setup view module.
Contains functions for displaying the workflow setup view.
"""

import streamlit as st
from data.concepts import ALL_conceptS
from workflow.state_manager import initialize_workflow, get_available_models
from ui.common import (
    get_custom_contexts, get_custom_focuses, get_custom_tones, get_custom_styles,
    add_task_context, add_message_focus, add_message_tone, add_message_style,
    delete_task_context, delete_message_focus, delete_message_tone, delete_message_style
)
from datetime import datetime

def display_setup_view():
    """Display the workflow setup view."""
    # Group concepts by theory
    concepts_by_theory = {}
    for concept in ALL_conceptS:
        theory = ALL_conceptS[concept]["theory"]
        if theory not in concepts_by_theory:
            concepts_by_theory[theory] = []
        concepts_by_theory[theory].append(concept)
    
    # 1. concept Selection
    with st.container(border=True):
        st.markdown('<div class="section-header">1. Select Psychological concept</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-explanation">Choose a psychological concept from one of the available theories. '
            'Each concept represents a specific psychological concept that you want to communicate through your message.</div>',
            unsafe_allow_html=True
        )
        
        # Create a friendly dropdown with theory grouping
        concept_options = []
        for theory, concepts in concepts_by_theory.items():
            for concept in sorted(concepts):
                concept_options.append(f"{concept} ({theory})")
        
        # Two-column layout for concept selection
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_concept_full = st.selectbox(
                "Concept",
                options=concept_options,
                help="The psychological concept for which to generate messages",
                key="concept_selector"
            )
        
        # Extract concept name from the selected option
        selected_concept = selected_concept_full.split(" (")[0] if selected_concept_full else ""
        
        with col2:
            if selected_concept:
                # Show concept description with edit option
                concept_info = ALL_conceptS.get(selected_concept, {})
                original_description = concept_info.get("description", "")
                
                # Get or set the custom definition in session state
                custom_def_key = f"custom_definition_{selected_concept}"
                if custom_def_key not in st.session_state:
                    st.session_state[custom_def_key] = original_description
                
                # Display editable definition
                edited_description = st.text_area(
                    "Concept Definition (Editable Text)",
                    value=st.session_state[custom_def_key],
                    height=100,
                    key=f"edit_def_{selected_concept}"
                )
                
                if st.button("Save Edited Definition", key="save_definition_btn"):
                    st.session_state[custom_def_key] = edited_description
                    st.success("Definition updated!")
    
    # 2. Task Context
    with st.container(border=True):
        st.markdown('<div class="section-header">2. Select Task Context</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-explanation">Choose the situational context in which your message will be delivered. '
            'The context helps frame the message appropriately for the target audience and situation.</div>',
            unsafe_allow_html=True
        )
        
        # Get custom contexts
        custom_contexts = get_custom_contexts()
        
        # Create two-column layout for task context
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Get just the IDs for the selectbox
            context_ids = [ctx["id"] for ctx in custom_contexts]
            selected_context_id = st.selectbox(
                "Task Context",
                options=context_ids,
                help="The context in which the message will be used",
                key="context_selector"
            )
            
            # Add a button to add new task context
            if st.button("Add New Task Context", key="add_task_btn"):
                st.session_state.show_add_task = True
                st.session_state.auto_expand_task_manager = True  # Auto-expand manager
        
        with col2:
            # Find the selected context
            selected_context_obj = next((ctx for ctx in custom_contexts if ctx["id"] == selected_context_id), None)
            selected_context_text = selected_context_obj["text"] if selected_context_obj else ""
            
            # Display editable context
            edited_context = st.text_area(
                "Task Context Details (Editable Text)",
                value=selected_context_text,
                height=100,
                key="edit_context_text"
            )
            
            # Save button for edited context
            if st.button("Save Edited Context", key="save_context_btn"):
                for ctx in custom_contexts:
                    if ctx["id"] == selected_context_id:
                        ctx["text"] = edited_context
                        st.success("Context updated!")
                        break
        
        # Show manage task contexts expander
        with st.expander("🔧 Manage Task Contexts", expanded=st.session_state.get("auto_expand_task_manager", False)):
            # First show the form to add new task if flag is set
            if st.session_state.get("show_add_task", False):
                add_task_context()
                # Reset the auto expand flag after displaying
                st.session_state.auto_expand_task_manager = False
            
            # Then show delete buttons for contexts
            for ctx in custom_contexts:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.text(ctx["id"])
                with cols[1]:
                    if st.button("Delete", key=f"del_ctx_{ctx['id']}"):
                        delete_task_context(ctx["id"])
    
    # 3. Message Characteristics
    with st.container(border=True):
        st.markdown('<div class="section-header">3. Message Characteristics</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-explanation">Define the specific focus, style, and tone of your message. '
            'The message focus determines what aspect of the concept to emphasize, the style determines the message structure, '
            'while the tone sets the emotional quality and style.</div>',
            unsafe_allow_html=True
        )
        
        # Create separate containers for each message characteristic with visible boundaries
        # 3.1 Message Focus
        with st.container(border=True):
            st.markdown('<div class="parameter-header">3.1 Message Focus</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Select the specific aspect of the concept to emphasize in your message</div>', unsafe_allow_html=True)
            
            # Message focus (formerly diversity focus)
            custom_focuses = get_custom_focuses()
            
            # Modified to show focus text directly in dropdown
            focus_options = [focus["text"] for focus in custom_focuses]
            
            selected_focus_text = st.selectbox(
                "Message Focus",
                options=focus_options,
                help="Specific focus area for the message",
                key="focus_selector"
            )
            
            # Button to add new focus
            if st.button("Add New Message Focus", key="add_focus_btn"):
                st.session_state.show_add_focus = True
                st.session_state.auto_expand_focus_manager = True  # Auto-expand manager
                
            # Show manage message focuses expander
            with st.expander("🔧 Manage Message Focuses", expanded=st.session_state.get("auto_expand_focus_manager", False)):
                # First show the form to add new focus if flag is set
                if st.session_state.get("show_add_focus", False):
                    add_message_focus()
                    # Reset the auto expand flag after displaying
                    st.session_state.auto_expand_focus_manager = False
                
                # Then show delete buttons for focuses
                for focus in custom_focuses:
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.text(focus["id"])
                    with cols[1]:
                        if st.button("Delete", key=f"del_focus_{focus['id']}"):
                            delete_message_focus(focus["id"])
        
        # 3.2 Message Style
        with st.container(border=True):
            st.markdown('<div class="parameter-header">3.2 Message Style</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Select the structural format for your message</div>', unsafe_allow_html=True)
            
            # Message Style
            custom_styles = get_custom_styles()
            
            # Modified to show style text directly in dropdown
            style_options = [style["text"] for style in custom_styles]
            
            selected_style_text = st.selectbox(
                "Message Style",
                options=style_options,
                help="Structural format for the message",
                key="style_selector"
            )
            
            # Button to add new style
            if st.button("Add New Message Style", key="add_style_btn"):
                st.session_state.show_add_style = True
                st.session_state.auto_expand_style_manager = True  # Auto-expand manager
                
            # Show manage message styles expander
            with st.expander("🔧 Manage Message Styles", expanded=st.session_state.get("auto_expand_style_manager", False)):
                # First show the form to add new style if flag is set
                if st.session_state.get("show_add_style", False):
                    add_message_style()
                    # Reset the auto expand flag after displaying
                    st.session_state.auto_expand_style_manager = False
                
                # Then show delete buttons for styles
                for style in custom_styles:
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.text(style["id"])
                    with cols[1]:
                        if st.button("Delete", key=f"del_style_{style['id']}"):
                            delete_message_style(style["id"])
            
        # 3.3 Message Tone
        with st.container(border=True):
            st.markdown('<div class="parameter-header">3.3 Message Tone</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Set the emotional quality and style of your message</div>', unsafe_allow_html=True)
            
            # Tone selection
            custom_tones = get_custom_tones()
            tone_ids = [tone["id"] for tone in custom_tones]
            
            selected_tone_id = st.selectbox(
                "Tone",
                options=tone_ids,
                help="Desired tone for the message",
                key="tone_selector"
            )
            
            # Find the selected tone
            selected_tone_obj = next((tone for tone in custom_tones if tone["id"] == selected_tone_id), None)
            selected_tone_text = selected_tone_obj["text"] if selected_tone_obj else ""
            
            # Display tone description if needed
            st.text_area(
                "Tone Description",
                value=selected_tone_text,
                height=70,
                disabled=False,
                key="tone_full_text"
            )
            
            # Button to add new tone
            if st.button("Add New Tone", key="add_tone_btn"):
                st.session_state.show_add_tone = True
                st.session_state.auto_expand_tone_manager = True  # Auto-expand manager
                
            # Show manage tones expander
            with st.expander("🔧 Manage Tones", expanded=st.session_state.get("auto_expand_tone_manager", False)):
                # First show the form to add new tone if flag is set
                if st.session_state.get("show_add_tone", False):
                    add_message_tone()
                    # Reset the auto expand flag after displaying
                    st.session_state.auto_expand_tone_manager = False
                
                # Then show delete buttons for tones
                for tone in custom_tones:
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.text(tone["id"])
                    with cols[1]:
                        if st.button("Delete", key=f"del_tone_{tone['id']}"):
                            delete_message_tone(tone["id"])
        
        # 3.4 Message Length
        with st.container(border=True):
            st.markdown('<div class="parameter-header">3.4 Message Length</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Adjust the number of sentences in your generated message</div>', unsafe_allow_html=True)
            
            # Add Message Length setting
            message_length = st.slider(
                "Number of Sentences",
                min_value=1,
                max_value=8,
                value=3,
                step=1,
                help="Select the desired length of the generated message in sentences",
                key="message_length_slider"
            )
            
            # Add visual indicator for length classification
            length_category = "Short" if message_length <= 2 else ("Medium" if message_length <= 5 else "Long")
            st.markdown(f'<div class="length-indicator">Length Category: <span class="length-{length_category.lower()}">{length_category}</span> ({message_length} sentences)</div>', unsafe_allow_html=True)
            
        # 3.5 Number of Messages to Generate
        with st.container(border=True):
            st.markdown('<div class="parameter-header">3.5 Number of Messages</div>', unsafe_allow_html=True)
            st.markdown('<div class="parameter-description">Set how many messages you want to generate for this concept</div>', unsafe_allow_html=True)
            
            # Add number of messages setting
            num_messages = st.number_input(
                "Number of Messages",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Select how many messages you want to generate for this concept",
                key="num_messages_input"
            )
    
    # 4. Model Selection
    with st.container(border=True):
        st.markdown('<div class="section-header">4. Model Selection</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-explanation">Choose the AI models for generating and evaluating messages. '
            'Different models have different strengths - some excel at creative writing while others are better at evaluation.</div>',
            unsafe_allow_html=True
        )
        
        # Get available models based on API keys
        available_models = get_available_models()
        
        # Create 2 columns for model selection with nested columns for parameters
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="parameter-header">4.1 Generator Model</div>', unsafe_allow_html=True)
            
            # Flatten available models list for selection
            generator_options = []
            for provider, models in available_models.items():
                for model in models:
                    generator_options.append(model)
            
            if not generator_options:
                st.warning("No models available. Please check your API keys.")
                generator_model = ""
            else:
                generator_model = st.selectbox(
                    "Select Generator Model",
                    options=generator_options,
                    help="Model for generating messages",
                    key="generator_model_select"
                )
            
            # Generator parameters
            st.markdown('<div class="parameter-subheader">Generator Parameters</div>', unsafe_allow_html=True)
            
            # Temperature slider
            generator_temp = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Higher values make output more random, lower values make it more deterministic",
                key="generator_temp_slider"
            )
            
            # Top P slider
            generator_top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=0.95,
                step=0.05,
                help="Controls diversity by limiting to top tokens that add up to probability mass P",
                key="generator_top_p_slider"
            )
        
        with col2:
            st.markdown('<div class="parameter-header">4.2 Evaluator Model</div>', unsafe_allow_html=True)
            
            # Flatten available models list for selection
            evaluator_options = []
            for provider, models in available_models.items():
                for model in models:
                    evaluator_options.append(model)
            
            if not evaluator_options:
                st.warning("No models available. Please check your API keys.")
                evaluator_model = ""
            else:
                # Set default to gpt-4o if available
                default_index = evaluator_options.index("gpt-4o") if "gpt-4o" in evaluator_options else 0
                
                evaluator_model = st.selectbox(
                    "Select Evaluator Model",
                    options=evaluator_options,
                    index=default_index,
                    help="Model for evaluating messages",
                    key="evaluator_model_select"
                )
            
            # Evaluator parameters
            st.markdown('<div class="parameter-subheader">Evaluator Parameters</div>', unsafe_allow_html=True)
            
            # Temperature slider (lower default for evaluation)
            evaluator_temp = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.05,
                help="Lower values recommended for evaluation tasks",
                key="evaluator_temp_slider"
            )
            
            # Top P slider
            evaluator_top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=0.95,
                step=0.05,
                help="Controls diversity by limiting to top tokens that add up to probability mass P",
                key="evaluator_top_p_slider"
            )
            
    # Add MongoDB management section
    with st.container(border=True):
        # st.markdown('<div class="section-header">Database Management</div>', unsafe_allow_html=True)
        # st.markdown(
        #     '<div class="section-explanation">Manage message database settings and operations.</div>',
        #     unsafe_allow_html=True
        # )
        
        if 'mongodb_service' in st.session_state:
            # Get message count
            all_messages = st.session_state.mongodb_service.get_all_messages()
            
            # st.markdown(f"**Current database contains {len(all_messages)} messages**")
            
            st.markdown('<div class="section-header">We Need an User ID</div>', unsafe_allow_html=True)
            user_id = st.session_state.get('user_id', '')
            new_user_id = st.text_input(
                "Enter Your Name (Required) and Press Enter",
                value=user_id,
                help="Enter your first name or username (required to proceed)",
                key="user_id_input"
            )

            # Store user ID in lowercase
            if new_user_id:
                st.session_state.user_id = new_user_id.lower()
            else:
                # st.warning("Please enter a User ID to proceed. This is required for message tracking.")
                pass

            # Add a check for User ID before enabling the Start Workflow button
            has_valid_user_id = bool(st.session_state.get('user_id', ''))
            
            # Add warning and confirmation for clearing database
            if st.button("Clear All Messages from Database", type="secondary", key="clear_db_btn", disabled=True):
                if st.session_state.get("confirm_clear_db"):
                    deleted_count = st.session_state.mongodb_service.delete_all_messages()
                    st.success(f"Successfully deleted {deleted_count} messages from the database.")
                    st.session_state.confirm_clear_db = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear_db = True
                    st.warning("⚠️ Are you sure? Click again to confirm deletion of ALL messages from the database. This action cannot be undone.")
                    
    # Submit button
    if st.button("Generate Message", 
             type="primary", 
             key="start_workflow_btn",
             disabled=not has_valid_user_id):  # Disable if no valid user ID
    
        # Validate User ID first
        if not st.session_state.get('user_id'):
            st.error("Please enter a User ID to continue.")
            return
        
        # Find the actual text for selected items
        custom_contexts = get_custom_contexts()
        custom_tones = get_custom_tones()
        
        # For focus and style, we're now using the text directly
        selected_context_text = next((ctx["text"] for ctx in custom_contexts if ctx["id"] == selected_context_id), "")
        selected_tone_text = next((tone["text"] for tone in custom_tones if tone["id"] == selected_tone_id), "")
        
        # Get values directly from the UI
        selected_focus_text = st.session_state.focus_selector
        selected_style_text = st.session_state.style_selector
        
        # Get the message length and number of messages from the UI
        message_length = st.session_state.get("message_length_slider", 3)
        num_messages = st.session_state.get("num_messages_input", 3)
        
        if not selected_concept or not selected_context_text:
            st.error("Please select a concept and context.")
            return
        
        with st.spinner("Initializing workflow..."):
            success = initialize_workflow(
                concept_name=selected_concept,
                context=selected_context_text,
                diversity_focus=selected_focus_text,
                tone=selected_tone_text,
                message_style=selected_style_text,
                generator_model=generator_model,
                evaluator_model=evaluator_model,
                generator_temp=generator_temp,
                evaluator_temp=evaluator_temp,
                generator_top_p=generator_top_p,
                evaluator_top_p=evaluator_top_p,
                message_length=message_length,
                num_messages=num_messages
            )
            
            if success:
                st.session_state.current_view = "generation"
                st.rerun()
            else:
                st.error("Failed to initialize workflow. Please check your settings and API keys.")