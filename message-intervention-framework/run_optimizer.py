"""Entry point for running the message optimization process with enhanced convergence criteria."""

import argparse
import json
import os
from datetime import datetime
import random

from common.constants import all_constructs, task_contexts
from generator.message_generator import LlamaGenerator
from evaluator.message_evaluator import GPTEvaluator
from optimizer.message_optimizer import MessageOptimizer

def get_user_input(prompt, default=None, cast_func=str):
    """Ask user for input with a default value."""
    if default is not None:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "
    
    user_input = input(prompt).strip()
    return cast_func(user_input) if user_input else default

def main():
    
    # List of constructs to choose from
    constructs = [
        "Autonomy", "Competence", "Relatedness", "Self-concept", "Cognitive inconsistency",
        "Dissonance arousal", "Dissonance reduction", "Performance accomplishments",
        "Vicarious experience", "Verbal persuasion", "Emotional arousal", "Descriptive Norms",
        "Injunctive Norms", "Social Sanctions", "Reference Group Identification"
    ]
    
    print("\nMessage Optimizer - Enhanced Version")
    print("====================================")
    print("\nList of Theoretical Concepts for Message Generation:")
    
    # Group constructs by theory
    construct_by_theory = {}
    for construct in constructs:
        theory = all_constructs[construct]["theory"]
        if theory not in construct_by_theory:
            construct_by_theory[theory] = []
        construct_by_theory[theory].append(construct)
    
    # Print constructs organized by theory
    count = 1
    for theory, theory_constructs in construct_by_theory.items():
        print(f"\n{theory}:")
        for construct in theory_constructs:
            print(f"{count}. {construct}")
            count += 1
    
    construct_choice = get_user_input("\nEnter the number corresponding to your theoretical concept", cast_func=int)
    if 1 <= construct_choice <= len(constructs):
        construct = constructs[construct_choice - 1]
    else:
        print("Invalid choice. Exiting...")
        return
    
    # IMPROVED default argument values for parameters
    defaults = {
        "num_messages": 3,
        "max_iterations": 25,  # Increased from 20
        "min_consecutive": 3,
        "target_score_threshold": 90.0,  # Increased from 85
        "score_difference_threshold": 30.0,  # Increased from 25
        "output": "optimization_results",
        "generator_temp": 0.7,
        "evaluator_temp": 0.2,
        "llama_model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "gpt_model": "gpt-4o",
    }

    print("\nOptimization Parameters (press Enter to accept defaults):")
    print("------------------------------------------------------")
    
    # Ask the user for each argument with improved explanations
    num_messages = get_user_input("Number of messages to generate for this concept", defaults["num_messages"], int)
    max_iterations = get_user_input("Maximum iterations per message", defaults["max_iterations"], int)
    min_consecutive = get_user_input("Minimum consecutive iterations meeting criteria", defaults["min_consecutive"], int)
    target_score_threshold = get_user_input("Target score threshold", defaults["target_score_threshold"], float)
    score_difference_threshold = get_user_input("Score difference threshold from competing concepts", defaults["score_difference_threshold"], float)
    output = get_user_input("Output directory for results", defaults["output"])
    generator_temp = get_user_input("Generator temperature (0.0-1.0)", defaults["generator_temp"], float)
    evaluator_temp = get_user_input("Evaluator temperature (0.0-1.0)", defaults["evaluator_temp"], float)
    llama_model = get_user_input("Llama model", defaults["llama_model"])
    gpt_model = get_user_input("GPT model", defaults["gpt_model"])
    
    # Choose contexts
    print("\nAvailable task contexts:")
    for i, context in enumerate(task_contexts, start=1):
        # Show a preview of each context (first 100 characters)
        preview = context[:100] + "..." if len(context) > 100 else context
        print(f"{i}. {preview}")
    
    context_choice = get_user_input("Choose a primary context (0 for random each time)", 0, int)
    
    # Create output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)
    
    # Initialize generator and evaluator
    print("Initializing generator and evaluator...")
    generator = LlamaGenerator(
        model=llama_model,
        temperature=generator_temp
    )
    
    evaluator = GPTEvaluator(
        model=gpt_model,
        temperature=evaluator_temp
    )
    
    # Create optimizer
    optimizer = MessageOptimizer(
        generator=generator,
        evaluator=evaluator,
        output_dir=output
    )
    
    # Set selected context if specified
    if context_choice > 0 and context_choice <= len(task_contexts):
        selected_context = task_contexts[context_choice - 1]
        optimizer.default_context = selected_context
    
    # Get list of all constructs to optimize
    constructs_to_optimize = []
    if construct:
        if construct in all_constructs:
            constructs_to_optimize = [construct]
        else:
            print(f"Error: Unknown construct '{construct}'. Available constructs: {', '.join(all_constructs.keys())}")
            return
    else:
        constructs_to_optimize = list(all_constructs.keys())
    
    # Optimize messages for each construct
    all_optimized_messages = {}
    
    for construct in constructs_to_optimize:
        print(f"\n{'='*80}\nOptimizing messages for construct: {construct}\n{'='*80}")
        
        optimized_messages = optimizer.optimize_multiple_messages(
            construct_name=construct,
            all_constructs=all_constructs,
            num_messages=num_messages,
            max_iterations=max_iterations,
            min_consecutive=min_consecutive,
            target_score_threshold=target_score_threshold,
            score_difference_threshold=score_difference_threshold
        )
        
        all_optimized_messages[construct] = optimized_messages
        
        # Print optimized messages
        print(f"\nOptimized messages for {construct}:")
        for i, result in enumerate(optimized_messages, 1):
            converged_status = "✓ CONVERGED" if result.get("converged", False) else "✗ NOT CONVERGED"
            score_diff = result.get("score_difference", "N/A")
            next_highest = result.get("next_highest_construct", "N/A")
            
            print(f"\n{i}. \"{result['message']}\"")
            print(f"   Score: {result['score']}%, Iterations: {result['iterations']}, Status: {converged_status}")
            print(f"   Difference from next highest construct ({next_highest}): {score_diff}%")
    
    # Save all optimized messages to a single file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_optimized_messages_{timestamp}.json"
    filepath = os.path.join(output, filename)
    
    with open(filepath, "w") as f:
        json.dump({
            "generator_model": llama_model,
            "evaluator_model": gpt_model,
            "generator_temperature": generator_temp,
            "evaluator_temperature": evaluator_temp,
            "target_score_threshold": target_score_threshold,
            "score_difference_threshold": score_difference_threshold,
            "min_consecutive": min_consecutive,
            "max_iterations": max_iterations,
            "optimized_messages": all_optimized_messages
        }, f, indent=2)
    
    print(f"\nAll optimized messages saved to: {filepath}")

    # Generate summary statistics
    converged_count = 0
    total_messages = 0
    
    for construct, messages in all_optimized_messages.items():
        for message in messages:
            total_messages += 1
            if message.get("converged", False):
                converged_count += 1
    
    convergence_rate = (converged_count / total_messages) * 100 if total_messages > 0 else 0
    
    print(f"\nSummary Statistics:")
    print(f"Total messages optimized: {total_messages}")
    print(f"Messages that converged: {converged_count} ({convergence_rate:.1f}%)")
    print(f"Messages that did not converge: {total_messages - converged_count} ({100 - convergence_rate:.1f}%)")
    
    # Print the best message
    if all_optimized_messages and constructs_to_optimize:
        construct = constructs_to_optimize[0]
        if construct in all_optimized_messages and all_optimized_messages[construct]:
            best_message = max(all_optimized_messages[construct], key=lambda x: x.get("score", 0))
            print(f"\nBest message for {construct} (Score: {best_message.get('score', 0)}%):")
            print(f"\"{best_message.get('message', '')}\"")

if __name__ == "__main__":
    main()