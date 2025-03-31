"""
*** GPT-4o Message Evaluator implementation ***

This module evaluates how well generated messages align with psychological constructs
and provides more consistent, actionable feedback for optimization.

This module provides a GPT-4o based message evaluator for psychological concept or constructs.
1. It uses an evaluation prompt with specific scoring (rubric) guidelines for all constructs
3. Detailed feedback structure for message improvement back to message generator
4. Score extraction and consistency checks

Functions
- __init__(): Initializes evaluator with GPT model settings
- get_llm(): Creates and returns the configured LLM instance
- evaluate_message_with_feedback(): Main function that assesses message alignment and generates improvement feedback
- _create_augmented_evaluation_prompt(): Creates prompt template with scoring guidelines
- _extract_primary_score(): Extracts numerical score for target construct
- _extract_feedback_json(): Parses structured JSON feedback from evaluation
"""

import os
import json
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from common.constants import game_context, all_constructs
from common.utils import extract_construct_ratings
# from common.prompts import create_evaluation_prompt

load_dotenv()

class GPTEvaluator:
    """Evaluator that uses GPT-4o to evaluate messages and provide optimization feedback."""
    
    def __init__(self, model="gpt-4o", temperature=0.3, top_p=0.95):
        """Initialize the evaluator.
        
        Args:
            model (str): The GPT model to use
            temperature (float): Temperature for generation
            top_p (float): Top-p sampling parameter
        """
        self.model_name = model
        self.temperature = temperature
        self.top_p = top_p
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set the OPENAI_API_KEY environment variable.")
        
        # Create evaluation prompt using the centralized function
        # self.evaluation_prompt = create_evaluation_prompt()
        
    def get_llm(self):
        """Return the GPT-4o language model."""
        return ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            top_p=self.top_p,
            api_key=self.api_key
        )
        
    def _create_augmented_evaluation_prompt(self, context, message, construct_name, 
                        construct_description, examples_text, construct_differentiation):
        """Create an augmented evaluation prompt with consistent scoring guidelines."""
        return ChatPromptTemplate.from_messages([
            ("user", """
                Context: {context}
                
                Message to evaluate: "{message}"

                Target Construct: {construct_name}

                Construct Description: {construct_description}

                Construct Examples: {examples}

                Construct Differentiation: {differentiation}
                
                SCORING GUIDELINES:
                - Be consistent in your scoring approach
                - When scoring this message, consider it in isolation without comparing to previous iterations
                - For each criterion, provide a specific score explanation with evidence from the message
                - Maintain the same standards across all evaluations
                - Focus on textual evidence rather than inferences
                
                IMPORTANT EVALUATION GUIDELINES:
                - Maintain consistency in your evaluation approach across messages
                - When a message aligns strongly with the target construct, ensure competing constructs receive proportionally lower scores
                - Be disciplined about score differences - they should reflect meaningful distinctions between constructs
                - Avoid score inflation for non-target constructs that only tangentially relate to the message

                Evaluate how well this message aligns with the target construct using these five criteria:

                1. Core Element Alignment: Does the message capture the essential psychological mechanism of the construct?
                2. Differentiation: Does the message avoid elements explicitly differentiated from this construct?
                3. Language Appropriateness: Does the message use natural, motivational language suitable for a puzzle-solving game?
                4. Conciseness: Is the message 2-3 sentences and focused?
                5. Context Relevance: Is the message well-tailored to the puzzle-solving game context?

                First, provide a detailed score for the target construct with specific reasoning.
                Use the below rubric for scoring as stated below.
                SCORING RUBRIC:
                - 90-100%: Message captures all key aspects of the construct description with appropriate emphasis while clearly avoiding elements of differentiated constructs. Message uses language that precisely captures the psychological mechanism and closely resembles the provided examples.
                - 80-89%: Message clearly invokes most of the key aspects of the construct description and largely avoids differentiated elements. Message contains similar themes to the examples with only minimal overlap with related constructs.
                - 70-79%: Message conveys some important aspects of the construct description but may include elements from one or two differentiated constructs. Message shows general similarity to examples but lacks precision.
                - 50-69%: Message only tangentially relates to the construct description and fails to maintain boundaries from differentiated constructs. Message has limited similarity to examples.
                - 0-49%: Message contradicts the construct description or primarily exemplifies differentiated constructs. Message bears little resemblance to provided examples.

                Then, score ALL the listed psychological constructs:
                {construct_list}
                
                Present your scores in this format:
                ### Construct Confidence Scores
                - Construct1: XX%
                - Construct2: XX%
                [all constructs]

                Then provide structured feedback in this JSON format:
                {{
                    "context": "Specific context improvement",
                    "generation_instruction": "Specific guidance for improvement",
                    "top_competing_construct": "Name of the most similar competing construct",
                    "differentiation_tip": "Specific tip to better differentiate from the top competing construct"
                }}
                """)
        ])
    
    def evaluate_message_with_feedback(self, message, construct_name, context=None, 
                                     construct_description=None, construct_examples=None,
                                     construct_differentiation=None):
        """Evaluate a message and provide feedback for optimization.
        
        Args:
            message (str): The message to evaluate
            construct_name (str): The target construct
            context (str, optional): Context used for generation
            construct_description (str, optional): Description of the construct
            construct_examples (list, optional): Examples of the construct
            construct_differentiation (str, optional): Differentiation text
            
        Returns:
            dict: Evaluation results including score, all construct ratings, and feedback
        """
        # Use default values from constants if not provided
        if construct_name not in all_constructs and not all([
            context, construct_description, construct_examples, construct_differentiation]):
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
        
        # Format the examples as a string
        examples_text = ""
        for i, example in enumerate(construct_examples, 1):
            examples_text += f"{i}. \"{example}\"\n"
        
        # Create augmented prompt to request explicit ratings for all constructs
        prompt = self._create_augmented_evaluation_prompt(
            context, message, construct_name, construct_description, 
            examples_text, construct_differentiation
        )
        
        # Invoke the model with the augmented prompt
        llm = self.get_llm()
        chain = prompt | llm | StrOutputParser()

        # Pass the variables to the template
        evaluation = chain.invoke({
            "context": context,
            "message": message,
            "construct_name": construct_name,
            "construct_description": construct_description,
            "examples": examples_text,
            "differentiation": construct_differentiation,
            "construct_list": "\n".join([f"- {name}" for name in all_constructs.keys()])
        })
        
        # Extract primary target construct score
        score = self._extract_primary_score(evaluation, construct_name)
        
        # Extract ratings for all constructs
        all_construct_names = all_constructs.keys()
        all_ratings = extract_construct_ratings(evaluation, all_construct_names)
        
        # Extract feedback JSON
        feedback = self._extract_feedback_json(evaluation)
        
        # Ensure feedback contains all required keys
        if isinstance(feedback, dict):
            for key in ["context", "generation_instruction", "construct_description", 
                      "construct_examples", "construct_differentiation"]:
                if key not in feedback:
                    if key == "construct_examples" and feedback.get(key) is None:
                        feedback[key] = construct_examples  # Keep original examples if not provided
                    else:
                        feedback[key] = locals().get(key, "")  # Keep original value if not provided
        else:
            # If feedback is not a dict, create default feedback
            feedback = {
                "context": context,
                "generation_instruction": f"Create a message that aligns with {construct_name}",
                "construct_description": construct_description,
                "construct_examples": construct_examples,
                "construct_differentiation": construct_differentiation
            }
        
        return {
            "message": message,
            "construct": construct_name,
            "evaluation": evaluation,
            "score": score,
            "ratings": all_ratings,
            "feedback": feedback
        }
    
    def _extract_primary_score(self, evaluation, construct_name):
        """Extract the primary score for the target construct from evaluation text.
        
        Args:
            evaluation (str): The evaluation text
            construct_name (str): The target construct name
            
        Returns:
            int: Score for the target construct
        """
        score = 0
        
        # Try to find explicit score for the target construct
        pattern = rf"{construct_name}:\s*(\d+)%"
        matches = re.findall(pattern, evaluation, re.IGNORECASE)
        
        if matches and matches[0].isdigit():
            score = int(matches[0])
            return score
        
        # If not found, look for overall score expressions
        for line in evaluation.split('\n'):
            if '%' in line and any(x in line.lower() for x in ['score', 'overall', 'rating']):
                # Try to extract a percentage
                parts = line.split('%')
                if parts and len(parts) > 0:
                    # Look for numbers before the % sign
                    number_part = parts[0].split()[-1]
                    if number_part.isdigit():
                        score = int(number_part)
                        break
        
        return score
    
    def _extract_feedback_json(self, evaluation):
        """Extract feedback JSON from the evaluation text."""
        feedback = {}
        try:
            # Look for JSON structure in the evaluation
            json_start = evaluation.find('{')
            json_end = evaluation.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = evaluation[json_start:json_end]
                feedback = json.loads(json_str)
                
                # Validate that feedback contains substantive content, not placeholders
                for key in ["context", "generation_instruction", "construct_description"]:
                    if key in feedback and (
                        feedback[key] == f"Suggested improved {key}" or 
                        feedback[key] == f"Enhanced {key}" or
                        feedback[key] == f"Refined {key}"
                    ):
                        # Replace generic feedback with the original value
                        feedback[key] = None
        except Exception as e:
            print(f"Error extracting feedback JSON: {e}")
            
        return feedback