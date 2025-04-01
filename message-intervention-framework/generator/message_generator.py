"""
*** Llama 3.3 70B-based Message Generator implementation using Together.ai ***

This module provides an Llama 3.3 70B-based message generator for psychological concepts or constructs.
1. It incorporates generation techniques using specific prompt, differentiation between competing constructs, examples
2. It improves the generated messages based on evaluator feedback
3. It includes enhanced diversity mechanisms and score improvement strategies

Key Components:
- LlamaGenerator: Main class that handles message generation using the Together.ai API

Functions:
- __init__: Initializes the generator with model parameters and API key
- generate_message: Generates a single message for a specified construct with optional custom parameters
- improve_message: Improves an existing message based on evaluator feedback with specific strategies
- _check_forbidden_terms: Checks if a message contains forbidden psychological terminology
- _clean_message: Cleans up the generated message by removing prefixes and quotes
"""

import os
import random
from dotenv import load_dotenv
from together import Together
from langchain_together import Together as LangchainTogether
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from common.constants import game_context, task_contexts, all_constructs
from common.prompt_components import (
    DEFAULT_GENERATION_PROMPT,
    DIVERSITY_GENERATION_PROMPT,
    IMPROVEMENT_PROMPT,
    CLOSE_TO_TARGET_PROMPT,
    STANDARD_IMPROVEMENT_PROMPT
)

# Load environment variables from .env file
load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

