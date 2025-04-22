"""
Common UI components module.
Contains shared UI components and utility functions.
"""

import streamlit as st
from data.concepts import TASK_CONTEXTS, MESSAGE_FOCUSES, TONES

# Define default message styles
MESSAGE_STYLES = [
    "Create a message that uses a question-answer format",
    "Create a message that uses a conditional 'when-then' structure",
    "Create a message that uses a comparison or contrast structure",
    "Create a message that uses cause-effect reasoning format",
]

# Define short descriptions for task contexts
TASK_CONTEXT_DESCRIPTIONS = [
    "Problem-solving scenarios",
    "Persistence & skill tasks",
    "Learning & expertise",
    "Progressive challenges",
    "Skill development"
]

def get_custom_contexts():
    """Get task contexts from session state or default list."""
    if "custom_contexts" not in st.session_state:
        # Create task context labels with short descriptions
        labeled_contexts = []
        for i, (context, description) in enumerate(zip(TASK_CONTEXTS, TASK_CONTEXT_DESCRIPTIONS), 1):
            labeled_contexts.append({
                "id": description,  # Use short description as ID
                "text": context
            })
        st.session_state.custom_contexts = labeled_contexts
    return st.session_state.custom_contexts

def get_custom_focuses():
    """Get message focuses from session state or default list."""
    if "custom_focuses" not in st.session_state:
        # Create focus labels
        labeled_focuses = []
        for i, focus in enumerate(MESSAGE_FOCUSES, 1):
            labeled_focuses.append({
                "id": f"Predefined Focus {i}",
                "text": focus
            })
        st.session_state.custom_focuses = labeled_focuses
    return st.session_state.custom_focuses

def get_custom_tones():
    """Get tones from session state or default list."""
    if "custom_tones" not in st.session_state:
        # Create tone labels
        labeled_tones = []
        for i, tone in enumerate(TONES, 1):
            labeled_tones.append({
                "id": tone,
                "text": tone
            })
        st.session_state.custom_tones = labeled_tones
    return st.session_state.custom_tones

def get_custom_styles():
    """Get message styles from session state or default list."""
    if "custom_styles" not in st.session_state:
        # Create style labels
        labeled_styles = []
        for i, style in enumerate(MESSAGE_STYLES, 1):
            labeled_styles.append({
                "id": f"Style {i}",
                "text": style
            })
        st.session_state.custom_styles = labeled_styles
    return st.session_state.custom_styles

def add_task_context():
    """Add a new task context."""
    custom_contexts = get_custom_contexts()
    new_id = f"Custom Task {len(custom_contexts) + 1}"
    
    with st.form("add_task_form", clear_on_submit=True):
        new_text = st.text_area("Enter a new task context", height=100, key="new_task_text")
        new_id = st.text_input("Short description (3-4 words)", key="new_task_id", 
                               help="This will appear in the dropdown menu")
        submit = st.form_submit_button("Add Task Context")
        
        if submit and new_text:
            if not new_id:
                new_id = f"Custom Task {len(custom_contexts) + 1}"
            custom_contexts.append({
                "id": new_id,
                "text": new_text
            })
            st.success(f"Added new task context: {new_id}")
            st.session_state.custom_contexts = custom_contexts
            st.rerun()

def add_message_focus():
    """Add a new message focus."""
    custom_focuses = get_custom_focuses()
    new_id = f"Custom Focus {len(custom_focuses) + 1}"
    
    with st.form("add_focus_form", clear_on_submit=True):
        new_text = st.text_area("Enter a new message focus", height=100, key="new_focus_text")
        submit = st.form_submit_button("Add Message Focus")
        
        if submit and new_text:
            custom_focuses.append({
                "id": new_id,
                "text": new_text
            })
            st.success(f"Added new message focus: {new_id}")
            st.session_state.custom_focuses = custom_focuses
            st.rerun()

def add_message_tone():
    """Add a new message tone."""
    custom_tones = get_custom_tones()
    new_id = f"Custom Tone {len(custom_tones) + 1}"
    
    with st.form("add_tone_form", clear_on_submit=True):
        new_text = st.text_input("Enter a new tone", key="new_tone_text")
        submit = st.form_submit_button("Add Tone")
        
        if submit and new_text:
            custom_tones.append({
                "id": new_id,
                "text": new_text
            })
            st.success(f"Added new tone: {new_id}")
            st.session_state.custom_tones = custom_tones
            st.rerun()

def add_message_style():
    """Add a new message style."""
    custom_styles = get_custom_styles()
    new_id = f"Custom Style {len(custom_styles) + 1}"
    
    with st.form("add_style_form", clear_on_submit=True):
        new_text = st.text_area("Enter a new message style", height=100, key="new_style_text")
        submit = st.form_submit_button("Add Message Style")
        
        if submit and new_text:
            custom_styles.append({
                "id": new_id,
                "text": new_text
            })
            st.success(f"Added new message style: {new_id}")
            st.session_state.custom_styles = custom_styles
            st.rerun()

def delete_task_context(task_id):
    """Delete a task context by ID."""
    custom_contexts = get_custom_contexts()
    st.session_state.custom_contexts = [ctx for ctx in custom_contexts if ctx["id"] != task_id]
    st.success(f"Deleted task context: {task_id}")
    st.rerun()

def delete_message_focus(focus_id):
    """Delete a message focus by ID."""
    custom_focuses = get_custom_focuses()
    st.session_state.custom_focuses = [focus for focus in custom_focuses if focus["id"] != focus_id]
    st.success(f"Deleted message focus: {focus_id}")
    st.rerun()

def delete_message_tone(tone_id):
    """Delete a message tone by ID."""
    custom_tones = get_custom_tones()
    st.session_state.custom_tones = [tone for tone in custom_tones if tone["id"] != tone_id]
    st.success(f"Deleted message tone: {tone_id}")
    st.rerun()

def delete_message_style(style_id):
    """Delete a message style by ID."""
    custom_styles = get_custom_styles()
    st.session_state.custom_styles = [style for style in custom_styles if style["id"] != style_id]
    st.success(f"Deleted message style: {style_id}")
    st.rerun()