"""
Generation view module contains functions for displaying the message generation and evaluation view.
"""

import streamlit as st
from utils.helpers import format_time, create_evaluation_visualization, display_competing_concepts
from ui.styling import apply_message_editing_css

def display_generation_view():
    """Display the message generation and evaluation view."""
    apply_message_editing_css()
    st.markdown(
        """
        <script>
            window.scrollTo(0, 0);
        </script>
        """, 
        unsafe_allow_html=True
    )
    
    if 'workflow' not in st.session_state:
        st.error("Workflow not initialized. Please set up the workflow first.")
        st.session_state.current_view = "setup"
        st.rerun()
        return
    
    workflow = st.session_state.workflow
    
    # Display current workflow info
    with st.container(border=True):
        # Get the concept number from session state
        concept_number = st.session_state.get("concept_numbers", {}).get(workflow.concept_name, "")
        concept_display = f"{concept_number}. {workflow.concept_name}" if concept_number else workflow.concept_name
            
        st.markdown(f'<div class="sub-header">Concept Selected - {concept_display}</div>', unsafe_allow_html=True)
        # st.markdown(
        #     '<div class="">You\'re now in the message generation phase. The AI will generate a message, '
        #     'which will be evaluated for alignment with your selected psychological concept. You can provide feedback '
        #     'to improve the message or accept it when you\'re satisfied.</div>',
        #     unsafe_allow_html=True
        # )
        
        col1, col2, col3, col4 = st.columns([1, 3, 1, 2])
        with col1:
            st.markdown(f"**Message #{workflow.current_message_number} of {workflow.num_messages}**, Iteration #{workflow.current_iteration}")
        with col2:
            st.markdown(f"Focus: **{workflow.diversity_focus}**")
        with col3:
            st.markdown(f"Tone: **{workflow.tone}**")
        with col4:
            st.markdown(f"Style: **{workflow.message_style}**")
            
        with st.expander("View Concept Definition", expanded=True):
            custom_def_key = f"custom_definition_{workflow.concept_name}"
            concept_definition = st.session_state.get(custom_def_key, workflow.concept_info.get("description", ""))
            
            st.markdown(
                f"""
                <div style='font-size: 18px; font-weight: bold; line-height: 1.6;'>
                    <span style='font-weight: normal;'>{concept_definition}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Display current state based on what exists in the workflow
    current_message = workflow.message_history[-1] if workflow.message_history else None
    current_evaluation = workflow.evaluation_history[-1] if workflow.evaluation_history else None
    
    # If no message exists yet, generate the first one
    if not current_message:
        with st.spinner("Generating initial message..."):
            message, evaluation = workflow.run_iteration()
        st.rerun()
        return
    
    # Display the current message
    with st.container(border=True):
        st.markdown('<div class="section-header">Message Generated</div>', unsafe_allow_html=True)
        
        # Add editable message feature
        edited_message = st.text_area(
            "Message",
            placeholder="Edit the message here if you want to make changes.",
            value=current_message,
            height=150,
            key="editable_message"
        )
        # Show message whether button is enabled or disabled        
        # if edited_message == current_message:
        #     st.info("You can edit the message and accept, the save & evaluate button will be enabled.")

        if edited_message == current_message:
            with st.expander("Message options explained", expanded=True):
                st.markdown("""
                **What you can do with this message:**
                
                - **Edit + Accept**: Make changes and click "I Accept the Message" to finalize
                - **Edit + Refine**: Make changes, provide feedback and generate again with AI model
                - **Accept as is**: Click "Accept Message" to finalize the current version
                - **Refine as is**: Provide feedback and generate again with AI model
                - **Edit + Evaluate**: Make changes and evaluate the edited message without AI regeneration (visible at the end)
                """)
            # st.info("If you edit the message, the save & evaluate button will be enabled.")
    
    # Create new unique keys for each render to force clearing of fields
    # This is a simple approach that guarantees fields are cleared on each iteration
    unique_key_base = f"feedback_{workflow.current_message_number}_{workflow.current_iteration}"
    
    # Human feedback section with structured feedback fields - MOVED UP before evaluation display
    with st.container(border=True):
        st.markdown('<div class="section-header">Your Feedback</div>', unsafe_allow_html=True)
        
        # Create columns for the feedback form
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Rating slider
            rating = st.slider(
                "How strongly do you think the message aligns with the concept? (1-10 i.e. worst->best)",
                min_value=1,
                max_value=10,
                value=7,
                step=1,
                key=f"{unique_key_base}_rating_slider"
            )
        
        with col2:
            # Structured feedback fields with unique keys for each render
            strengths_feedback = st.text_area(
                "Strengths (what to preserve)",
                placeholder="What aspects of this message work well and should be kept?",
                height=70,
                key=f"{unique_key_base}_strengths_feedback_area"
            )
            
            weaknesses_feedback = st.text_area(
                "Weaknesses (what to change)",
                placeholder="What aspects need improvement or don't align well with the concept?",
                height=70,
                key=f"{unique_key_base}_weaknesses_feedback_area" 
            )
            
            improvement_feedback = st.text_area(
                "Improvement Suggestions",
                placeholder="Specific suggestions for improving the message in the next iteration",
                height=70,
                key=f"{unique_key_base}_improvement_feedback_area"
            )
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Refine the Message with My Feedback", type="primary", use_container_width=True, key=f"{unique_key_base}_refine_message_btn"):
                # Update the message in workflow if it was edited
                if edited_message != current_message:
                    workflow.message_history[-1] = edited_message
                
                # Record structured feedback
                workflow.record_structured_human_feedback(
                    rating,
                    strengths_feedback,
                    weaknesses_feedback,
                    improvement_feedback
                )
                
                # Increment iteration
                workflow.increment_iteration()
                
                # Generate next iteration
                with st.spinner("Generating improved message..."):
                    message, evaluation = workflow.run_iteration()
                
                st.rerun()
        
        with col2:
            accept_button_type = "primary"
            accept_button_disabled = False
            
            # Check if message is too similar to previous ones and add a warning
            if len(workflow.final_messages) > 0 and 'similarity_service' in st.session_state:
                similarity_result = st.session_state.similarity_service.check_message_diversity(
                    current_message, workflow.final_messages
                )
                
                if not similarity_result["is_diverse"]:
                    accept_button_type = "secondary"
                    st.warning("This message is very similar to previous ones. Consider refining it further for more diversity.")
            
            if st.button("I Accept the Message", type=accept_button_type, use_container_width=True, key=f"{unique_key_base}_accept_message_btn"):
                # Update the message in workflow if it was edited
                if edited_message != current_message:
                    workflow.message_history[-1] = edited_message
                
                # Record structured feedback
                workflow.record_structured_human_feedback(
                    rating,
                    strengths_feedback,
                    weaknesses_feedback,
                    improvement_feedback
                )
                
                # Finalize message
                final_message = workflow.finalize_message()
                
                # Check if all messages are complete
                if len(workflow.final_messages) >= workflow.num_messages:
                    st.session_state.current_view = "results"
                else:
                    # Prepare for next message
                    st.session_state.current_view = "next_message"
                
                st.rerun()
        
        with col3:  
            if st.button("Cancel & Reset", type="secondary", use_container_width=True, key=f"{unique_key_base}_cancel_reset_btn"):
                if st.session_state.get("confirm_reset"):
                    from workflow.state_manager import reset_session_state
                    reset_session_state()
                    st.rerun()
                else:
                    st.session_state.confirm_reset = True
                    st.warning("Click again to confirm reset. All progress will be lost.")
    
    # Display evaluation results after feedback section
    if current_evaluation:
        with st.container(border=True):
            st.markdown('<div class="section-header">In Case You are Interested About the Evaluation Results by Your Selected Evaluator Model</div>', unsafe_allow_html=True)
            
            score = current_evaluation["score"]
            score_class = "score-high" if score >= 80 else ("score-medium" if score >= 70 else "score-low")
            
            # Generation and evaluation times
            gen_time = format_time(workflow.generation_time) if workflow.generation_time else "N/A"
            eval_time = format_time(workflow.evaluation_time) if workflow.evaluation_time else "N/A"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f'<div class="score-indicator {score_class}">{score}% Alignment Calculated between the Concept and the Generated Message</div>', unsafe_allow_html=True)
            
            # Create visualization of evaluation results
            eval_vis_data = create_evaluation_visualization(current_evaluation, workflow.concept_name)
            if eval_vis_data:
                # Display top competing concepts
                if eval_vis_data.get("competing", []):
                    st.markdown("### Top competing concepts:")
                    
                    # Create a nice table to display competing concepts
                    competing_data = [{"Concept": concept["name"], "Alignment Score": f"{concept['score']}%"} 
                                    for concept in eval_vis_data["competing"][:3]]
                    
                    # Display as a dataframe for better styling
                    import pandas as pd
                    competing_df = pd.DataFrame(competing_data)
                    st.dataframe(competing_df, hide_index=True, use_container_width=True)
            
            # Evaluation feedback
            with st.expander("View detailed evaluation feedback", expanded=False):
                st.markdown("### Strengths")
                st.markdown(current_evaluation["feedback"]["strengths"])
                
                st.markdown("### Improvements")
                st.markdown(current_evaluation["feedback"]["improvements"])
                
                st.markdown("### Differentiation Tips")
                st.markdown(current_evaluation["feedback"]["differentiation_tips"])
                
            # Display similarity check if there are previous messages
            if len(workflow.final_messages) > 0 and 'similarity_service' in st.session_state:
                with st.expander("Message Diversity Check", expanded=False):
                    similarity_result = st.session_state.similarity_service.check_message_diversity(
                        current_message, workflow.final_messages
                    )
                    
                    if similarity_result["is_diverse"]:
                        st.success(f"Message is sufficiently distinct from previous messages (Max similarity: {similarity_result['max_similarity']:.2f})")
                    else:
                        st.warning(f"Message is too similar to previous messages (Max similarity: {similarity_result['max_similarity']:.2f})")
                        st.markdown("Consider using different examples, structure, or phrasing to increase diversity.")

            # Add save & evaluate button in the feedback section
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Always show the increment iteration checkbox
            if "increment_iteration" not in st.session_state:
                st.session_state.increment_iteration = True
            
            increment_iteration = st.checkbox(
                "Count as new iteration when saving",
                value=st.session_state.increment_iteration,
                help="If checked, saving will increase the iteration counter. This helps track major changes to the message.",
                key="increment_iteration_checkbox"
            )
            st.session_state.increment_iteration = increment_iteration
        
        # Always show the Save & Evaluate button
        if st.button("Save the Edited Message & Evaluate It Only (No Generation)", 
                     key="save_evaluate_message_btn", 
                     disabled=(edited_message == current_message),
                     type="primary" if edited_message != current_message else "secondary"):
            # First check if the message was actually edited
            if edited_message != current_message:
                # Update the message in workflow
                workflow.message_history[-1] = edited_message
                
                # Increment iteration if checkbox is checked
                if st.session_state.increment_iteration:
                    workflow.increment_iteration()
                    status_message = "Message saved and evaluated as new iteration!"
                else:
                    status_message = "Message saved and re-evaluated!"
                
                # Evaluate the edited message
                with st.spinner("Evaluating edited message..."):
                    evaluation = workflow.evaluate_current_message()
                
                st.success(status_message)
                st.rerun()
            else:
                st.info("No changes detected in the message.")