class LlamaGenerator:
    """Generator that uses Llama 3.3 70B model to create messages aligned with specific constructs."""
    
    def __init__(self, model="meta-llama/Llama-3.3-70B-Instruct-Turbo", temperature=0.3, top_p=0.95):
        """Initialize the generator with model parameters.
        
        Args:
            model (str): The Llama model to use
            temperature (float): Temperature for generation (higher = more creative)
            top_p (float): Top-p sampling parameter
        """
        self.model_name = model
        self.temperature = temperature
        self.original_temperature = temperature  # Store original temperature for reset
        self.top_p = top_p
        self.api_key = TOGETHER_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Together.ai API token is required. Set the TOGETHER_API_KEY environment variable."
            )
        
        # Create the Together.ai client
        self.client = Together(api_key=self.api_key)
        
    def get_llm(self):
        """Return the Llama 3.3 70B language model from Together.ai."""
        return LangchainTogether(
            model=self.model_name,
            temperature=self.temperature,
            top_p=self.top_p,
            together_api_key=self.api_key,
        )
        
    def _check_forbidden_terms(self, message):
        """Check if the message contains any forbidden terms that could prime participants."""
        forbidden_terms = [
            "descriptive norm", "injunctive norm", "cognitive dissonance", "self-determination", 
            "cheating", "cheat", "collaborate", "collaborative", "social sanction",
            "autonomy", "competence", "relatedness", "self-concept", "dissonance arousal",
            "dissonance reduction", "performance accomplishment", "vicarious experience",
            "efficacy expectation", "emotional arousal", "reference group identification"
        ]
        
        for term in forbidden_terms:
            if term.lower() in message.lower():
                return True, term
        
        return False, None
    
    def generate_message(self, construct_name, context=None, generation_instruction=None, 
                    construct_description=None, construct_examples=None, 
                    construct_differentiation=None, diversity_mode=False, previous_messages=None):
        """Generate a message aligned with the specified construct using custom parameters.
        
        Args:
            construct_name (str): The name of the psychological construct
            context (str, optional): Custom context to use
            generation_instruction (str, optional): Custom generation instruction
            construct_description (str, optional): Custom construct description
            construct_examples (list, optional): Custom construct examples
            construct_differentiation (str, optional): Custom differentiation text
            diversity_mode (bool): Whether to use diversity-enhanced generation
            previous_messages (list): Previously generated messages to avoid similarity
            
        Returns:
            str: Generated message
        """
        # Use default values from constants if not provided
        if construct_name not in all_constructs and not all([
            context, construct_description, construct_examples]):
            raise ValueError(f"Unknown construct: {construct_name}")
        
        construct_info = all_constructs.get(construct_name, {})
        
        if context is None:
            if hasattr(self, 'current_context') and self.current_context:
                context = self.current_context
            elif task_contexts:
                context = random.choice(task_contexts)
            else:
                context = game_context
                
        # Store the current context for future reference
        self.current_context = context
        
        if construct_description is None:
            construct_description = construct_info.get("description", "")
        
        if construct_examples is None:
            construct_examples = construct_info.get("examples", [])
        
        if construct_differentiation is None:
            differentiation = construct_info.get("differentiation", {})
            construct_differentiation = ""
            for _, diff_description in differentiation.items():
                construct_differentiation += f"- {diff_description}\n"
        
        if generation_instruction is None:
            generation_instruction = (
                f"Create a message that strongly aligns with the psychological construct of {construct_name}. "
                f"The message should exemplify the core elements of {construct_name} and avoid elements of differentiated constructs. "
                f"Ensure the message encourages honest effort and authentic skill development."
            )
            
        # Special generator instructions for certain constructs
        if construct_name == "Cognitive inconsistency":
            additional_instruction = "Focus ONLY on recognition of contradictions WITHOUT emotional reactions or resolution attempts."
            generation_instruction += additional_instruction
        elif construct_name == "Dissonance arousal":
            additional_instruction = "Focus ONLY on emotional discomfort WITHOUT mentioning recognition or resolution."
            generation_instruction += additional_instruction
        elif construct_name == "Dissonance reduction":
            additional_instruction = "Focus ONLY on resolution strategies WITHOUT focusing on the initial recognition or emotional discomfort."
            generation_instruction += additional_instruction
        
        # Format the examples as a string
        examples_text = ""
        for i, example in enumerate(construct_examples, 1):
            examples_text += f"{i}. \"{example}\"\n"
        
        # Choose diversity focus if in diversity mode
        diversity_focus = ""
        if diversity_mode:
            diversity_focuses = [
                "how this construct relates to personal growth over time",
                "how this construct manifests in challenging situations",
                "the internal experience of this construct",
                "the long-term benefits of embodying this construct",
                "how this construct relates to authentic achievement",
                "the relationship between this construct and perseverance",
                "how this construct connects to personal values and integrity"
            ]
            diversity_focus = random.choice(diversity_focuses)
            
            # Create the prompt with diversity emphasis
            generation_prompt = DIVERSITY_GENERATION_PROMPT.format(
                context=context,
                construct_name=construct_name,
                construct_description=construct_description,
                construct_examples=examples_text,
                construct_differentiation=construct_differentiation,
                generation_instruction=generation_instruction,
                diversity_focus=diversity_focus
            )
        else:
            # Create the standard prompt
            generation_prompt = DEFAULT_GENERATION_PROMPT.format(
                context=context,
                construct_name=construct_name,
                construct_description=construct_description,
                construct_examples=examples_text,
                construct_differentiation=construct_differentiation,
                generation_instruction=generation_instruction
            )
        
        # Add guidance to avoid similarity with previous messages if provided
        if previous_messages and len(previous_messages) > 0:
            previous_examples = "\n".join([f"- \"{msg}\"" for msg in previous_messages[:3]])
            
            generation_prompt += f"""

IMPORTANT: Your message should be significantly different from these previous messages:
{previous_examples}

Create a message that aligns with the same construct but uses a clearly different approach, language, and focus.
"""
        
        # Generate using the Together.ai client directly
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": generation_prompt}],
            temperature=self.temperature,
            top_p=self.top_p,
        )
        
        # Extract the message from the response
        message = response.choices[0].message.content.strip()
        
        # Clean up the message
        message = self._clean_message(message)
        
        # Check for forbidden terms
        contains_forbidden, term = self._check_forbidden_terms(message)
        if contains_forbidden:
            # Create a prompt to regenerate without the forbidden term
            improvement_prompt = f"""
Your message contains the term "{term}" which should be avoided.
Please rephrase without using this specific terminology while 
maintaining the same core meaning about {construct_name}.

Original message: "{message}"

IMPORTANT: Keep each sentence under 15 words for better readability. Break longer ideas into multiple short sentences.

Improved message:
"""
            
            # Regenerate message
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": improvement_prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
            )
            
            message = response.choices[0].message.content.strip()
            message = self._clean_message(message)
        
        return message
    
    def generate_messages(self, construct_name, num_messages=3):
        """Generate multiple messages aligned with the specified construct.
        
        Args:
            construct_name (str): The name of the psychological construct
            num_messages (int): Number of messages to generate
            
        Returns:
            list: Generated messages
        """
        messages = []
        
        for i in range(num_messages):
            # Use diversity mode for subsequent messages
            diversity_mode = (i > 0)
            
            # Choose a different context for each message
            if task_contexts:
                context = random.choice(task_contexts)
            else:
                context = game_context
                
            # Vary temperature slightly for diversity
            if diversity_mode:
                self.temperature = min(0.9, self.original_temperature + (0.1 * i))
            
            message = self.generate_message(
                construct_name, 
                context=context, 
                diversity_mode=diversity_mode,
                previous_messages=messages
            )
            
            messages.append(message)
            
            # Reset temperature
            self.temperature = self.original_temperature
        
        return messages
    
    def improve_message(self, current_message, feedback, target_score_threshold=85.0, current_score=None, 
                       previous_messages=None):
        """Improve an existing message with more targeted guidance.
        
        Args:
            current_message: The message to improve
            feedback: Feedback dictionary from evaluator
            target_score_threshold: Target score to reach
            current_score: Current score of the message
            previous_messages: List of previous messages to ensure diversity
            
        Returns:
            str: Improved message
        """
        # Extract key feedback elements
        context = feedback.get("context", self.current_context if hasattr(self, 'current_context') else game_context)
        generation_instruction = feedback.get("generation_instruction", "")
        top_competing_construct = feedback.get("top_competing_construct", "")
        differentiation_tip = feedback.get("differentiation_tip", "")
        score_improvement_strategy = feedback.get("score_improvement_strategy", "")
        
        # Determine if we're in conservative mode (high current score)
        conservative_mode = current_score is not None and current_score >= target_score_threshold + 5
        close_to_target = current_score is not None and target_score_threshold - 5 <= current_score < target_score_threshold
        
        # Create a customized improvement prompt based on current score
        if current_score is not None and current_score >= 80:
            # For high-scoring messages, provide more specific guidance to reach 90%+
            conservatism_guidance = "Make only minimal refinements to enhance alignment without changing the core message." if conservative_mode else "Improve the message while maintaining its core alignment with the construct."
            
            improvement_prompt = IMPROVEMENT_PROMPT.format(
                current_message=current_message,
                current_score=current_score,
                context=context,
                generation_instruction=generation_instruction,
                score_improvement_strategy=score_improvement_strategy,
                top_competing_construct=top_competing_construct,
                differentiation_tip=differentiation_tip,
                conservatism_guidance=conservatism_guidance
            )
        elif close_to_target:
            # For messages close to the target threshold, provide focused guidance
            improvement_prompt = CLOSE_TO_TARGET_PROMPT.format(
                current_message=current_message,
                current_score=current_score,
                target_score_threshold=target_score_threshold,
                context=context,
                generation_instruction=generation_instruction,
                score_improvement_strategy=score_improvement_strategy,
                top_competing_construct=top_competing_construct,
                differentiation_tip=differentiation_tip
            )
        else:
            # Standard improvement prompt for lower scores
            differentiation_guidance = f"Better differentiate from {top_competing_construct} by: {differentiation_tip}" if top_competing_construct else "Ensure the message is distinct from other psychological constructs"
            improvement_strategy = score_improvement_strategy if score_improvement_strategy else "Make the message more clearly align with the core construct"
            
            improvement_prompt = STANDARD_IMPROVEMENT_PROMPT.format(
                current_message=current_message,
                context=context,
                generation_instruction=generation_instruction,
                score_improvement_strategy=improvement_strategy,
                differentiation_guidance=differentiation_guidance
            )
        
        # Add previous messages to avoid similarity if provided
        if previous_messages and len(previous_messages) > 0:
            previous_examples = "\n".join([f"- \"{msg}\"" for msg in previous_messages[:2]])
            
            improvement_prompt += f"""

Also, ensure your improved message is distinct from these other messages:
{previous_examples}
"""
        
        # Generate improved message
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": improvement_prompt}],
            temperature=self.temperature,
            top_p=self.top_p,
        )
        
        improved_message = response.choices[0].message.content.strip()
        
        # Clean up the message
        improved_message = self._clean_message(improved_message)
        
        # Check for forbidden terms
        contains_forbidden, term = self._check_forbidden_terms(improved_message)
        if contains_forbidden:
            # Create a prompt to regenerate without the forbidden term
            term_improvement_prompt = f"""
Your improved message contains the term "{term}" which should be avoided.
Please rephrase without using this specific terminology while 
maintaining the same core meaning.

Current message to improve: "{improved_message}"

IMPORTANT: Keep each sentence under 15 words for better readability. Break longer ideas into multiple short sentences.

Revised message:
"""
            
            # Regenerate message
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": term_improvement_prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
            )
            
            improved_message = response.choices[0].message.content.strip()
            improved_message = self._clean_message(improved_message)
        
        return improved_message

    def _clean_message(self, message):
        """Clean up generated message by removing prefixes, quotes, etc."""
        # Remove common prefixes
        prefixes = [
            "Here's an improved message:", 
            "Improved message:", 
            "Here is the improved message:",
            "Here's a message:",
            "Message:",
            "Here is a message that",
            "Here's my message:"
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
        
        return message