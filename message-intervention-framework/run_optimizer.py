"""Entry point for running the message optimization process with enhanced convergence criteria."""

import argparse
import json
import os
from datetime import datetime

from common.constants import all_constructs
from generator.message_generator import LlamaGenerator
from evaluator.message_evaluator import GPTEvaluator
from optimizer.message_optimizer import MessageOptimizer

def main():
    parser = argparse.ArgumentParser(description="Optimize messages for psychological constructs with enhanced convergence criteria")
    parser.add_argument("--construct", type=str, 
                      help="Target construct for message optimization (if not specified, will optimize for all constructs)")
    parser.add_argument("--num-messages", type=int, default=3, 
                      help="Number of messages to optimize per construct (default: 3)")
    parser.add_argument("--max-iterations", type=int, default=20, 
                      help="Maximum number of iterations per message (default: 20)")
    parser.add_argument("--min-consecutive", type=int, default=3, 
                      help="Minimum consecutive iterations meeting convergence criteria (default: 3)")
    parser.add_argument("--target-score-threshold", type=float, default=85.0, 
                      help="Target construct score threshold for convergence (default: 85.0)")
    parser.add_argument("--score-difference-threshold", type=float, default=25.0, 
                    help="Minimum score difference between target and next highest construct (default: 25.0)")
    parser.add_argument("--improvement-threshold", type=float, default=5.0,
                    help="Threshold for determining score improvement plateaus (default: 5.0)")
    parser.add_argument("--output", type=str, default="optimization_results", 
                      help="Output directory for optimization results (default: 'optimization_results')")
    parser.add_argument("--generator-temp", type=float, default=0.7, 
                      help="Temperature for generator (default: 0.7)")
    parser.add_argument("--evaluator-temp", type=float, default=0.3, 
                      help="Temperature for evaluator (default: 0.3)")
    parser.add_argument("--llama-model", type=str, default="meta-llama/Llama-3.3-70B-Instruct-Turbo", 
                      help="Llama model to use for generation (default: meta-llama/Llama-3.3-70B-Instruct-Turbo)")
    parser.add_argument("--gpt-model", type=str, default="gpt-4o", 
                      help="GPT model to use for evaluation (default: gpt-4o)")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Initialize generator and evaluator
    print("Initializing generator and evaluator...")
    generator = LlamaGenerator(
        model=args.llama_model,
        temperature=args.generator_temp
    )
    
    evaluator = GPTEvaluator(
        model=args.gpt_model,
        temperature=args.evaluator_temp
    )
    
    # Create optimizer
    optimizer = MessageOptimizer(
        generator=generator,
        evaluator=evaluator,
        output_dir=args.output
    )
    
    # Get list of all constructs to optimize
    constructs_to_optimize = []
    if args.construct:
        if args.construct in all_constructs:
            constructs_to_optimize = [args.construct]
        else:
            print(f"Error: Unknown construct '{args.construct}'. Available constructs: {', '.join(all_constructs.keys())}")
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
            num_messages=args.num_messages,
            max_iterations=args.max_iterations,
            min_consecutive=args.min_consecutive,
            target_score_threshold=args.target_score_threshold,
            score_difference_threshold=args.score_difference_threshold
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
    filepath = os.path.join(args.output, filename)
    
    with open(filepath, "w") as f:
        json.dump({
            "generator_model": args.llama_model,
            "evaluator_model": args.gpt_model,
            "generator_temperature": args.generator_temp,
            "evaluator_temperature": args.evaluator_temp,
            "target_score_threshold": args.target_score_threshold,
            "score_difference_threshold": args.score_difference_threshold,
            "min_consecutive": args.min_consecutive,
            "max_iterations": args.max_iterations,
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