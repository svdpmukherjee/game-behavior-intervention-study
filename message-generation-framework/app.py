"""
Main Streamlit application.
Human-in-the-Loop Message Generation Workflow.
"""

import logging
import os
from typing import List, Dict, Any

import streamlit as st
from dotenv import load_dotenv

# Import modularized components
from ui.header import display_header
from ui.setup import display_setup_view
from ui.generation import display_generation_view
from ui.next_message import display_next_message_view
from ui.change_focus import display_change_focus_view
from ui.results import display_results_view
from ui.styling import apply_custom_css
from services.similarity import SemanticSimilarityService
from workflow.state_manager import (
    initialize_services, reset_session_state, save_results_to_file
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Message Generator App",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def api_key_setup():
    """Setup API keys for the application."""
    st.markdown('<div class="section-header">API Key Setup</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-explanation">Enter at least one API key to access language models. '
        'Your API keys allow the application to generate and evaluate messages using powerful AI models.</div>',
        unsafe_allow_html=True
    ) 
    
    # Load API keys from environment or session state
    together_key = os.getenv("TOGETHER_API_KEY") or st.session_state.get("together_api_key", "")
    openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_api_key", "")
    
    # Check if keys are already in session state
    if "together_api_key" not in st.session_state:
        st.session_state.together_api_key = together_key
    
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = openai_key
    
    # Create API key input fields
    together_api_key = st.text_input(
        "Together API Key",
        type="password",
        value=st.session_state.together_api_key,
        help="Required for using Together AI models (Llama, Gemma, etc.)",
        key="together_api_key_input"
    )
    
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.openai_api_key,
        help="Required for using OpenAI models (GPT-4, GPT-3.5)",
        key="openai_api_key_input"
    )
    
    # Update session state with input values
    st.session_state.together_api_key = together_api_key
    st.session_state.openai_api_key = openai_api_key
    
    # Initialize services if keys are provided
    if together_api_key or openai_api_key:
        with st.spinner("Initializing services..."):
            initialize_services(together_api_key, openai_api_key)
        return True
    else:
        st.warning("Please enter at least one API key to continue.")
        return False

def lazy_load_similarity_model():
    """Lazy load the similarity model only when needed."""
    if 'similarity_service' not in st.session_state:
        with st.spinner("Loading similarity model..."):
            st.session_state.similarity_service = SemanticSimilarityService()
            logger.info("Semantic similarity service initialized")

def main():
    """Main application function."""
    # Apply custom CSS
    apply_custom_css()
    
    # Display application header
    display_header()
    st.markdown(
            '<br/>',
            unsafe_allow_html=True)
    
    # Sidebar for API key setup
    with st.sidebar:
        st.title("Settings")
        
        with st.container(border=True):
            api_keys_valid = api_key_setup()
        
        st.divider()
        
        # Navigation
        if api_keys_valid:
            st.subheader("Navigation")
            if st.button("New Workflow", use_container_width=True, key="sidebar_new_workflow_btn"):
                if 'workflow' in st.session_state and st.session_state.workflow.final_messages:
                    if st.session_state.get("confirm_new_workflow"):
                        # Save current results first
                        if len(st.session_state.workflow.final_messages) > 0:
                            save_path = save_results_to_file()
                            if save_path:
                                st.success(f"Previous results saved to: {save_path}")
                        
                        # Reset session state
                        reset_session_state()
                        st.rerun()
                    else:
                        st.session_state.confirm_new_workflow = True
                        st.warning("Click again to confirm. Current progress will be saved before starting new workflow.")
                else:
                    reset_session_state()
                    st.rerun()
    
    # Main content based on current view
    current_view = st.session_state.get("current_view", "setup")
    
    # Display appropriate view based on current state
    if current_view == "setup":
        display_setup_view()
    elif current_view == "generation":
        # Only load similarity model when needed
        lazy_load_similarity_model()
        display_generation_view()
    elif current_view == "next_message":
        display_next_message_view()
    elif current_view == "change_focus":
        display_change_focus_view()
    elif current_view == "results":
        display_results_view()
    else:
        st.error(f"Unknown view: {current_view}")
        reset_session_state()
        st.rerun()

if __name__ == "__main__":
    # Initialize session state if needed
    if "current_view" not in st.session_state:
        st.session_state.current_view = "setup"
    
    # Initialize other session state variables
    if "show_add_task" not in st.session_state:
        st.session_state.show_add_task = False
    if "show_add_focus" not in st.session_state:
        st.session_state.show_add_focus = False
    if "show_add_tone" not in st.session_state:
        st.session_state.show_add_tone = False
    
    main()