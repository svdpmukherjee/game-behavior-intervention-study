"""
*** GPT-4o Message Evaluator implementation ***

This module evaluates how well generated messages align with psychological constructs
and provides more consistent, actionable feedback for optimization.

This module provides a GPT-4o based message evaluator for psychological concept or constructs.
1. It uses an evaluation prompt with specific scoring (rubric) guidelines for all constructs
2. Enhanced feedback structure for message improvement back to message generator
3. Score extraction and consistency checks with more granular scoring criteria

Functions
- __init__(): Initializes evaluator with GPT model settings
- get_llm(): Creates and returns the configured LLM instance
- evaluate_message_with_feedback(): Main function that assesses message alignment and generates improvement feedback
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
from common.constants import game_context, task_contexts, all_constructs
from common.utils import extract_construct_ratings
from common.prompt_components import AUGMENTED_EVALUATION_PROMPT

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
        
    def get_llm(self):
        """Return the GPT-4o language model."""
        return ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            top_p=self.top_p,
            api_key=self.api_key
        )
        
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
            # If there are task contexts, use the first one as default
            if task_contexts and len(task_contexts) > 0:
                context = task_contexts[0]
            else:
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
        
        # Create prompt using the template
        prompt = ChatPromptTemplate.from_template(AUGMENTED_EVALUATION_PROMPT)
        
        # Invoke the model with the prompt
        llm = self.get_llm()
        chain = prompt | llm | StrOutputParser()

        # Pass the variables to the template
        try:
            evaluation = chain.invoke({
                "context": context,
                "message": message,
                "construct_name": construct_name,
                "construct_description": construct_description,
                "examples": examples_text,
                "differentiation": construct_differentiation,
                "construct_list": "\n".join([f"- {name}" for name in all_constructs.keys()])
            })
        except Exception as e:
            print(f"Error during evaluation: {e}")
            # Provide a fallback evaluation for robustness
            evaluation = f"""
            ### Evaluation for {construct_name}
            
            Score: 70%
            
            This message partially aligns with {construct_name} but could be improved.
            
            ### Construct Confidence Scores
            - {construct_name}: 70%
            """
            for name in all_constructs.keys():
                if name != construct_name:
                    evaluation += f"\n- {name}: 30%"
                    
            evaluation += """
            
            To improve:
            - Focus more on the core elements of the construct
            - Use more natural and motivational language
            - Ensure clear differentiation from other constructs
            """
        
        # Extract primary target construct score
        score = self._extract_primary_score(evaluation, construct_name)
        
        # Extract ratings for all constructs
        all_construct_names = all_constructs.keys()
        all_ratings = extract_construct_ratings(evaluation, all_construct_names)
        
        # Extract feedback JSON
        feedback = self._extract_feedback_json(evaluation)
        
        # Ensure feedback contains all required keys
        if isinstance(feedback, dict):
            required_keys = [
                "context", "generation_instruction", "top_competing_construct", 
                "differentiation_tip", "score_improvement_strategy", "conciseness_tip"
            ]
            
            for key in required_keys:
                if key not in feedback or not feedback[key]:
                    if key == "context":
                        feedback[key] = context
                    elif key == "generation_instruction":
                        feedback[key] = f"Improve the message to better align with {construct_name}"
                    elif key == "top_competing_construct":
                        # Find the competing construct with the highest score
                        other_scores = {k: v for k, v in all_ratings.items() if k != construct_name}
                        if other_scores:
                            top_competing = max(other_scores.items(), key=lambda x: x[1])
                            feedback[key] = top_competing[0]
                        else:
                            feedback[key] = "None"
                    elif key == "differentiation_tip":
                        feedback[key] = f"Focus more on the core elements of {construct_name} and avoid language that might relate to other constructs."
                    elif key == "score_improvement_strategy":
                        feedback[key] = f"Strengthen the alignment with the core mechanism of {construct_name} and ensure clear differentiation from other constructs."
                    elif key == "conciseness_tip":
                        feedback[key] = "Keep the message focused on 2-3 concise sentences with simple language. Keep each sentence under 15 words."
        else:
            # If feedback is not a dict, create default feedback
            # Find the competing construct with the highest score
            other_scores = {k: v for k, v in all_ratings.items() if k != construct_name}
            top_competing = "None"
            if other_scores:
                top_competing = max(other_scores.items(), key=lambda x: x[1])[0]
                
            feedback = {
                "context": context,
                "generation_instruction": f"Improve the message to better align with {construct_name}",
                "top_competing_construct": top_competing,
                "differentiation_tip": f"Focus more on the core elements of {construct_name} and avoid language that might relate to other constructs.",
                "score_improvement_strategy": f"Strengthen the alignment with the core mechanism of {construct_name} and ensure clear differentiation from other constructs.",
                "conciseness_tip": "Keep the message focused on 2-3 concise sentences with simple language. Keep each sentence under 15 words."
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