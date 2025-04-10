"""
Message evaluation service module.
Handles interactions with language model APIs for evaluating generated messages.
"""

import json
import logging
import re
from typing import Dict, Any, Callable, Tuple, Optional

from openai import OpenAI
from together import Together

from data.concepts import ALL_conceptS

logger = logging.getLogger(__name__)

def extract_json_from_llm_response(text):
    """
    Extract valid JSON from LLM response text which may contain markdown or additional text.
    
    Args:
        text: The raw response text from the LLM
        
    Returns:
        Extracted JSON string or the original text if no JSON markers found
    """
    # Try to find JSON enclosed in code blocks first (common LLM output pattern)
    # Look for ```json ... ``` pattern
    json_code_block = re.search(r'```(?:json)?\s*({[\s\S]*?})\s*```', text)
    if json_code_block:
        return json_code_block.group(1)
    
    # Look for JSON object pattern (starting with { and ending with })
    json_pattern = re.search(r'({[\s\S]*})', text)
    if json_pattern:
        return json_pattern.group(1)
    
    # Return original if no JSON pattern found
    return text

class MessageEvaluationService:
    """Service for evaluating messages using different language model providers."""
    
    def __init__(self, together_api_key: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
        Initialize the message evaluation service.
        
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
                logger.info("Together.ai client initialized for evaluation")
            except Exception as e:
                logger.error(f"Failed to initialize Together.ai client for evaluation: {e}")
        
        if openai_api_key:
            try:
                self.openai_client = OpenAI(api_key=openai_api_key)
                logger.info("OpenAI client initialized for evaluation")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client for evaluation: {e}")
    
    def setup_evaluator(self, model: str, temperature: float = 0.2, top_p: float = 0.95) -> Tuple[Callable, Dict[str, Any]]:
        """
        Set up the message evaluator function and configuration.
        
        Args:
            model: Name of the language model to use
            temperature: Temperature setting for evaluation
            top_p: Top P setting for evaluation
            
        Returns:
            Tuple containing the evaluator function and its configuration
        """
        # Configure model parameters
        evaluator_config = {
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": 2048
        }
        
        # Detect the model provider based on the model name
        is_openai_model = model.startswith(("gpt-", "text-"))
        is_together_model = model.startswith(("meta-llama", "gemma"))
        
        def evaluate_message(message: str, concept_name: str, context: Optional[str] = None) -> Dict[str, Any]:
            """
            Evaluate a message using the appropriate API based on the model.
            
            Args:
                message: The message to evaluate
                concept_name: The name of the target psychological concept
                context: The context in which the message is used
                
            Returns:
                Dictionary containing evaluation results
            """
            # Create the evaluation prompt
            evaluation_prompt = create_evaluation_prompt(message, concept_name, context)
            
            try:
                # Choose API based on model and available clients
                if is_openai_model and self.openai_client:
                    response = self.openai_client.chat.completions.create(
                        model=evaluator_config["model"],
                        messages=[{"role": "user", "content": evaluation_prompt}],
                        temperature=evaluator_config["temperature"],
                        top_p=evaluator_config["top_p"],
                        response_format={"type": "json_object"}
                    )
                    result_text = response.choices[0].message.content
                    
                elif self.together_client:
                    # Together.ai models may not support response_format directly
                    response = self.together_client.chat.completions.create(
                        model=evaluator_config["model"],
                        messages=[
                            {"role": "user", "content": evaluation_prompt},
                            {"role": "system", "content": "Respond with valid JSON only."}
                        ],
                        temperature=evaluator_config["temperature"],
                        top_p=evaluator_config["top_p"],
                        max_tokens=evaluator_config["max_tokens"]
                    )
                    result_text = response.choices[0].message.content
                    
                else:
                    logger.error("No appropriate API client available for the specified model")
                    return {
                        "score": 0,
                        "ratings": {concept_name: 0},
                        "feedback": {
                            "strengths": "No appropriate API client available for the specified model",
                            "improvements": "No appropriate API client available for the specified model",
                            "differentiation_tips": "No appropriate API client available for the specified model"
                        }
                    }
                
                # Parse JSON response
                try:
                    # For Together.ai models, try to extract JSON from the response
                    if (is_together_model and self.together_client) or not is_openai_model:
                        result_text = extract_json_from_llm_response(result_text)
                        
                    result = json.loads(result_text)
                    if concept_name not in result.get("ratings", {}):
                        # If target concept is missing, add it using the overall score
                        if "ratings" not in result:
                            result["ratings"] = {}
                        if "score" in result:
                            result["ratings"][concept_name] = result["score"]
                        else:
                            # If no score available, default to 50
                            result["score"] = 50
                            result["ratings"] = {concept_name: 50}
                        
                    # Ensure feedback structure exists
                    if "feedback" not in result:
                        result["feedback"] = {
                            "strengths": "Feedback structure missing in evaluation response",
                            "improvements": "Feedback structure missing in evaluation response",
                            "differentiation_tips": "Feedback structure missing in evaluation response"
                        }
                    elif not isinstance(result["feedback"], dict):
                        # Convert string feedback to structured format if needed
                        feedback_text = str(result["feedback"])
                        result["feedback"] = {
                            "strengths": feedback_text,
                            "improvements": "Please refine for better concept alignment",
                            "differentiation_tips": "Ensure clear differentiation from related concepts"
                        }
                    
                    # Ensure all required feedback fields exist
                    required_fields = ["strengths", "improvements", "differentiation_tips"]
                    for field in required_fields:
                        if field not in result["feedback"]:
                            result["feedback"][field] = f"{field.capitalize()} information not provided"
                            
                    return result
                    
                except json.JSONDecodeError:
                    # Fallback if response is not valid JSON
                    logger.error(f"Error parsing evaluation response: {result_text[:200]}...")
                    return {
                        "score": 50,
                        "ratings": {concept_name: 50},
                        "feedback": {
                            "strengths": "Error parsing evaluation response",
                            "improvements": "Error parsing evaluation response",
                            "differentiation_tips": "Error parsing evaluation response"
                        }
                    }
                    
            except Exception as e:
                logger.error(f"Error evaluating message: {e}")
                return {
                    "score": 0,
                    "ratings": {concept_name: 0},
                    "feedback": {
                        "strengths": f"Error: {str(e)}",
                        "improvements": f"Error: {str(e)}",
                        "differentiation_tips": f"Error: {str(e)}"
                    }
                }
        
        if not (self.together_client or self.openai_client):
            logger.warning("No API keys provided. Evaluation will not be available.")
            evaluate_message = lambda message, concept_name, context=None: {
                "score": 0,
                "ratings": {concept_name: 0},
                "feedback": {
                    "strengths": "API key missing - unable to evaluate",
                    "improvements": "API key missing - unable to evaluate",
                    "differentiation_tips": "API key missing - unable to evaluate"
                }
            }
        
        return evaluate_message, evaluator_config

def create_evaluation_prompt(message: str, concept_name: str, context: Optional[str] = None) -> str:
    """
    Create a detailed evaluation prompt for the message.
    
    Args:
        message: The message to evaluate
        concept_name: The name of the target psychological concept
        context: The context in which the message is used
        
    Returns:
        Formatted prompt for evaluation
    """
    # Get concept info
    concept_info = ALL_conceptS.get(concept_name, {})
    
    # Check for custom concept definition in session state
    import streamlit as st
    custom_def_key = f"custom_definition_{concept_name}"
    if custom_def_key in st.session_state:
        concept_description = st.session_state[custom_def_key]
    else:
        concept_description = concept_info.get("description", "")

    # Get examples
    concept_examples = concept_info.get("examples", [])
    examples_text = ""
    for i, example in enumerate(concept_examples, 1):
        examples_text += f"{i}. \"{example}\"\n"

    # Create differentiation text
    differentiation = concept_info.get("differentiation", {})
    differentiation_text = ""
    for other_concept, diff_description in differentiation.items():
        differentiation_text += f"- {diff_description}\n"

    # Prepare evaluation prompt - using raw string to avoid issues with format specifiers
    evaluation_prompt = f"""
    Context: {context or "Task completion scenario with ethical considerations"}

    Message to evaluate: "{message}"

    Target concept: {concept_name}

    concept Description: {concept_description}

    concept Examples: {examples_text}

    concept Differentiation: {differentiation_text}

    IMPORTANT SCORING GUIDANCE:
    - Each message should align strongly with ONE primary concept - the target concept
    - When a message strongly aligns with the target concept, competing concepts MUST receive proportionally LOWER scores
    - High differentiation is essential - if target concept scores > 80%, competing concepts should score significantly lower
    - Avoid score inflation for non-target concepts - they should score at least 30% lower than the target concept
    - Be critical and demanding in your evaluation of alignment

    Evaluate how well this message aligns with the target concept {concept_name}.
    For each concept, assign a confidence score (0-100%) based on the following criteria:

    SCORING RUBRIC:
    - 95-100%: Message perfectly captures all aspects of the concept with ideal emphasis while completely avoiding elements of differentiated concepts. Message uses natural language that precisely captures the psychological mechanism and perfectly resembles the provided examples.
    - 90-94%: Message excellently captures nearly all aspects of the concept with appropriate emphasis while clearly avoiding most elements of differentiated concepts. Message uses language that very clearly captures the psychological mechanism and closely resembles the provided examples.
    - 85-89%: Message strongly captures most aspects of the concept with good emphasis while avoiding important elements of differentiated concepts. Message uses language that clearly captures the psychological mechanism and resembles the provided examples well.
    - 80-84%: Message clearly captures several key aspects of the concept and largely avoids elements of differentiated concepts. Message contains similar themes to the examples with only minimal overlap with related concepts.
    - 75-79%: Message adequately captures some important aspects of the concept but may include minor elements from differentiated concepts. Message shows similarity to examples but lacks precision in differentiating from other concepts.
    - 70-74%: Message conveys basic aspects of the concept but includes elements from one or two differentiated concepts. Message shows general similarity to examples but lacks precision.
    - 60-69%: Message only partially relates to the concept description and fails to maintain boundaries from multiple differentiated concepts. Message has limited similarity to examples.
    - 50-59%: Message tangentially relates to the concept description but primarily reflects aspects of differentiated concepts. Message has minimal similarity to examples.
    - 0-49%: Message contradicts the concept description or primarily exemplifies differentiated concepts. Message bears little resemblance to provided examples.

    Provide ratings for all psychological concepts, not just the target. Ensure proper differentiation between scores.

    Respond in this JSON format:
    {{
        "score": [score for the target concept],
        "ratings": {{
            "Autonomy": [score],
            "Competence": [score],
            "Relatedness": [score],
            "Self-concept": [score],
            "Cognitive inconsistency": [score],
            "Dissonance arousal": [score],
            "Dissonance reduction": [score],
            "Performance accomplishments": [score],
            "Vicarious experience": [score],
            "Verbal persuasion": [score],
            "Emotional arousal": [score],
            "Descriptive Norms": [score],
            "Injunctive Norms": [score],
            "Social Sanctions": [score],
            "Reference Group Identification": [score]
        }},
        "feedback": {{
            "strengths": [what the message does well],
            "improvements": [how the message could better align with the target concept],
            "differentiation_tips": [how to better differentiate from competing concepts]
        }}
    }}
    """

    return evaluation_prompt