"""
*** Message Optimizer implementation ***

This module orchestrates the iterative optimization process between message generation and 
evaluation to create messages that strongly align with psychological constructs.

Functions
- initialize_parameters: Sets up initial parameters for a construct based on its definition
- optimize_message: Runs the iterative optimization process for a single message
- optimize_multiple_messages: Orchestrates optimization of multiple messages for a construct
- _check_convergence_criteria: Determines if optimization has converged based on scores
- _identify_competing_constructs: Identifies constructs with scores competing with target
- update_parameters_with_differentiation: Updates parameters to better differentiate from competing constructs
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime
from difflib import SequenceMatcher
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any, Optional
from common.utils import plot_message_construct_barchart
from common.constants import all_constructs, task_contexts

@dataclass
class GenerationParameters:
    """Class to track and refine parameters for message generation."""
    context: str
    generation_instruction: str
    construct_description: str
    construct_examples: list
    construct_differentiation: str = ""
    iteration_history: list = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    def update_from_feedback(self, feedback):
        """Update parameters based on feedback."""
        # Store current parameters in history
        self.iteration_history.append({
            "context": self.context,
            "generation_instruction": self.generation_instruction,
            "construct_description": self.construct_description,
            "construct_examples": self.construct_examples.copy(),
            "construct_differentiation": self.construct_differentiation
        })
        
        # Update parameters based on feedback
        if isinstance(feedback, dict):
            if "context" in feedback and feedback["context"]:
                self.context = feedback["context"]
            if "generation_instruction" in feedback and feedback["generation_instruction"]:
                self.generation_instruction = feedback["generation_instruction"]
            if "construct_description" in feedback and feedback["construct_description"]:
                self.construct_description = feedback["construct_description"]
            if "construct_examples" in feedback and feedback["construct_examples"]:
                self.construct_examples = feedback["construct_examples"]
            if "construct_differentiation" in feedback and feedback["construct_differentiation"]:
                self.construct_differentiation = feedback["construct_differentiation"]
            
            # Apply score improvement strategy if available
            if "score_improvement_strategy" in feedback and feedback["score_improvement_strategy"]:
                current_instruction = self.generation_instruction
                if "Additionally" in current_instruction:
                    self.generation_instruction = current_instruction.split("Additionally")[0].strip()
                    
                self.generation_instruction += f" Additionally, {feedback['score_improvement_strategy']}"

class MessageOptimizer:
    """Optimizer that coordinates the iterative process between generation and evaluation."""
    
    def __init__(self, generator, evaluator, output_dir="optimization_results"):
        """Initialize the optimizer.
        
        Args:
            generator: The message generator
            evaluator: The message evaluator
            output_dir: Directory to store optimization results
        """
        self.generator = generator
        self.evaluator = evaluator
        self.output_dir = output_dir
        self.task_contexts = task_contexts if task_contexts else []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)                               
        
    def initialize_parameters(self, construct_name, all_constructs):
        """Initialize parameters for a construct.
        
        Args:
            construct_name: Name of the construct
            all_constructs: Dictionary of all constructs
            
        Returns:
            GenerationParameters: Initial parameters
        """
        construct_info = all_constructs.get(construct_name, {})
        construct_description = construct_info.get("description", "")
        construct_examples = construct_info.get("examples", [])
        
        # Create differentiation text
        differentiation_text = ""
        differentiation = construct_info.get("differentiation", {})
        for other_construct, diff_description in differentiation.items():
            differentiation_text += f"- {diff_description}\n"
        
        # Select a context from the available task contexts
        if self.task_contexts:
            context = random.choice(self.task_contexts)
        else:
            # Use the game context from constants if no task contexts
            from common.constants import game_context
            context = game_context
        
        # Initial generation instruction
        generation_instruction = (
            f"Create a message that strongly aligns with the psychological construct of {construct_name}. "
            f"The message should be 2-3 sentences, use natural motivational and conversational language, and be tailored to task completion contexts. "
            f"Your message should exemplify the core elements of {construct_name} and avoid elements of differentiated constructs. "
            f"Ensure the message encourages honest effort and authentic skill development."
        )
        
        return GenerationParameters(
            context=context,
            generation_instruction=generation_instruction,
            construct_description=construct_description,
            construct_examples=construct_examples,
            construct_differentiation=differentiation_text
        )
        
    def check_message_similarity(self, new_message, previous_messages, threshold=0.7):
        """Check if new message is too similar to previous ones.
        
        Args:
            new_message: New message to check
            previous_messages: List of previous messages
            threshold: Similarity threshold (0-1)
            
        Returns:
            bool: True if too similar, False otherwise
        """
        for prev_msg in previous_messages:
            # Use SequenceMatcher for a better similarity check
            similarity = SequenceMatcher(None, new_message.lower(), prev_msg.lower()).ratio()
            if similarity > threshold:
                return True
        return False
    
    def _extract_all_construct_ratings(self, evaluation_text):
        """Extract ratings for all constructs from the evaluation text.
        
        Args:
            evaluation_text: Full evaluation text
            
        Returns:
            dict: Dictionary of construct names to scores
        """
        
        # Get all construct names from constants
        from common.constants import all_constructs
        all_construct_names = list(all_constructs.keys())
        
        # Use the utility function to extract construct ratings
        from common.utils import extract_construct_ratings
        return extract_construct_ratings(evaluation_text, all_construct_names)
    
    def _check_convergence_criteria(self, 
                    target_construct: str, 
                    scores_history: List[Dict[str, float]], 
                    min_consecutive: int = 3,
                    target_score_threshold: float = 90.0,
                    score_difference_threshold: float = 30.0) -> Tuple[bool, str]:
        """Check if optimization has converged with enhanced criteria."""
        
        if len(scores_history) < min_consecutive:
            return False, "Not enough iterations yet"
            
        # Get recent scores for target construct
        recent_scores = [scores.get(target_construct, 0) for scores in scores_history[-min_consecutive:]]   
        
        # Check if target scores meet threshold
        if min(recent_scores) < target_score_threshold:
            return False, f"Target score below threshold: {min(recent_scores):.1f}%"
        
        # Check if scores are stable (no significant change in last consecutive iterations)
        score_stability = max(recent_scores) - min(recent_scores)
        if score_stability > 5.0:  # More than 5% variation
            return False, f"Scores not stable: {score_stability:.1f}% variation"
        
        # Check if differentiation is sufficient
        for scores in scores_history[-min_consecutive:]:
            target_score = scores.get(target_construct, 0)
            other_scores = {k: v for k, v in scores.items() if k != target_construct}
            if other_scores:
                next_highest = max(other_scores.values())
                if target_score - next_highest < score_difference_threshold:
                    return False, f"Insufficient differentiation: {target_score - next_highest:.1f}%"
        
        return True, "Target score consistently above threshold with sufficient differentiation"
    
    def _identify_competing_constructs(self, all_scores, target_construct, top_n=3):
        """
        Identify the top competing constructs based on their scores.
        
        Args:
            all_scores: Dictionary of construct names to scores
            target_construct: Name of the target construct
            top_n: Number of top competing constructs to return
            
        Returns:
            List of tuples (construct_name, score) of the top competing constructs
        """
        # Filter out the target construct and sort by score in descending order
        competing = [(k, v) for k, v in all_scores.items() if k != target_construct]
        competing.sort(key=lambda x: x[1], reverse=True)
        
        # Return the top n competing constructs
        return competing[:top_n]
        
    def optimize_message(self, construct_name, all_constructs, 
                    max_iterations=25, min_consecutive=3,
                    target_score_threshold=90.0, score_difference_threshold=30.0,
                    previous_messages=None):
        """Run the optimization process for a construct with improved convergence criteria."""
        print(f"\n{'='*80}\nOptimizing message for construct: {construct_name}\n{'='*80}")
        
        # Initialize parameters
        params = self.initialize_parameters(construct_name, all_constructs)
        
        # Track scores and messages
        message_scores = []  # List of score dictionaries for the target construct
        all_construct_scores_history = []  # List of dictionaries containing scores for all constructs
        messages = []
        feedbacks = []
        best_message = ""
        best_score = 0
        best_all_scores = {}
        
        # Store original generator temperature for reset
        exploration_temperature = self.generator.temperature
        previous_best_message = ""
        
        # Initialize previous messages list if not provided
        if previous_messages is None:
            previous_messages = []
        
        # Run optimization loop
        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration}/{max_iterations}:")
            
            # Implement simulated annealing - exploration phase
            if iteration > 5 and (iteration % 3 == 0) and best_score > 0:
                # Exploration phase to escape local maxima
                print("  Exploration phase: Adjusting parameters for diversity...")
                temp_boost = min(0.3, 1.0 - self.generator.temperature)  # Ensure we don't exceed 1.0
                self.generator.temperature += temp_boost
                
                # Add specific instruction to try something different
                exploration_instruction = params.generation_instruction
                exploration_instruction += " IMPORTANT: Try a completely different approach than previous messages."
                
                if random.random() < 0.5:  # 50% chance to use a different context
                    if self.task_contexts:
                        alt_context = random.choice(self.task_contexts)
                        print(f"  Using alternative context for exploration.")
                    else:
                        from common.constants import task_contexts
                        self.task_contexts = task_contexts
                        alt_context = random.choice(task_contexts)
                        
                    message = self.generator.generate_message(
                        construct_name,
                        context=alt_context,
                        generation_instruction=exploration_instruction,
                        construct_description=params.construct_description,
                        construct_examples=params.construct_examples,
                        construct_differentiation=params.construct_differentiation,
                        diversity_mode=True,
                        previous_messages=messages
                    )
                else:
                    message = self.generator.generate_message(
                        construct_name,
                        params.context,
                        exploration_instruction,
                        params.construct_description,
                        params.construct_examples,
                        params.construct_differentiation,
                        diversity_mode=True,
                        previous_messages=messages
                    )
                
                # Reset temperature for next normal iteration
                self.generator.temperature = exploration_temperature
            elif iteration == 1 or best_score < 50:  # Start fresh for first iteration or poor previous results
                print("  Generating new message...")
                message = self.generator.generate_message(
                    construct_name,
                    params.context,
                    params.generation_instruction,
                    params.construct_description,
                    params.construct_examples,
                    params.construct_differentiation,
                    diversity_mode=False,
                    previous_messages=previous_messages
                )
            else:
                # Improve the previous best message
                print("  Improving previous best message...")
                message = self.generator.improve_message(
                    best_message,
                    feedbacks[-1],
                    current_score=best_score,
                    target_score_threshold=target_score_threshold,
                    previous_messages=previous_messages
                )
            
            # Check for too much similarity with previous best message
            if previous_best_message and self.check_message_similarity(message, [previous_best_message]) and iteration > 1:
                print("  Generated message too similar to previous best. Attempting more diverse generation...")
                
                # Temporarily increase temperature to encourage diversity
                orig_temp = self.generator.temperature
                self.generator.temperature = min(0.9, self.generator.temperature + 0.2)
                
                # Add diversity instruction
                diversity_instruction = params.generation_instruction + " IMPORTANT: Generate a message that expresses the same construct but is substantially different in wording and approach."
                
                message = self.generator.generate_message(
                    construct_name,
                    params.context,
                    diversity_instruction,
                    params.construct_description,
                    params.construct_examples,
                    params.construct_differentiation,
                    diversity_mode=True,
                    previous_messages=[previous_best_message] + messages[-2:] if len(messages) >= 2 else [previous_best_message]
                )
                
                # Reset temperature
                self.generator.temperature = orig_temp
            
            messages.append(message)
            print(f"  Generated: {message}")
            
            # Evaluate message
            print("  Evaluating message...")
            evaluation = self.evaluator.evaluate_message_with_feedback(
                message,
                construct_name,
                params.context,
                params.construct_description,
                params.construct_examples,
                params.construct_differentiation
            )
            
            # Extract target construct score
            target_score = evaluation["score"]
            message_scores.append(target_score)
            
            # Extract all construct scores from the evaluation text
            all_scores = evaluation["ratings"] if "ratings" in evaluation else self._extract_all_construct_ratings(evaluation["evaluation"])
            all_construct_scores_history.append(all_scores)
            
            # Get feedback for parameter updating
            feedback = evaluation["feedback"]
            feedbacks.append(feedback)
            
            print(f"  Target Construct Score: {target_score}%")
            
            # Find the next highest construct score
            other_scores = {k: v for k, v in all_scores.items() if k != construct_name}
            if other_scores:
                next_highest = max(other_scores.items(), key=lambda x: x[1])
                print(f"  Next highest construct: {next_highest[0]} with score {next_highest[1]}%")
                print(f"  Score difference: {target_score - next_highest[1]}%")
            
            # Update best message if this one has a higher target score
            if target_score > best_score:
                previous_best_message = best_message
                best_message = message
                best_score = target_score
                best_all_scores = all_scores
                print(f"  New best message (score: {best_score}%)")
            
            # Check for convergence based on criteria
            has_converged, convergence_reason = self._check_convergence_criteria(
                construct_name,
                all_construct_scores_history,
                min_consecutive=min_consecutive,
                target_score_threshold=target_score_threshold,
                score_difference_threshold=score_difference_threshold
            )
            
            if has_converged:
                print(f"  Convergence achieved! Reason: {convergence_reason}")
                break
            else:
                print(f"  Not yet converged: {convergence_reason}")
            
            # Update parameters based on feedback with differentiation
            print("  Updating parameters with differentiation focus...")
            self.update_parameters_with_differentiation(
                params, feedback, all_scores, construct_name)
            
            # Print key competing constructs to watch
            competing = self._identify_competing_constructs(all_scores, construct_name)
            if competing:
                print(f"  Key competing constructs to differentiate from: {', '.join([c[0] for c in competing])}")
        
        # Save convergence tracking information
        convergence_messages = messages[-min_consecutive:] if len(messages) >= min_consecutive else messages
        convergence_scores = message_scores[-min_consecutive:] if len(message_scores) >= min_consecutive else message_scores
        
        # Create results
        results = {
            "construct": construct_name,
            "best_message": best_message,
            "best_score": best_score,
            "best_all_scores": best_all_scores,
            "iterations": iteration,
            "all_construct_scores_history": all_construct_scores_history,
            "messages": messages,
            "feedbacks": feedbacks,
            "final_parameters": params.to_dict(),
            "converged": has_converged,
            "convergence_reason": convergence_reason if 'convergence_reason' in locals() else "Max iterations reached",
            "convergence_messages": convergence_messages,
            "convergence_scores": convergence_scores
        }
        
        # Save results
        self._save_results(results, construct_name)
        
        # Create visualization
        self._plot_convergence(message_scores, all_construct_scores_history, construct_name)
        
        return results
    
    def optimize_multiple_messages(self, construct_name, all_constructs, num_messages=3, 
                                max_iterations=25, min_consecutive=3,
                                target_score_threshold=90.0, score_difference_threshold=30.0):
        """Optimize multiple messages for a construct with enhanced diversity.
        
        Args:
            construct_name: Name of the construct
            all_constructs: Dictionary of all constructs
            num_messages: Number of messages to optimize
            max_iterations: Maximum number of iterations per message
            min_consecutive: Minimum number of consecutive iterations meeting criteria
            target_score_threshold: Minimum score for target construct (default: 90%)
            score_difference_threshold: Minimum difference between target and next highest score (default: 30%)
            
        Returns:
            list: Optimized messages with scores
        """
        optimized_messages = []
        all_previous_messages = []
        
        for i in range(1, num_messages + 1):
            print(f"\nOptimizing message {i}/{num_messages} for {construct_name}")
            
            # Create varied parameters for each message after the first one
            if i > 1:
                # Initialize with fresh parameters but modify for diversity
                print(f"  Creating diversified parameters for message {i}...")
                params = self.initialize_parameters(construct_name, all_constructs)
                
                # Add diversity through parameter tweaking
                diversity_additions = [
                    "Focus on expressing this construct through the lens of personal growth.",
                    "Emphasize how this construct applies to overcoming specific challenges.",
                    "Frame this construct in terms of long-term development.",
                    "Highlight how this construct relates to achieving authentic results.",
                    "Connect this construct to maintaining personal integrity in task completion."
                ]
                
                # Add a specific diversity instruction
                diversity_instruction = random.choice(diversity_additions)
                params.generation_instruction = f"{params.generation_instruction} {diversity_instruction}"
                
                # Use a different context from the pool if available
                if self.task_contexts:
                    params.context = random.choice(self.task_contexts)
                
                # Modify generator temperature for creativity
                original_temp = self.generator.temperature
                generator_temp = self.generator.temperature + (random.random() * 0.2 - 0.1)  # +/- 0.1
                self.generator.temperature = max(0.1, min(0.9, generator_temp))
                
                # Pass the previous messages to avoid excessive similarity
                results = self.optimize_message(
                    construct_name,
                    all_constructs,
                    max_iterations,
                    min_consecutive,
                    target_score_threshold,
                    score_difference_threshold,
                    previous_messages=all_previous_messages
                )
                
                # Reset temperature
                self.generator.temperature = original_temp
            else:
                results = self.optimize_message(
                    construct_name,
                    all_constructs,
                    max_iterations,
                    min_consecutive,
                    target_score_threshold,
                    score_difference_threshold
                )
            
            # Calculate the score difference against next highest construct
            if results["best_all_scores"]:
                other_scores = {k: v for k, v in results["best_all_scores"].items() if k != construct_name}
                if other_scores:
                    next_highest = max(other_scores.items(), key=lambda x: x[1])
                    score_difference = results["best_score"] - next_highest[1]
                    next_highest_name = next_highest[0]
                else:
                    score_difference = None
                    next_highest_name = None
            else:
                score_difference = None
                next_highest_name = None
            
            optimized_message = {
                "message": results["best_message"],
                "score": results["best_score"],
                "iterations": results["iterations"],
                "converged": results.get("converged", False),
                "score_difference": score_difference,
                "next_highest_construct": next_highest_name
            }
            
            optimized_messages.append(optimized_message)
            
            # Add to previous messages list to ensure diversity in subsequent generations
            all_previous_messages.append(results["best_message"])
        
        return optimized_messages
    
    def _save_results(self, results, construct_name):
        """Save optimization results to a file.
        
        Args:
            results: Optimization results
            construct_name: Name of the construct
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{construct_name}_optimization_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filepath}")
    
    def _plot_convergence(self, target_scores, all_construct_scores_history, construct_name):
        """
        Create visualization showing convergence patterns, competing constructs, and a barchart of average construct scores across all iterations with error bars
        
        Args:
            target_scores: List of scores for target construct
            all_construct_scores_history: List of dictionaries containing scores for all constructs
            construct_name: Name of the target construct
        """
        # Create a figure with two subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 20), gridspec_kw={'height_ratios': [2, 1, 2]})
    
        iterations = range(1, len(target_scores) + 1)
        
        # Plot 1: Target construct score over iterations
        # ax1.plot(iterations, target_scores, marker='o', linestyle='-', color='#4285F4', linewidth=2)
        # ax1.axhline(y=85, color='#EA4335', linestyle='--', alpha=0.7, label='Target threshold (85%)')
        
        # ax1.set_title(f"Target Score Convergence for {construct_name}")
        # ax1.set_xlabel("Iteration")
        # ax1.set_ylabel("Score (%)")
        # ax1.grid(True, alpha=0.3)
        # ax1.legend()
        
        # Plot 1: Top competing constructs over iterations along with intended construct
        if all_construct_scores_history:
            # Identify top competing constructs across all iterations
            all_competing = {}
            for scores in all_construct_scores_history:
                for construct, score in scores.items():
                    if construct != construct_name:
                        if construct not in all_competing:
                            all_competing[construct] = 0
                        all_competing[construct] += score
            
            # Get top 4 competing constructs overall
            top_competing = sorted(all_competing.items(), key=lambda x: x[1], reverse=True)[:4]
            top_competing_names = [c[0] for c in top_competing]
            
            # Plot target construct
            ax1.plot(iterations, target_scores, marker='o', label=construct_name, linewidth=2)
            ax1.set_yticks(range(10, 110, 10))
            
            # Plot top competing constructs
            colors = ['#EA4335', '#FBBC05', '#34A853', '#4285F4']
            for i, comp_name in enumerate(top_competing_names):
                comp_scores = [scores.get(comp_name, 0) for scores in all_construct_scores_history]
                ax1.plot(iterations, comp_scores, marker='s', label=comp_name, 
                        color=colors[i % len(colors)], linewidth=1.5, alpha=0.8)
                
            ax1.axhline(y=85, color='#EA4335', linestyle='--', alpha=0.7, label='Target threshold (85%)')
            ax1.set_title(f"Score Trends: Target vs Top Competing Constructs")
            ax1.set_xlabel("Iteration")
            ax1.set_ylabel("Score (%)")
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Plot 2: Difference between target construct and next highest construct
        if all_construct_scores_history:
            # Calculate score differences for each iteration
            score_differences = []
            next_highest_constructs = []
            
            for scores in all_construct_scores_history:
                target_score = scores.get(construct_name, 0)
                
                # Get scores for other constructs
                other_scores = {k: v for k, v in scores.items() if k != construct_name}
                
                if other_scores:
                    # Find the highest score among other constructs
                    next_highest = max(other_scores.items(), key=lambda x: x[1])
                    next_highest_score = next_highest[1]
                    next_highest_name = next_highest[0]
                    
                    # Calculate the difference
                    score_difference = target_score - next_highest_score
                    
                    score_differences.append(score_difference)
                    next_highest_constructs.append(next_highest_name)
                else:
                    score_differences.append(0)
                    next_highest_constructs.append("None")
            
            # Plot score differences
            ax2.plot(iterations, score_differences, marker='s', linestyle='-', color='#34A853', linewidth=2)
            ax2.set_yticks(range(10, 110, 10))
            ax2.axhline(y=25, color='#FBBC05', linestyle='--', alpha=0.7, label='Difference threshold (25%)')
            
            ax2.set_title(f"Score Difference (Target vs Next Highest Construct)")
            ax2.set_xlabel("Iteration")
            ax2.set_ylabel("Score Difference (%)")
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
        # Plot 3: Add barchart of all constructs for the final iteration
        if all_construct_scores_history:
            # Get all constructs from constants
            all_construct_names = list(all_constructs.keys())
            
            # Calculate average scores and standard deviations across all iterations
            avg_scores = {}
            std_devs = {}
            
            for construct in all_construct_names:
                scores = [iteration.get(construct, 0) for iteration in all_construct_scores_history]
                avg_scores[construct] = np.mean(scores)
                std_devs[construct] = np.std(scores) if len(scores) > 1 else 0
                
            # Sort constructs by theory groups for better visualization
            constructs_by_theory = {}
            for construct in all_construct_names:
                theory = all_constructs[construct]["theory"]
                if theory not in constructs_by_theory:
                    constructs_by_theory[theory] = []
                constructs_by_theory[theory].append(construct)
                
            # Define colors for different theories
            # theory_colors = {
            #     "Self-Determination Theory (SDT)": "#4285F4",  # Blue
            #     "Cognitive Dissonance Theory (CDT)": "#EA4335", # Red
            #     "Self-Efficacy Theory (SET)": "#34A853",  # Green
            #     "Social Norm Theory (SNT)": "#FBBC05"  # Yellow
            # }
            theory_colors = {}
            
            # Create bars grouped by theory
            all_constructs_ordered = []
            theory_boundaries = []
            current_position = 0
            
            for theory, constructs in constructs_by_theory.items():
                all_constructs_ordered.extend(constructs)
                current_position += len(constructs)
                theory_boundaries.append((current_position - len(constructs)/2, theory))
                
            # Calculate values for plotting
            values = [avg_scores[c] for c in all_constructs_ordered]
            errors = [std_devs[c] for c in all_constructs_ordered]
            positions = np.arange(len(all_constructs_ordered))
            
            # Create bar colors
            colors = []
            for construct in all_constructs_ordered:
                theory = all_constructs[construct]["theory"]
                color = theory_colors.get(theory, "gray")
                
                # Highlight the target construct
                if construct == construct_name:
                    color = "darkblue"  # Special highlight for target
                    
                colors.append(color)
                
            # Create bars with error bars
            ax3.bar(positions, values, color=colors, width=0.7, alpha=0.7)
            ax3.errorbar(positions, values, yerr=errors, fmt='none', ecolor='black', 
                        capsize=4, elinewidth=1, capthick=1)
            
            # Highlight the target construct score threshold line
            # ax3.axhline(y=85, color='green', linestyle='--', alpha=0.7, label='Target score threshold (85%)')
            
            # Add theory labels
            # for position, theory in theory_boundaries:
            #     ax3.text(position, -10, theory, ha='center', fontsize=10, fontweight='bold')
            
            # Format the plot
            ax3.set_title(f"Average Construct Scores Across All Iterations", fontsize=14)
            ax3.set_ylabel("Average Score (%)", fontsize=12)
            ax3.set_ylim(0, 100)
            ax3.set_xticks(positions)
            ax3.set_xticklabels(all_constructs_ordered, rotation=45, ha='right', fontsize=9)
            
            # Highlight target construct label
            if construct_name in all_constructs_ordered:
                target_idx = all_constructs_ordered.index(construct_name)
                plt.setp(ax3.get_xticklabels()[target_idx], color='darkblue', weight='bold')
            
            # Add grid lines
            ax3.grid(axis='y', linestyle='--', alpha=0.3)
            
            # Remove top and right spines
            for spine in ['top', 'right']:
                ax3.spines[spine].set_visible(False)
        
        plt.tight_layout(pad=3.0)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{construct_name}_convergence_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"The convergence plot saved to: {filepath}")
        plt.close()
        
    def update_parameters_with_differentiation(self, params, feedback, all_scores, target_construct):
        """Update parameters with focus on the primary competing construct."""
        # Store current parameters in history
        params.iteration_history.append({
            "context": params.context,
            "generation_instruction": params.generation_instruction,
            "construct_description": params.construct_description,
            "construct_examples": params.construct_examples.copy(),
            "construct_differentiation": params.construct_differentiation
        })
        
        # Update parameters from feedback
        if isinstance(feedback, dict):
            for key in ["context", "generation_instruction", "construct_description", 
                    "construct_examples", "construct_differentiation"]:
                if key in feedback and feedback[key]:
                    setattr(params, key, feedback[key])
        
        # Identify the top competing construct only
        competing_constructs = self._identify_competing_constructs(all_scores, target_construct, top_n=1)
        
        if competing_constructs:
            # Get the top competing construct
            top_competitor, competitor_score = competing_constructs[0]
            target_score = all_scores.get(target_construct, 0)
            diff = target_score - competitor_score
            
            # Only add differentiation guidance if score difference is below threshold
            if diff < 25.0:
                from common.constants import all_constructs
                construct_info = all_constructs.get(top_competitor, {})
                description = construct_info.get("description", "")
                
                # Create focused differentiation instruction
                instruction_base = params.generation_instruction.split("Additionally")[0].strip()
                new_instruction = f"{instruction_base} Additionally, ensure the message clearly differentiates from {top_competitor} by emphasizing elements unique to {target_construct}."
                
                params.generation_instruction = new_instruction
                
                # Don't accumulate differentiation text over iterations
                # Instead, replace it with targeted guidance
                diff_text = params.construct_differentiation.split("\n\nAdditional differentiation emphasis")[0]
                diff_enhancement = f"\n\nAdditional differentiation emphasis:\nFocus on distinguishing from {top_competitor}: {description.split('.')[0]}."
                
                params.construct_differentiation = diff_text + diff_enhancement