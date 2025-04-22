"""
State manager module for Streamlit.
Manages session state for the Streamlit application.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from functools import lru_cache
import base64
from services.mongodb_service import MongoDBService
import streamlit as st

from data.concepts import ALL_conceptS, TASK_CONTEXTS, MESSAGE_FOCUSES, TONES
from services.generator import TextGenerationService
from services.evaluator import MessageEvaluationService
from workflow.message_workflow import MessageWorkflow

logger = logging.getLogger(__name__)

# Use lru_cache to avoid reloading services
@lru_cache(maxsize=2)
def get_service_instance(service_type, together_api_key=None, openai_api_key=None):
    """
    Get cached service instances to improve performance.
    
    Args:
        service_type: Type of service to get ('generator' or 'evaluator')
        together_api_key: API key for Together.ai
        openai_api_key: API key for OpenAI
        
    Returns:
        Service instance
    """
    if service_type == 'generator':
        return TextGenerationService(
            together_api_key=together_api_key,
            openai_api_key=openai_api_key
        )
    elif service_type == 'evaluator':
        return MessageEvaluationService(
            together_api_key=together_api_key,
            openai_api_key=openai_api_key
        )
    else:
        raise ValueError(f"Unknown service type: {service_type}")

def initialize_services(together_api_key: Optional[str] = None, openai_api_key: Optional[str] = None):
    """
    Initialize API services and store them in session state.
    
    Args:
        together_api_key: API key for Together.ai
        openai_api_key: API key for OpenAI
    """
    # Initialize services if not already in session state or if keys have changed
    current_together_key = st.session_state.get('current_together_key')
    current_openai_key = st.session_state.get('current_openai_key')
    
    # Check if keys have changed
    keys_changed = (current_together_key != together_api_key or 
                   current_openai_key != openai_api_key)
    
    if 'generator_service' not in st.session_state or keys_changed:
        st.session_state.generator_service = get_service_instance(
            'generator', together_api_key, openai_api_key
        )
        logger.info("Text generation service initialized")
    
    if 'evaluator_service' not in st.session_state or keys_changed:
        st.session_state.evaluator_service = get_service_instance(
            'evaluator', together_api_key, openai_api_key
        )
        logger.info("Message evaluation service initialized")
    
    # Store current keys for future comparison
    st.session_state.current_together_key = together_api_key
    st.session_state.current_openai_key = openai_api_key
    
def initialize_mongodb(uri: Optional[str] = None, db_name: Optional[str] = None):
    """
    Initialize MongoDB service and store it in session state.
    
    Args:
        uri: MongoDB connection URI
        db_name: Name of the database
    """
    if not uri:
        # Use default URI if not provided
        uri = st.session_state.get('mongodb_uri', os.getenv("MONGODB_URI", 'mongodb://localhost:27017/'))
    
    if not db_name:
        # Use default database name if not provided
        db_name = st.session_state.get('mongodb_db_name', os.getenv("MONGODB_DB_NAME", 'message_generator'))
    
    # Store values in session state
    st.session_state.mongodb_uri = uri
    st.session_state.mongodb_db_name = db_name
    
    # Initialize service if not already in session state or if connection details have changed
    current_uri = st.session_state.get('current_mongodb_uri')
    current_db_name = st.session_state.get('current_mongodb_db_name')
    
    if ('mongodb_service' not in st.session_state or 
        current_uri != uri or 
        current_db_name != db_name):
        # No collection name is provided - collections will be created based on concept names
        st.session_state.mongodb_service = MongoDBService(uri, db_name)
        logger.info(f"MongoDB service initialized with database: {db_name}")
    
    # Store current values for future comparison
    st.session_state.current_mongodb_uri = uri
    st.session_state.current_mongodb_db_name = db_name

def initialize_workflow(
    concept_name: str,
    context: str,
    diversity_focus: str,
    tone: str,
    message_style: str,
    generator_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    evaluator_model: str = "gpt-4o",
    generator_temp: float = 0.7,
    evaluator_temp: float = 0.2,
    generator_top_p: float = 0.95,
    evaluator_top_p: float = 0.95,
    message_length: int = 3,
    num_messages: int = 3
) -> bool:
    """
    Initialize a new message generation workflow and store it in session state.
    
    Args:
        concept_name: Name of the psychological concept
        context: Task context for the message
        diversity_focus: Focus area for the message
        tone: Desired tone for the message
        message_style: Structural style for the message
        generator_model: Model to use for text generation
        evaluator_model: Model to use for message evaluation
        generator_temp: Temperature setting for generation
        evaluator_temp: Temperature setting for evaluation
        generator_top_p: Top P setting for generation
        evaluator_top_p: Top P setting for evaluation
        message_length: Number of sentences per message
        num_messages: Number of messages to generate
        
    Returns:
        True if workflow was successfully initialized, False otherwise
    """
    # Check if services are initialized
    if 'generator_service' not in st.session_state or 'evaluator_service' not in st.session_state:
        st.error("API services not initialized. Please set up API keys first.")
        return False
    
    # Get concept info
    concept_info = ALL_conceptS.get(concept_name, {})
    if not concept_info:
        st.error(f"concept '{concept_name}' not found.")
        return False
    
    # Use custom concept definition if available
    custom_definition_key = f"custom_definition_{concept_name}"
    if custom_definition_key in st.session_state:
        concept_info = concept_info.copy()  # Create a copy to avoid modifying the original
        concept_info["description"] = st.session_state[custom_definition_key]
    
    # Set up generator with custom parameters
    generate_text, generator_config = st.session_state.generator_service.setup_generator(
        generator_model, generator_temp
    )
    # Update top_p in generator config
    generator_config["top_p"] = generator_top_p
    
    # Set up evaluator with custom parameters
    evaluate_message, evaluator_config = st.session_state.evaluator_service.setup_evaluator(
        evaluator_model, evaluator_temp
    )
    # Update top_p in evaluator config
    evaluator_config["top_p"] = evaluator_top_p
    
    # Create workflow
    workflow = MessageWorkflow(
        concept_name=concept_name,
        concept_info=concept_info,
        context=context,
        diversity_focus=diversity_focus,
        tone=tone,
        message_style=message_style,
        generate_text=generate_text,
        evaluate_message=evaluate_message,
        generator_config=generator_config,
        evaluator_config=evaluator_config
    )
    
    # Set additional parameters
    workflow.message_length = message_length
    workflow.num_messages = num_messages
    
    # Store in session state
    st.session_state.workflow = workflow
    st.session_state.current_view = "generation"
    
    return True

def save_results_to_file() -> Optional[str]:
    """
    Save the workflow results to a file and provide download link.
    
    Returns:
        Path to the saved file, or None if saving failed
    """
    if 'workflow' not in st.session_state:
        logger.error("No workflow found in session state")
        return None
    
    workflow = st.session_state.workflow
    
    # Create results dictionary
    results = {
        "concept": workflow.concept_name,
        "context": workflow.context,
        "diversity_focus": workflow.diversity_focus,
        "tone": workflow.tone,
        "message_style": workflow.message_style,
        "message_length": workflow.message_length,
        "num_messages": workflow.num_messages,
        "generator_model": workflow.generator_config["model"],
        "evaluator_model": workflow.evaluator_config["model"],
        "generator_settings": {
            "temperature": workflow.generator_config["temperature"],
            "top_p": workflow.generator_config["top_p"]
        },
        "evaluator_settings": {
            "temperature": workflow.evaluator_config["temperature"],
            "top_p": workflow.evaluator_config["top_p"]
        },
        "final_messages": workflow.final_messages,
        "iterations_per_message": workflow.iterations_per_message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Convert to JSON string
    json_str = json.dumps(results, indent=2)
    
    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{workflow.concept_name}_results_{timestamp}.json"
    
    # Create download link
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">Download Results JSON</a>'
    
    # Display download link
    st.markdown(href, unsafe_allow_html=True)
    
    # For compatibility, still save locally if possible
    try:
        output_dir = os.path.join("results")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(json_str)
        logger.info(f"Results saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving results to file: {e}")
        return None

def check_api_keys() -> bool:
    """
    Check if API keys are available.
    
    Returns:
        True if at least one API key is available, False otherwise
    """
    together_api_key = st.session_state.get('together_api_key')
    openai_api_key = st.session_state.get('openai_api_key')
    
    return bool(together_api_key or openai_api_key)

def reset_session_state():
    """Reset the session state to initial values."""
    # Keys to preserve
    preserve_keys = [
        'together_api_key', 
        'openai_api_key', 
        'generator_service', 
        'evaluator_service',
        'current_together_key',
        'current_openai_key',
        'custom_contexts',
        'custom_focuses',
        'custom_tones',
        'custom_styles',
        'user_id',
        'mongodb_uri',
        'mongodb_db_name',
        'current_mongodb_uri',
        'current_mongodb_db_name',
        'mongodb_service'
    ]
    
    # Extract values to preserve
    preserved_values = {}
    for key in preserve_keys:
        if key in st.session_state:
            preserved_values[key] = st.session_state[key]
    
    # Also preserve custom concept definitions
    custom_def_keys = [k for k in st.session_state.keys() if k.startswith("custom_definition_")]
    for key in custom_def_keys:
        preserved_values[key] = st.session_state[key]
    
    # Clear everything
    st.session_state.clear()
    
    # Restore preserved values
    for key, value in preserved_values.items():
        st.session_state[key] = value
    
    # Set initial view
    st.session_state.current_view = "setup"
    
    # Initialize flags
    st.session_state.show_add_task = False
    st.session_state.show_add_focus = False
    st.session_state.show_add_tone = False
    st.session_state.show_add_style = False

def get_available_models() -> Dict[str, list]:
    """
    Get available models based on API keys.
    
    Returns:
        Dictionary mapping service names to lists of available models
    """
    models = {
        "Together AI": [],
        "OpenAI": []
    }
    
    # Together.ai models
    if st.session_state.get('together_api_key'):
        models["Together AI"] = [
            "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            "google/gemma-2-27b-it",
        ]
    
    # OpenAI models
    if st.session_state.get('openai_api_key'):
        models["OpenAI"] = [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
    
    return models