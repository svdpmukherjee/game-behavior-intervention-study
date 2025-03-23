"""Message optimizer that iteratively refines message generation parameters with enhanced convergence criteria."""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any, Optional
from common.utils import plot_message_construct_barchart
from common.constants import all_constructs

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
        if "context" in feedback:
            self.context = feedback["context"]
        if "generation_instruction" in feedback:
            self.generation_instruction = feedback["generation_instruction"]
        if "construct_description" in feedback:
            self.construct_description = feedback["construct_description"]
        if "construct_examples" in feedback:
            self.construct_examples = feedback["construct_examples"]
        if "construct_differentiation" in feedback:
            self.construct_differentiation = feedback["construct_differentiation"]


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
        
        # Use the game context from constants
        from common.constants import game_context
        
        # Initial generation instruction
        generation_instruction = (
            f"Create a message that strongly aligns with the psychological construct of {construct_name}. "
            f"The message should be 2-3 sentences, use natural motivational language, and be tailored to the anagram game context. "
            f"Your message should exemplify the core elements of {construct_name} and avoid elements of differentiated constructs."
        )
        
        return GenerationParameters(
            context=game_context,
            generation_instruction=generation_instruction,
            construct_description=construct_description,
            construct_examples=construct_examples,
            construct_differentiation=differentiation_text
        )
    
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
                    target_score_threshold: float = 85.0,
                    score_difference_threshold: float = 25.0) -> Tuple[bool, str]:
        """Check if optimization has converged with simplified criteria."""
        
        if len(scores_history) < min_consecutive:
            return False, "Not enough iterations yet"
            
        # Get recent scores for target construct
        recent_scores = [scores.get(target_construct, 0) for scores in scores_history[-min_consecutive:]]
        
        # Check if target scores meet threshold
        if min(recent_scores) < target_score_threshold:
            return False, f"Target score below threshold: {min(recent_scores):.1f}%"
        
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
    
    def _refine_generation_instruction(self, instruction, competing_constructs):
        """
        Refine generation instruction to emphasize differentiation from competing constructs.
        
        Args:
            instruction: Original generation instruction
            competing_constructs: List of tuples (construct_name, score) of competing constructs
            
        Returns:
            Refined instruction with emphasis on differentiation
        """
        if not competing_constructs:
            return instruction
            
        # Extract names of top competing constructs
        competing_names = [c[0] for c in competing_constructs]
        competing_str = ", ".join(competing_names)
        
        # Add differentiation guidance to the instruction
        refined = f"{instruction} Additionally, ensure the message clearly differentiates from {competing_str} by emphasizing elements unique to the target construct and avoiding characteristic elements of these competing constructs."
        
        return refined
        
    def optimize_message(self, construct_name, all_constructs, 
                    max_iterations=20, min_consecutive=3,
                    target_score_threshold=85.0, score_difference_threshold=25.0):
        """Run the optimization process for a construct with enhanced convergence criteria."""
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
        
        # Run optimization loop
        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration}/{max_iterations}:")
            
            # Generate or improve message
            print("  Generating/improving message...")
            if iteration == 1 or best_score < 50:  # Start fresh for first iteration or poor previous results
                message = self.generator.generate_message(
                    construct_name,
                    params.context,
                    params.generation_instruction,
                    params.construct_description,
                    params.construct_examples,
                    params.construct_differentiation
                )
            else:
                # Improve the previous best message
                message = self.generator.improve_message(
                    best_message,
                    feedbacks[-1]  # Use the most recent feedback
                )
            
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
            all_scores = self._extract_all_construct_ratings(evaluation["evaluation"])
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
                best_message = message
                best_score = target_score
                best_all_scores = all_scores
            
            # Check for convergence based on enhanced criteria
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
            
            # Update parameters based on feedback with enhanced differentiation
            print("  Updating parameters with enhanced differentiation focus...")
            self.update_parameters_with_differentiation(
                params, feedback, all_scores, construct_name)
            
            # Print key competing constructs to watch
            competing = self._identify_competing_constructs(all_scores, construct_name)
            if competing:
                print(f"  Key competing constructs to differentiate from: {', '.join([c[0] for c in competing])}")
                
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
            "convergence_reason": convergence_reason if 'convergence_reason' in locals() else "Max iterations reached"
        }
        
        # Save results
        self._save_results(results, construct_name)
        
        # Create visualization
        self._plot_convergence(message_scores, all_construct_scores_history, construct_name)
        
        return results
    
    def optimize_multiple_messages(self, construct_name, all_constructs, num_messages=3, 
                                max_iterations=20, min_consecutive=3,
                                target_score_threshold=85.0, score_difference_threshold=25.0):
        """Optimize multiple messages for a construct.
        
        Args:
            construct_name: Name of the construct
            all_constructs: Dictionary of all constructs
            num_messages: Number of messages to optimize
            max_iterations: Maximum number of iterations per message
            min_consecutive: Minimum number of consecutive iterations meeting criteria
            target_score_threshold: Minimum score for target construct (default: 85%)
            score_difference_threshold: Minimum difference between target and next highest score (default: 25%)
            
        Returns:
            list: Optimized messages with scores
        """
        optimized_messages = []
        
        for i in range(1, num_messages + 1):
            print(f"\nOptimizing message {i}/{num_messages} for {construct_name}")
            
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
            
            optimized_messages.append({
                "message": results["best_message"],
                "score": results["best_score"],
                "iterations": results["iterations"],
                "converged": results.get("converged", False),
                "score_difference": score_difference,
                "next_highest_construct": next_highest_name
            })
        
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
                
    def _get_construct_characteristics(self, construct_name):
        """
        Get key characteristics of a construct to help with differentiation.
        This would use the construct definitions from common.constants.
        
        Args:
            construct_name: Name of the construct
            
        Returns:
            String describing key characteristics of the construct
        """
        from common.constants import all_constructs
        
        # Get the construct info
        construct_info = all_constructs.get(construct_name, {})
        
        # Extract key phrases from the description
        description = construct_info.get("description", "")
        key_phrases = []
        
        # Simple extraction of potential key phrases based on common patterns
        if "focuses on" in description:
            parts = description.split("focuses on")
            if len(parts) > 1:
                key_phrases.append(parts[1].split(".")[0].strip())
        
        if "emphasizes" in description:
            parts = description.split("emphasizes")
            if len(parts) > 1:
                key_phrases.append(parts[1].split(".")[0].strip())
        
        if "centers on" in description:
            parts = description.split("centers on")
            if len(parts) > 1:
                key_phrases.append(parts[1].split(".")[0].strip())
        
        # If no key phrases were found, use the first sentence of the description
        if not key_phrases and description:
            key_phrases.append(description.split(".")[0].strip())
        
        return ", ".join(key_phrases)