"""Entry point for running the message optimization process with convergence criteria."""

import argparse
import json
import os
from datetime import datetime

from common.constants import all_constructs
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
    
    print("\nMessage Optimizer - Version")
    print("====================================")
    print("\nList of Theoretical Concepts for Message Generation:")
    for i, construct in enumerate(constructs, start=1):
        print(f"{i}. {construct}")
    
    construct_choice = get_user_input("\nEnter the number corresponding to your theoretical concept", cast_func=int)
    construct = constructs[construct_choice - 1] if 1 <= construct_choice <= len(constructs) else None
    if not construct:
        print("Invalid choice. Exiting...")
        return
    
    # IMPROVED default argument values for parameters based on analysis
    defaults = {
        "num_messages": 3,
        "max_iterations": 20,
        "min_consecutive": 3,
        "target_score_threshold": 85.0,
        "score_difference_threshold": 25.0,
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
    
    # parser = argparse.ArgumentParser(description="Optimize messages for psychological constructs with convergence criteria")
    # parser.add_argument("--construct", type=str, 
    #                   help="Target construct for message optimization (if not specified, will optimize for all constructs)")
    # parser.add_argument("--num-messages", type=int, default=3, 
    #                   help="Number of messages to optimize per construct (default: 3)")
    # parser.add_argument("--max-iterations", type=int, default=20, 
    #                   help="Maximum number of iterations per message (default: 20)")
    # parser.add_argument("--min-consecutive", type=int, default=3, 
    #                   help="Minimum consecutive iterations meeting convergence criteria (default: 3)")
    # parser.add_argument("--target-score-threshold", type=float, default=85.0, 
    #                   help="Target construct score threshold for convergence (default: 85.0)")
    # parser.add_argument("--score-difference-threshold", type=float, default=25.0, 
    #                 help="Minimum score difference between target and next highest construct (default: 25.0)")
    # parser.add_argument("--improvement-threshold", type=float, default=5.0,
    #                 help="Threshold for determining score improvement plateaus (default: 5.0)")
    # parser.add_argument("--output", type=str, default="optimization_results", 
    #                   help="Output directory for optimization results (default: 'optimization_results')")
    # parser.add_argument("--generator-temp", type=float, default=0.7, 
    #                   help="Temperature for generator (default: 0.7)")
    # parser.add_argument("--evaluator-temp", type=float, default=0.3, 
    #                   help="Temperature for evaluator (default: 0.3)")
    # parser.add_argument("--llama-model", type=str, default="meta-llama/Llama-3.3-70B-Instruct-Turbo", 
    #                   help="Llama model to use for generation (default: meta-llama/Llama-3.3-70B-Instruct-Turbo)")
    # parser.add_argument("--gpt-model", type=str, default="gpt-4o", 
    #                   help="GPT model to use for evaluation (default: gpt-4o)")
    
    # args = parser.parse_args()
    
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
            converged_status = "CONVERGED" if result.get("converged", False) else "NOT CONVERGED"
            score_diff = result.get("score_difference", "N/A")
            next_highest = result.get("next_highest_construct", "N/A")
            
            print(f"\n{i}. \"{result['message']}\" (Score: {result['score']}%, Iterations: {result['iterations']}, Status: {converged_status})")
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

if __name__ == "__main__":
    main()