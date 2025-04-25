"""
Message workflow module with enhanced semantic similarity checks.
Manages the workflow for generating and refining messages.
"""

import logging
import time
from typing import Dict, Any, Callable, List, Optional, Tuple
import streamlit as st

from services.generator import clean_message
from workflow.prompt_builder import create_single_message_prompt

logger = logging.getLogger(__name__)


class MessageWorkflow:
    """Manages the workflow for generating and refining psychological concept messages."""
    
    def __init__(
        self,
        concept_name: str,
        concept_info: Dict[str, Any],
        context: str,
        diversity_focus: str,
        tone: str,
        message_style: str,
        generate_text: Callable,
        evaluate_message: Callable,
        generator_config: Dict[str, Any],
        evaluator_config: Dict[str, Any]
    ):
        """
        Initialize a new message generation workflow.
        
        Args:
            concept_name: Name of the psychological concept
            concept_info: Information about the concept
            context: Task context for the message
            diversity_focus: Focus area for the message (renamed to Message Focus in UI)
            tone: Desired tone for the message
            message_style: Structural style for the message
            generate_text: Function for generating text
            evaluate_message: Function for evaluating messages
            generator_config: Configuration for text generation
            evaluator_config: Configuration for message evaluation
        """
        # Workflow parameters
        self.concept_name = concept_name
        self.concept_info = concept_info
        self.context = context
        self.diversity_focus = diversity_focus  # We keep the variable name for compatibility
        self.tone = tone
        self.message_style = message_style
        self.message_length = 3 
        self.num_messages = 3  # Default number of messages to generate
        
        # Service functions
        self.generate_text = generate_text
        self.evaluate_message = evaluate_message
        
        # Configuration
        self.generator_config = generator_config
        self.evaluator_config = evaluator_config
        
        # Workflow state
        self.current_message_number = 1
        self.current_iteration = 1
        self.message_history = []
        self.feedback_history = []
        self.evaluation_history = []
        self.final_messages = []
        self.iterations_per_message = []
        
        # Metrics
        self.generation_time = None
        self.evaluation_time = None
        self.current_human_rating = None
        
        logger.info(f"Initialized workflow for concept: {concept_name} with generator: {generator_config['model']} and evaluator: {evaluator_config['model']}")
    
    def check_forbidden_terms(self, message):
        """
        Check if the message contains any forbidden terms that could prime participants.
        
        Args:
            message: The message to check
            
        Returns:
            Tuple of (contains_forbidden_term, term_found)
        """
        forbidden_terms = [
            # Theory names
            "self-determination theory", "cognitive dissonance theory", "social norm theory", "self-efficacy theory",
            
            # Concept names (full and partial matches)
            "descriptive norm", "injunctive norm", "cognitive dissonance", "self-determination", 
            "social sanction", "autonomy", "competence", "relatedness", "self-concept", 
            "dissonance arousal", "dissonance reduction", "performance accomplishment", 
            "vicarious experience", "verbal persuasion", "emotional arousal", 
            "reference group identification", "efficacy expectation",
            
            # Study-related terms
            "experiment", "study", "research", "participant", "condition", "manipulation",
            "control group", "experimental", "hypothesis"
        ]
        
        # Check for exact matches (case insensitive)
        message_lower = message.lower()
        for term in forbidden_terms:
            if term.lower() in message_lower:
                return True, term
        
        return False, None
    
    def check_message_diversity(self, message):
        """
        Check if a message is sufficiently diverse from previously finalized messages.
        
        Args:
            message: The message to check
            
        Returns:
            Dict containing similarity information and diversity status
        """
        # Skip if no similarity service or no previous messages
        if 'similarity_service' not in st.session_state or not self.final_messages:
            return {"is_diverse": True, "max_similarity": 0.0}
        
        # Use the similarity service to check diversity
        similarity_result = st.session_state.similarity_service.check_message_diversity(
            message, self.final_messages
        )
        
        return similarity_result
    
    def generate_message_iteration(self):
        """
        Generate a new iteration of the message based on workflow state.
        
        Returns:
            The generated message
        """
        # Get existing messages for this concept from MongoDB if available
        existing_concept_messages = []
        if 'mongodb_service' in st.session_state:
            existing_concept_messages = st.session_state.mongodb_service.get_messages_by_concept(self.concept_name)
            logger.info(f"Retrieved {len(existing_concept_messages)} existing messages for concept: {self.concept_name}")
        
        # Create the prompt based on workflow state
        prompt = create_single_message_prompt(
            concept_name=self.concept_name,
            concept_info=self.concept_info,
            context=self.context,
            diversity_focus=self.diversity_focus,
            tone=self.tone,
            message_style=self.message_style,
            message_length=self.message_length, 
            current_iteration=self.current_iteration,
            previous_message=self.message_history[-1] if self.message_history else None,
            human_feedback=self.feedback_history[-1] if self.feedback_history else None,
            llm_evaluation=self.evaluation_history[-1] if self.evaluation_history else None,
            final_messages=self.final_messages,
            all_concept_messages=existing_concept_messages
        )
        
        # Generate the message
        start_time = time.time()
        max_attempts = 3  # Allow up to 3 attempts to generate a message without forbidden terms
        
        for attempt in range(1, max_attempts + 1):
            try:
                raw_message = self.generate_text(prompt)
                
                # Clean up the message
                message = clean_message(raw_message)
                
                # Check for forbidden terms
                has_forbidden, forbidden_term = self.check_forbidden_terms(message)
                
                if has_forbidden:
                    logger.warning(f"Attempt {attempt}: Generated message contains forbidden term '{forbidden_term}'. Regenerating...")
                    
                    # If this isn't the last attempt, try again with a modified prompt
                    if attempt < max_attempts:
                        # Add specific instruction to avoid forbidden terms
                        prompt += f"\n\nIMPORTANT: Do not use the term '{forbidden_term}' or any similar theoretical terms in your message."
                        continue
                    else:
                        # Last attempt - log warning but accept the message
                        logger.warning(f"Warning: Used message with forbidden term '{forbidden_term}' after {max_attempts} attempts")
                
                # Check similarity with previous messages if this is a new message (not an iteration of current)
                if self.current_iteration == 1 and len(self.final_messages) > 0:
                    similarity_result = self.check_message_diversity(message)
                    
                    # If not diverse enough and not the last attempt, try again with more emphasis on diversity
                    if not similarity_result["is_diverse"] and attempt < max_attempts:
                        logger.warning(f"Attempt {attempt}: Generated message too similar to previous messages (similarity: {similarity_result['max_similarity']:.2f}). Regenerating...")
                        
                        # Add specific instruction to increase diversity
                        prompt += f"\n\nIMPORTANT: Your message is too similar to previously accepted messages. Please make it significantly more different using new phrasing, structure, and examples, while still maintaining alignment with the concept {self.concept_name}."
                        continue
                
                # Check similarity with messages from the database
                if len(existing_concept_messages) > 0 and 'similarity_service' in st.session_state:
                    cross_user_similarity = st.session_state.similarity_service.check_message_diversity(
                        message, existing_concept_messages
                    )
                    
                    if not cross_user_similarity["is_diverse"] and attempt < max_attempts:
                        logger.warning(f"Attempt {attempt}: Generated message too similar to messages from other users (similarity: {cross_user_similarity['max_similarity']:.2f}). Regenerating...")
                        prompt += f"\n\nIMPORTANT: Your message is too similar to messages already created by other users. Make it significantly more different by using entirely new phrasing, structure, and examples."
                        continue
                
                # If we reach here, either the message is acceptable or we've tried the maximum attempts
                self.generation_time = time.time() - start_time
                
                # Log metrics
                logger.info(f"Message generated in {self.generation_time:.2f} seconds")
                
                # Update the workflow state
                self.message_history.append(message)
                
                return message
                    
            except Exception as e:
                self.generation_time = time.time() - start_time
                logger.error(f"Error generating message: {e}")
                error_message = f"Error generating message: {str(e)}"
                self.message_history.append(error_message)
                return error_message
    
    def evaluate_current_message(self) -> Dict[str, Any]:
        """
        Evaluate the current message iteration.
        
        Returns:
            Dictionary containing evaluation results
        """
        # Get the current message
        current_message = self.message_history[-1]
        
        # Evaluate the message
        start_time = time.time()
        try:
            evaluation = self.evaluate_message(current_message, self.concept_name, self.context)
            self.evaluation_time = time.time() - start_time
            
            # Log metrics
            logger.info(f"Message evaluated in {self.evaluation_time:.2f} seconds. Score: {evaluation['score']}%")
            
        except Exception as e:
            self.evaluation_time = time.time() - start_time
            logger.error(f"Error evaluating message: {e}")
            evaluation = {
                "score": 0,
                "ratings": {self.concept_name: 0},
                "feedback": {
                    "strengths": f"Error evaluating message: {str(e)}",
                    "improvements": "Please try again or check API keys and model settings.",
                    "differentiation_tips": "N/A"
                }
            }
        
        # Update workflow state
        self.evaluation_history.append(evaluation)
        
        return evaluation
    
    def record_human_feedback(self, rating: int, feedback_text: str) -> str:
        """
        Record human feedback on the current message.
        
        Args:
            rating: Numerical rating (1-10)
            feedback_text: Textual feedback
            
        Returns:
            Formatted feedback string
        """
        # Format the feedback
        feedback = f"- Rating: {rating}/10\n- Feedback: {feedback_text}"
        
        # Update workflow state
        self.feedback_history.append(feedback)
        self.current_human_rating = rating
        
        logger.info(f"Human feedback recorded: Rating {rating}/10")
        
        return feedback
    
    def record_structured_human_feedback(self, rating: int, strengths: str, weaknesses: str, suggestions: str) -> Dict[str, Any]:
        """
        Record structured human feedback on the current message.
        
        Args:
            rating: Numerical rating (1-10)
            strengths: Strengths of the message
            weaknesses: Weaknesses of the message
            suggestions: Suggestions for improvement
            
        Returns:
            Structured feedback dictionary
        """
        # Create structured feedback
        structured_feedback = {
            "rating": rating,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
        
        # Create formatted string for compatibility with old code
        formatted_feedback = (
            f"- Rating: {rating}/10\n"
            f"- Strengths: {strengths}\n"
            f"- Weaknesses: {weaknesses}\n"
            f"- Suggestions: {suggestions}"
        )
        
        # Store both the structured and formatted versions
        structured_feedback["formatted"] = formatted_feedback
        
        # Update workflow state
        self.feedback_history.append(structured_feedback)
        self.current_human_rating = rating
        
        logger.info(f"Structured human feedback recorded: Rating {rating}/10")
        
        return structured_feedback
    
    def check_convergence(self) -> bool:
        """
        Check if the current message meets acceptance criteria.
        
        Returns:
            True if message meets acceptance criteria, False otherwise
        """
        # Get current evaluation and human rating
        current_evaluation = self.evaluation_history[-1]
        current_human_rating = self.current_human_rating
        
        if current_human_rating is None:
            return False
        
        # Convert LLM score to 10-point scale for comparison
        llm_rating = current_evaluation["score"] / 10
        
        # Check if human rating is high enough
        if current_human_rating >= 8:
            # Check if LLM score is also high enough
            if current_evaluation["score"] >= 80:
                # Check if the difference between ratings is acceptable
                if abs(llm_rating - current_human_rating) <= 1.5:
                    return True
        
        # Not converged yet
        return False
    
    def finalize_message(self) -> str:
        """
        Finalize the current message and prepare for the next one.
        
        Returns:
            The finalized message
        """
        # Get the final message
        final_message = self.message_history[-1]
        
        # Get the final evaluation
        final_evaluation = self.evaluation_history[-1] if self.evaluation_history else None
        
        # Extract evaluation score
        evaluation_score = 0
        if final_evaluation and 'score' in final_evaluation:
            evaluation_score = final_evaluation['score']
        
        # Extract top competing concepts if available
        competing_concepts = []
        if final_evaluation and 'ratings' in final_evaluation:
            # Get all concepts except the target concept
            concept_scores = [(concept, score) for concept, score in final_evaluation['ratings'].items() 
                            if concept != self.concept_name]
            # Sort by score in descending order and take top 3
            concept_scores.sort(key=lambda x: x[1], reverse=True)
            competing_concepts = [{"name": concept, "score": score} for concept, score in concept_scores[:3]]
            
            logger.info(f"Extracted top competing concepts: {competing_concepts}")
        
        # Calculate diversity metrics
        diversity_metrics = None
        
        # Save to MongoDB if service is available
        if 'mongodb_service' in st.session_state:
            # Get user ID from session state or generate one
            user_id = st.session_state.get('user_id', 'anonymous_user')
            
            # Get all previous messages from this concept from MongoDB
            previous_messages = st.session_state.mongodb_service.get_messages_by_concept(self.concept_name)
            
            # Calculate diversity metrics compared to all previous messages for this concept
            if previous_messages and 'similarity_service' in st.session_state:
                diversity_metrics = st.session_state.similarity_service.check_message_diversity(
                    final_message, previous_messages
                )
                
                # Log the diversity metrics
                logger.info(f"Message diversity metrics against all previous messages for {self.concept_name}: {diversity_metrics}")
                
                # Also check against our current final messages for this session
                if len(self.final_messages) > 0:
                    session_diversity = st.session_state.similarity_service.check_message_diversity(
                        final_message, self.final_messages
                    )
                    
                    # Combine metrics
                    if diversity_metrics:
                        diversity_metrics["session_max_similarity"] = session_diversity.get("max_similarity", 0)
                        diversity_metrics["session_average_similarity"] = session_diversity.get("average_similarity", 0)
            else:
                # If no previous messages in the database, check against our current final messages
                if len(self.final_messages) > 0 and 'similarity_service' in st.session_state:
                    diversity_metrics = st.session_state.similarity_service.check_message_diversity(
                        final_message, self.final_messages
                    )
                    
                    # Add field to indicate this is only session-based
                    if diversity_metrics:
                        diversity_metrics["only_session_metrics"] = True
            
            # Save message with metadata, diversity metrics, competing concepts, and evaluation score
            message_id = st.session_state.mongodb_service.save_message(
                message=final_message,
                concept_name=self.concept_name,
                user_id=user_id,
                context=self.context,
                focus=self.diversity_focus,
                tone=self.tone,
                style=self.message_style,
                message_length=self.message_length,
                iterations=self.current_iteration,
                evaluation_score=evaluation_score,
                diversity_metrics=diversity_metrics,
                competing_concepts=competing_concepts,
                generator_model=self.generator_config["model"],
                evaluator_model=self.evaluator_config["model"]
            )
            
            if message_id:
                logger.info(f"Message saved to MongoDB concept collection: {self.concept_name} with ID: {message_id}")
        
        # Add to final messages list
        self.final_messages.append(final_message)
        
        # Track iterations required for this message
        self.iterations_per_message.append(self.current_iteration)
        
        logger.info(f"Message #{self.current_message_number} finalized after {self.current_iteration} iterations")
        
        # Reset iteration counters
        self.current_message_number += 1
        self.current_iteration = 1
        
        # Clear current message history but keep the final messages
        self.message_history = []
        self.feedback_history = []
        self.evaluation_history = []
        
        return final_message
    
    def get_workflow_state(self) -> Dict[str, Any]:
        """
        Get the current state of the workflow.
        
        Returns:
            Dictionary representing the current workflow state
        """
        return {
            "concept_name": self.concept_name,
            "context": self.context,
            "diversity_focus": self.diversity_focus,
            "tone": self.tone,
            "message_style": self.message_style,
            "message_length": self.message_length,
            "num_messages": self.num_messages,
            "current_message_number": self.current_message_number,
            "current_iteration": self.current_iteration,
            "message_history": self.message_history,
            "feedback_history": self.feedback_history,
            "evaluation_history": self.evaluation_history,
            "final_messages": self.final_messages,
            "iterations_per_message": self.iterations_per_message,
            "generation_time": self.generation_time,
            "evaluation_time": self.evaluation_time,
            "current_human_rating": self.current_human_rating,
            "generator_config": self.generator_config,
            "evaluator_config": self.evaluator_config
        }
    
    def run_iteration(self) -> Tuple[str, Dict[str, Any]]:
        """
        Run a complete iteration of the message generation workflow.
        
        Returns:
            Tuple containing the generated message and its evaluation
        """
        # Generate message
        message = self.generate_message_iteration()
        logger.info(f"Generated message of {len(message)} characters")
        
        # Evaluate message
        evaluation = self.evaluate_current_message()
        logger.info(f"Evaluation score: {evaluation['score']}%")
        
        return message, evaluation
    
    def increment_iteration(self) -> None:
        """Increment the iteration counter for the current message."""
        self.current_iteration += 1
        logger.info(f"Moving to iteration #{self.current_iteration}")