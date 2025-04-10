"""
Prompt builder module.
Contains functions for creating generation prompts based on workflow state.
"""

from typing import Dict, Any, List, Optional, Union

def format_structured_human_feedback(human_feedback: Dict[str, Any], llm_evaluation: Optional[Dict[str, Any]] = None) -> str:
    """
    Format structured human feedback into a prompt-friendly format, including rating comparison.
    
    Args:
        human_feedback: Dictionary containing structured human feedback
        llm_evaluation: LLM evaluation results for comparison (optional)
        
    Returns:
        Formatted feedback string
    """
    if not human_feedback:
        return ""
    
    rating_comparison = ""
    if llm_evaluation and isinstance(human_feedback, dict) and "score" in llm_evaluation and "rating" in human_feedback:
        human_rating = human_feedback.get('rating', 0)
        llm_rating = llm_evaluation["score"] / 10  # Convert to 1-10 scale
        rating_diff = human_rating - llm_rating
        
        if abs(rating_diff) >= 1.5:
            if rating_diff > 0:
                rating_comparison = f"NOTE: Human rating ({human_rating}/10) is significantly HIGHER than AI evaluation ({llm_rating:.1f}/10), suggesting the message may be more aligned with the concept than AI recognized."
            else:
                rating_comparison = f"NOTE: Human rating ({human_rating}/10) is significantly LOWER than AI evaluation ({llm_rating:.1f}/10), suggesting the message may have issues the AI didn't identify."
    
    if isinstance(human_feedback, dict):
        formatted_feedback = (
            f"✓ STRENGTHS TO MAINTAIN: {human_feedback.get('strengths', 'No strengths specified')}\n\n"
            f"✗ WEAKNESSES TO ADDRESS: {human_feedback.get('weaknesses', 'No weaknesses specified')}\n\n"
            f"→ SUGGESTED IMPROVEMENTS: {human_feedback.get('suggestions', 'No specific suggestions')}\n\n"
            f"HUMAN RATING: {human_feedback.get('rating', 'Not rated')}/10"
        )
    else:
        # Handle the case where human_feedback is a string
        formatted_feedback = str(human_feedback)
    
    if rating_comparison:
        formatted_feedback += f"\n\n{rating_comparison}"
    
    return formatted_feedback


