"""
Text generation service module.
Handles interactions with language model APIs to generate messages.
"""

import logging
from typing import Dict, Any, Callable, Tuple, Optional

from openai import OpenAI
from together import Together

logger = logging.getLogger(__name__)

class TextGenerationService:
    """Service for text generation using different language model providers."""
    
    def __init__(self, together_api_key: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
        Initialize the text generation service.
        
        Args:
            together_api_key: API key for Together.ai
            openai_api_key: API key for OpenAI
        """
        self.together_api_key = together_api_key
        self.openai_api_key = openai_api_key
        self.together_client = None
        self.openai_client = None
        
        # Initialize clients if API keys are provided
        if together_api_key:
            try:
                self.together_client = Together(api_key=together_api_key)
                logger.info("Together.ai client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Together.ai client: {e}")
        
        if openai_api_key:
            try:
                self.openai_client = OpenAI(api_key=openai_api_key)
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def setup_generator(self, model: str, temperature: float = 0.7, top_p: float = 0.95) -> Tuple[Callable, Dict[str, Any]]:
        """
        Set up the text generator function and configuration.
        
        Args:
            model: Name of the language model to use
            temperature: Temperature setting for generation
            top_p: Top P setting for generation
            
        Returns:
            Tuple containing the generator function and its configuration
        """
        # Configure model parameters
        generator_config = {
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": 2048
        }
        
        # Detect the model provider based on the model name
        is_openai_model = model.startswith(("gpt-", "text-"))
        is_together_model = model.startswith(("meta-llama", "gemma"))
        
        def generate_text(prompt: str) -> str:
            """
            Generate text using the appropriate API based on the model.
            
            Args:
                prompt: The prompt to generate text from
                
            Returns:
                The generated text
            """
            try:
                # Choose API based on model and available clients
                if is_openai_model and self.openai_client:
                    response = self.openai_client.chat.completions.create(
                        model=generator_config["model"],
                        messages=[{"role": "user", "content": prompt}],
                        temperature=generator_config["temperature"],
                        top_p=generator_config["top_p"],
                        max_tokens=generator_config["max_tokens"]
                    )
                    return response.choices[0].message.content.strip()
                    
                elif self.together_client:
                    response = self.together_client.chat.completions.create(
                        model=generator_config["model"],
                        messages=[{"role": "user", "content": prompt}],
                        temperature=generator_config["temperature"],
                        top_p=generator_config["top_p"],
                        max_tokens=generator_config["max_tokens"]
                    )
                    return response.choices[0].message.content.strip()
                    
                else:
                    logger.error("No appropriate API client available for the specified model")
                    return "Error: No appropriate API client available for the specified model"
                    
            except Exception as e:
                logger.error(f"Error generating text: {e}")
                return f"Error generating text: {str(e)}"
        
        if not (self.together_client or self.openai_client):
            logger.warning("No API keys provided. Text generation will not be available.")
            generate_text = lambda prompt: "Error: API key missing - unable to generate text"
        
        return generate_text, generator_config

def clean_message(message: str) -> str:
    """
    Clean up generated message by removing prefixes, quotes, etc.
    
    Args:
        message: The raw message to clean
        
    Returns:
        The cleaned message
    """
    # Remove common prefixes
    prefixes = [
        "Here's an improved message:",
        "Improved message:",
        "Here is the improved message:",
        "Here's a message:",
        "Message:",
        "Here is a message that",
        "Here's my message:",
        "Here is my response:",
        "Here is the message:"
    ]

    for prefix in prefixes:
        if message.startswith(prefix):
            message = message[len(prefix):].strip()

    # Remove surrounding quotes
    if (message.startswith('"') and message.endswith('"')) or \
       (message.startswith("'") and message.endswith("'")):
        message = message[1:-1]

    # Remove trailing quoted attribution
    if message.endswith('"'):
        last_quote_start = message.rfind('"', 0, -1)
        if last_quote_start != -1 and last_quote_start > len(message) // 2:
            message = message[:last_quote_start].strip()

    return message.strip()