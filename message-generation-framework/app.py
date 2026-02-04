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
    initialize_services, initialize_mongodb, reset_session_state, save_results_to_file
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

def get_secret(key, default=""):
    """Get a secret from st.secrets (Streamlit Cloud) or environment variables."""
    # First try st.secrets (Streamlit Cloud)
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            value = st.secrets[key]
            if value:  # Only return if non-empty
                return value
    except Exception:
        pass

    # Fall back to environment variables
    env_value = os.getenv(key)
    if env_value:
        return env_value

    return default

def has_server_credentials():
    """Check if server-side credentials are configured (secrets or env vars)."""
    together_key = get_secret("TOGETHER_API_KEY")
    openai_key = get_secret("OPENAI_API_KEY")
    mongodb_uri = get_secret("MONGODB_URI")
    return bool(together_key or openai_key) and bool(mongodb_uri)

def api_key_setup():
    """Setup API keys for the application."""
    st.markdown('<div class="section-header">API Key Setup</div>', unsafe_allow_html=True)

    # Check if server-side credentials exist (from secrets or env vars)
    server_together_key = get_secret("TOGETHER_API_KEY")
    server_openai_key = get_secret("OPENAI_API_KEY")
    server_mongodb_uri = get_secret("MONGODB_URI")
    server_mongodb_db_name = get_secret("MONGODB_DB_NAME", "message_generator")

    has_server_api_keys = bool(server_together_key or server_openai_key)
    has_server_mongodb = bool(server_mongodb_uri)

    # Initialize session state for "use own credentials" toggle
    if "use_own_api_keys" not in st.session_state:
        st.session_state.use_own_api_keys = not has_server_api_keys
    if "use_own_mongodb" not in st.session_state:
        st.session_state.use_own_mongodb = not has_server_mongodb

    # Initialize credential session states
    if "together_api_key" not in st.session_state:
        st.session_state.together_api_key = ""
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    if "mongodb_uri" not in st.session_state:
        st.session_state.mongodb_uri = ""
    if "mongodb_db_name" not in st.session_state:
        st.session_state.mongodb_db_name = "message_generator"

    # Determine which credentials to use
    together_api_key = ""
    openai_api_key = ""
    uri_input = ""
    db_name_input = server_mongodb_db_name

    # API Keys section
    if has_server_api_keys:
        st.success("✓ API keys configured")
        use_own = st.checkbox(
            "Use my own API keys instead",
            value=st.session_state.use_own_api_keys,
            key="use_own_api_keys_checkbox"
        )
        st.session_state.use_own_api_keys = use_own

        if use_own:
            st.markdown(
                '<div class="section-explanation">Enter your API keys below.</div>',
                unsafe_allow_html=True
            )
            together_api_key = st.text_input(
                "Together.ai API Key",
                type="password",
                value=st.session_state.together_api_key,
                placeholder="e.g., a]1b2c3d4e5f6g7h8i9j0...",
                help="Required for using Together AI models (Llama, Gemma, etc.)",
                key="together_api_key_input"
            )
            openai_api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.openai_api_key,
                placeholder="e.g., sk-proj-xxxx...",
                help="Required for using OpenAI models (GPT-4, GPT-3.5)",
                key="openai_api_key_input"
            )
            st.session_state.together_api_key = together_api_key
            st.session_state.openai_api_key = openai_api_key
        else:
            # Use server credentials (never display them)
            together_api_key = server_together_key
            openai_api_key = server_openai_key
    else:
        st.markdown(
            '<div class="section-explanation">Enter at least one API key to access language models.</div>',
            unsafe_allow_html=True
        )
        together_api_key = st.text_input(
            "Together.ai API Key",
            type="password",
            value=st.session_state.together_api_key,
            placeholder="e.g., a]1b2c3d4e5f6g7h8i9j0...",
            help="Required for using Together AI models (Llama, Gemma, etc.)",
            key="together_api_key_input"
        )
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.openai_api_key,
            placeholder="e.g., sk-proj-xxxx...",
            help="Required for using OpenAI models (GPT-4, GPT-3.5)",
            key="openai_api_key_input"
        )
        st.session_state.together_api_key = together_api_key
        st.session_state.openai_api_key = openai_api_key

    # MongoDB section
    with st.expander("Database Settings (MongoDB)", expanded=not has_server_mongodb):
        if has_server_mongodb:
            st.success("✓ Database configured")
            use_own_db = st.checkbox(
                "Use my own MongoDB instead",
                value=st.session_state.use_own_mongodb,
                key="use_own_mongodb_checkbox"
            )
            st.session_state.use_own_mongodb = use_own_db

            if use_own_db:
                # Use separate session state keys for user's own credentials
                if "user_mongodb_uri" not in st.session_state:
                    st.session_state.user_mongodb_uri = ""
                if "user_mongodb_db_name" not in st.session_state:
                    st.session_state.user_mongodb_db_name = ""

                uri_input = st.text_input(
                    "MongoDB URI",
                    type="password",
                    value=st.session_state.user_mongodb_uri,
                    placeholder="e.g., mongodb+srv://user:pass@cluster.mongodb.net/",
                    help="Connection URI for MongoDB",
                    key="mongodb_uri_input"
                )
                db_name_input = st.text_input(
                    "MongoDB Database Name",
                    value=st.session_state.user_mongodb_db_name,
                    placeholder="e.g., my_database",
                    help="Name of the MongoDB database to use",
                    key="mongodb_db_name_input"
                )
                st.session_state.user_mongodb_uri = uri_input
                st.session_state.user_mongodb_db_name = db_name_input
            else:
                # Use server credentials (never display them)
                uri_input = server_mongodb_uri
                db_name_input = server_mongodb_db_name
        else:
            uri_input = st.text_input(
                "MongoDB URI",
                type="password",
                value=st.session_state.mongodb_uri,
                placeholder="e.g., mongodb+srv://user:pass@cluster.mongodb.net/",
                help="Connection URI for MongoDB",
                key="mongodb_uri_input"
            )
            db_name_input = st.text_input(
                "MongoDB Database Name",
                value=st.session_state.mongodb_db_name,
                placeholder="e.g., my_database",
                help="Name of the MongoDB database to use",
                key="mongodb_db_name_input"
            )
            st.session_state.mongodb_uri = uri_input
            st.session_state.mongodb_db_name = db_name_input

        # Collection info message
        st.info("Collections will be automatically created based on concept names. Each concept will have its own collection.")

    # Initialize services if keys are provided
    if together_api_key or openai_api_key:
        with st.spinner("Initializing services..."):
            initialize_services(together_api_key, openai_api_key)

            # Initialize MongoDB if URI is provided
            if uri_input:
                initialize_mongodb(uri_input, db_name_input)
                logger.info(f"MongoDB initialized with database: {db_name_input}")
            else:
                st.warning("MongoDB URI not provided. Message storage will be unavailable.")

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