def create_single_message_prompt(
    concept_name: str,
    concept_info: Dict[str, Any],
    context: str,
    diversity_focus: str,  # Called "Message Focus" in UI but kept as diversity_focus in code
    tone: str,
    message_style: str,
    message_length: int = 3,  # Added message length parameter
    current_iteration: int = 1,
    previous_message: Optional[str] = None,
    human_feedback: Optional[Union[str, Dict[str, Any]]] = None,
    llm_evaluation: Optional[Dict[str, Any]] = None,
    final_messages: Optional[List[str]] = None
) -> str:
    """
    Create a prompt for generating a single message based on workflow state.
    
    Args:
        concept_name: Name of the target psychological concept
        concept_info: Dictionary containing information about the concept
        context: Task context for the message
        diversity_focus: Focus area for the message (called "Message Focus" in UI)
        tone: Desired tone for the message
        message_style: Structural style for the message
        message_length: Number of sentences in the message
        current_iteration: Current iteration number in the workflow
        previous_message: Previous version of the message (for refinement)
        human_feedback: Human feedback on the previous message (string or dict)
        llm_evaluation: Evaluation of the previous message by LLM
        final_messages: List of previously accepted final messages
        
    Returns:
        Formatted prompt for message generation
    """
    # Get concept description
    concept_description = concept_info.get("description", "")
    
    # Get examples for reference
    concept_examples = concept_info.get("examples", [])
    examples_text = ""
    for i, example in enumerate(concept_examples, 1):
        examples_text += f"{i}. \"{example}\"\n"
    
    # Format human feedback
    formatted_human_feedback = ""
    if human_feedback:
        if isinstance(human_feedback, dict):
            formatted_human_feedback = format_structured_human_feedback(human_feedback, llm_evaluation if current_iteration > 1 else None)
        else:
            formatted_human_feedback = human_feedback  # Legacy string format
    
    # Create the sentence length instruction
    sentence_instruction = f"Create ONE message that is {message_length} sentences long."
    
    # If this is the first iteration, create an initial generation prompt
    if current_iteration == 1:
        generation_prompt = f"""
        Create a natural, conversational message that communicates the psychological concept "{concept_name}" to be used in a "{context}" context.
        
        Definition: "{concept_description}"
        
        Message Focus: "{diversity_focus}"
        
        Tone: "{tone}"
        
        Message Style: "{message_style}"
        
        {sentence_instruction} Use natural, conversational language that sounds like something a real person would say in everyday conversation. The message should encourage honest effort and authentic skill development without explicitly mentioning the concept by name.
        
        IMPORTANT: 
        1. Do NOT mention the name of the concept or any technical psychological terminology in your message. Use ordinary language that communicates the essence of the concept without naming it.
        2. Keep each sentence of your message SHORT for better readability. Break longer ideas into multiple short sentences.
        3. AVOID complex vocabulary, long words, jargon, or academic phrasing from your message.
        4. The language of the sentences of your message should be at approximately an 6th-grade reading level
        
        For reference, here are examples of messages that exemplify {concept_name}:
        {examples_text}
        
        Your message should be original and different from these examples while maintaining alignment with the concept. It should sound like natural human speech - the kind of message a friend, mentor, or teacher might share.
        
        Be sure to use your own unique phrasing, structure, and examples rather than closely following the provided examples. Aim for a message that captures the essence of the concept but expresses it in a fresh, distinctive way.
        """
    else:
        # This is a refinement iteration, include previous message and feedback
        generation_prompt = f"""
        Refine the following message for the psychological concept "{concept_name}":
        
        Previous message: "{previous_message}"
        
        Human feedback (prioritize this feedback):
        {formatted_human_feedback}
        
        Evaluator feedback (use as supplementary guidance):
        - Score: {llm_evaluation['score']}%
        - Strengths: {llm_evaluation['feedback']['strengths']}
        - Improvements: {llm_evaluation['feedback']['improvements']}
        - Differentiation tips: {llm_evaluation['feedback']['differentiation_tips']}
        
        {sentence_instruction} Use natural, conversational language that sounds like something a real person would say. The message should encourage honest effort and authentic skill development.
        
        IMPORTANT: 
        1. Do NOT mention the name of the concept or any technical psychological terminology in your message. Use ordinary language that communicates the essence of the concept without naming it.
        2. Keep each sentence of your message SHORT for better readability. Break longer ideas into multiple short sentences.
        3. AVOID complex vocabulary, long words, jargon, or academic phrasing from your message.
        4. The language of the sentences of your message should be at approximately an 6th-grade reading level
        
        Focus specifically on addressing the human feedback while maintaining the strengths identified. Human feedback takes priority over evaluator feedback when there are differences.
        
        Remember to maintain:
        - The core concept: {concept_name} (without mentioning it explicitly)
        - Message Focus: {diversity_focus}
        - Tone: {tone}
        - Message Style: {message_style}
        """
        
    if isinstance(human_feedback, dict) and llm_evaluation:
        human_rating = human_feedback.get('rating', 5)
        llm_rating = llm_evaluation.get('score', 50) / 10
        if abs(human_rating - llm_rating) >= 1.5:
            generation_prompt += """
            
            Pay special attention to the difference between human and AI ratings. This discrepancy indicates that certain aspects of the message may be perceived differently by humans versus AI evaluation. Consider what might account for this difference and adjust your refinement accordingly.
            """
        
    # If there are previous final messages, make sure this one is different
    if final_messages:
        generation_prompt += "\n\nIMPORTANT: Create a message that is DISTINCTLY DIFFERENT from these previously accepted messages while maintaining alignment with the concept:"
        for i, prev_msg in enumerate(final_messages, 1):
            generation_prompt += f"\n{i}. \"{prev_msg}\""
        
        # Enhanced diversity instructions
        generation_prompt += """
        
        To ensure your new message is sufficiently different from these previous messages:
        
        1. Use a completely different opening approach and sentence structure
        2. Draw on different analogies, examples, or scenarios
        3. Emphasize different aspects of the concept while staying true to its core meaning
        4. Vary the phrasing patterns and vocabulary choices substantially
        5. Consider a different narrative flow or rhetorical structure
        
        The message should be recognizably distinct from the previous messages even while communicating the same underlying concept.
        """
    
    return generation_prompt