
"""
*** Llama 3.3 70B-based Message Generator implementation using Together.ai ***

This module provides an Llama 3.3 70B-based message generator for psychological concepts or constructs.
1. It incorporates generation techniques using specific prompt, differentiation between competing constructs, examples
2. It improves the generated messages based on evaluator feedback

Key Components:
- LlamaGenerator: Main class that handles message generation using the Together.ai API

Functions:
- __init__: Initializes the generator with model parameters and API key
- generate_message: Generates a single message for a specified construct with optional custom parameters
- improve_message: Improves an existing message based on evaluator feedback with enhanced strategies
- _check_forbidden_terms: Checks if a message contains forbidden psychological terminology
- _clean_message: Cleans up the generated message by removing prefixes and quotes
"""

import os
from dotenv import load_dotenv
from together import Together
from langchain_together import Together as LangchainTogether
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from common.constants import game_context, all_constructs

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
        self.top_p = top_p
        self.api_key = TOGETHER_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Together.ai API token is required. Set the TOGETHER_API_KEY environment variable."
            )
        
        # Create the Together.ai client
        self.client = Together(api_key=self.api_key)
        
        # Create the default generation prompt
        self.default_generation_prompt = """
        Context: {context}
        
        I need you to craft a message that strongly aligns with the psychological construct of {construct_name}.
        
        Here is the detailed description of {construct_name}:
        {construct_description}
        
        Here are examples of messages that exemplify {construct_name}:
        {construct_examples}
        
        This construct is differentiated from other constructs in these ways:
        {construct_differentiation}
        
        {generation_instruction}
        
        Create exactly one message that is 2-3 sentences long, using simple, conversational and natural language at approximately an 8th-grade reading level. Avoid complex vocabulary, jargon, or academic phrasing. The message should be easily understood by the average person while still conveying the core principles of {construct_name}.
        """
    
    # def get_llm(self):
    #     """Return the Llama 3.3 70B language model from Together.ai."""
    #     return LangchainTogether(
    #         model=self.model_name,
    #         temperature=self.temperature,
    #         top_p=self.top_p,
    #         # max_tokens=512,
    #         together_api_key=self.api_key,
    #     )
        
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
                    construct_differentiation=None):
        """Generate a message aligned with the specified construct using custom parameters.
        
        Args:
            construct_name (str): The name of the psychological construct
            context (str, optional): Custom context to use
            generation_instruction (str, optional): Custom generation instruction
            construct_description (str, optional): Custom construct description
            construct_examples (list, optional): Custom construct examples
            construct_differentiation (str, optional): Custom differentiation text
            
        Returns:
            str: Generated message
        """
        # Use default values from constants if not provided
        if construct_name not in all_constructs and not all([
            context, construct_description, construct_examples]):
            raise ValueError(f"Unknown construct: {construct_name}")
        
        construct_info = all_constructs.get(construct_name, {})
        
        if context is None:
            context = game_context
        
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
                f"The message should exemplify the core elements of {construct_name} and avoid elements of differentiated constructs."
            )
        """Special generator for CDT constructs with enhanced differentiation."""
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
        
        # Create the prompt
        generation_prompt = self.default_generation_prompt.format(
            context=context,
            construct_name=construct_name,
            construct_description=construct_description,
            construct_examples=examples_text,
            construct_differentiation=construct_differentiation,
            generation_instruction=generation_instruction
        )
        
        # Generate using the Together.ai client directly
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": generation_prompt}],
            temperature=self.temperature,
            top_p=self.top_p,
            # max_tokens=512
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
            
            Improved message:
            """
            
            # Regenerate message
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": improvement_prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
                # max_tokens=512
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
        
        for _ in range(num_messages):
            message = self.generate_message(construct_name)
            messages.append(message)
        
        return messages
    
    def improve_message(self, current_message, feedback, target_score_threshold=85.0, current_score=None):
        """Improve an existing message with more targeted guidance."""
        # Extract key feedback elements
        context = feedback.get("context", game_context)
        generation_instruction = feedback.get("generation_instruction", "")
        
        # Determine if we're in conservative mode (high current score)
        conservative_mode = current_score is not None and current_score >= target_score_threshold + 5
        
        # Create a more focused improvement prompt
        improvement_prompt = f"""
        Current message: "{current_message}"
        
        Context: {context}
        
        Instruction: {generation_instruction}
        
        {'IMPORTANT: Make only MINIMAL changes to refine this message.' if conservative_mode else 'IMPORTANT: Improve this message while maintaining its core meaning.'}
        
        {'1. This message already scores well, so preserve its core meaning and structure.' if conservative_mode else '1. Keep elements that strongly align with the intended construct'}
        2. Focus on addressing the specific feedback: {feedback.get("differentiation_tip", "")}
        {'3. Change only specific phrases that could be improved, not the entire message.' if conservative_mode else '3. Maintain similar length and natural, motivational tone'}
        
        Provide the improved message only.
        """
        
        # Generate improved message
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": improvement_prompt}],
            temperature=self.temperature,
            top_p=self.top_p,
            # max_tokens=512
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
            
            Revised message:
            """
            
            # Regenerate message
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": term_improvement_prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
                # max_tokens=512
            )
            
            improved_message = response.choices[0].message.content.strip()
            improved_message = self._clean_message(improved_message)
        
        return improved_message

    def _clean_message(self, message):
        """Clean up generated message by removing prefixes, quotes, etc."""
        # Remove common prefixes
        prefixes = ["Here's an improved message:", "Improved message:", "Here is the improved message:"]
        for prefix in prefixes:
            if message.startswith(prefix):
                message = message[len(prefix):].strip()
        
        # Remove surrounding quotes
        if (message.startswith('"') and message.endswith('"')) or \
        (message.startswith("'") and message.endswith("'")):
            message = message[1:-1]
        
        return message