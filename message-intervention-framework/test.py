"""
Test script for evaluating message generation and evaluation components without iteration.

This script:
1. Generates multiple messages using the LlamaGenerator with enhanced diversity mechanisms
2. Evaluates each generated message using the GPTEvaluator
3. Displays and saves evaluation results
4. Creates visualizations of the evaluation results

Usage:
python test.py

The script will prompt for:
- The construct to test
- Number of messages to generate
- Models to use for generation and evaluation
- Other parameters
"""

import os
import json
import time
import random
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Import the generator and evaluator
from generator.message_generator import LlamaGenerator
from evaluator.message_evaluator import GPTEvaluator
from common.constants import all_constructs, task_contexts
from common.utils import plot_message_construct_barchart, generate_message_summary

# Load environment variables
load_dotenv()

# Load a pre-trained SBERT model for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_user_input(prompt, default=None, cast_func=str):
    """Ask user for input with a default value."""
    if default is not None:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "
    
    user_input = input(prompt).strip()
    return cast_func(user_input) if user_input else default

def default_serializer(obj):
    """ Custom serializer to handle non-serializable objects """
    if hasattr(obj, 'to_json'):
        return obj.to_json()  # If object has a JSON method
    if isinstance(obj, plt.Axes):
        return "Matplotlib Axes object (not serializable)"  # Avoid dumping it
    return str(obj)  # Convert any other unknown objects to string

def display_construct_choices():
    """Display available constructs organized by theory."""
    print("\nAvailable Psychological Constructs:")
    print("==================================")
    
    # Group constructs by theory
    constructs_by_theory = {}
    for construct in all_constructs:
        theory = all_constructs[construct]["theory"]
        if theory not in constructs_by_theory:
            constructs_by_theory[theory] = []
        constructs_by_theory[theory].append(construct)
    
    # Print constructs organized by theory
    count = 1
    for theory, constructs in constructs_by_theory.items():
        print(f"\n{theory}:")
        for construct in constructs:
            print(f"{count}. {construct}")
            count += 1
    
    return list(all_constructs.keys())

def calculate_semantic_similarity(message1, message2):
    """Calculate semantic similarity between two messages using cosine similarity.
    
    Args:
        message1: First message
        message2: Second message
            
    Returns:
        float: Similarity score between 0 and 1
    """
    # Encode the messages to get their embeddings
    embeddings = model.encode([message1, message2], convert_to_tensor=True)
    
    # Convert to numpy and calculate cosine similarity
    embedding1 = embeddings[0].cpu().numpy().reshape(1, -1)
    embedding2 = embeddings[1].cpu().numpy().reshape(1, -1)
    
    sim_score = cosine_similarity(embedding1, embedding2)[0][0]
    return sim_score

def check_message_similarity(new_message, previous_messages, threshold=0.8):
    """Check if new message is too semantically similar to previous ones.
    
    Args:
        new_message: New message to check
        previous_messages: List of previous messages
        threshold: Similarity threshold (0-1)
            
    Returns:
        bool: True if too similar, False otherwise
    """
    if not previous_messages:
        return False
        
    for prev_msg in previous_messages:
        similarity = calculate_semantic_similarity(new_message, prev_msg)
        if similarity > threshold:
            return True
    return False

def calculate_pairwise_similarities(messages):
    """Calculate pairwise semantic similarities between all messages.
    
    Args:
        messages: List of messages
        
    Returns:
        list: List of tuples (pair_name, similarity_score)
    """
    if len(messages) <= 1:
        return []
    
    # Encode all messages at once for efficiency
    embeddings = model.encode(messages, convert_to_tensor=True)
    
    # Convert to numpy for cosine_similarity calculation
    embeddings_np = embeddings.cpu().numpy()
    
    # Calculate full similarity matrix
    similarity_matrix = cosine_similarity(embeddings_np)
    
    # Extract pairwise similarities (upper triangle of the matrix)
    pairs = []
    similarities = []
    for i in range(len(messages)):
        for j in range(i+1, len(messages)):
            pairs.append(f"M{i+1}-M{j+1}")
            similarities.append(similarity_matrix[i, j])
    
    return list(zip(pairs, similarities))

def generate_diverse_message(generator, construct_name, previous_messages, iteration, diversity_level=0.5):
    """Generate a message with enforced diversity from previous messages.
    
    Args:
        generator: The message generator
        construct_name: Name of the construct
        previous_messages: List of previously generated messages
        iteration: Current iteration number
        diversity_level: How aggressive diversity should be (0-1)
        
    Returns:
        str: Generated message
    """
    # Store original temperature
    original_temp = generator.temperature
    
    # Select a random context from available task contexts
    if task_contexts:
        # Use a different context for each message if possible
        context = task_contexts[iteration % len(task_contexts)]
    else:
        from common.constants import game_context
        context = game_context
    
    # Create diversity focus based on iteration
    diversity_focuses = [
        "how this construct manifests in personal growth over time",
        "how this construct helps overcome specific challenges and obstacles",
        "the internal emotional experience of embodying this construct",
        "the long-term benefits of applying this construct consistently",
        "how this construct relates to authentic skill development",
        "the relationship between this construct and maintaining integrity",
        "how this construct connects to decision-making processes",
        "practical day-to-day applications of this construct",
        "how this construct influences one's perspective on learning",
        "the relationship between this construct and personal satisfaction"
    ]
    
    # Use a different diversity focus for each iteration
    diversity_focus = diversity_focuses[iteration % len(diversity_focuses)]
    
    # Increase temperature for diversity (scales with iteration)
    temp_increase = min(0.5, 0.1 + (iteration * 0.05))
    generator.temperature = min(0.9, original_temp + temp_increase)
    
    # Craft a custom generation instruction with explicit diversity guidance
    generation_instruction = f"""
    Create a message that aligns with the construct of {construct_name} while 
    focusing specifically on {diversity_focus}.
    
    This message must be COMPLETELY DIFFERENT from previous messages in:
    - Structure and rhythm
    - Vocabulary and phrasing
    - Focus and perspective
    - Examples or scenarios used
    
    IMPORTANT: Do NOT reuse the following phrases or concepts that appeared in previous messages:
    """
    
    # Extract key phrases from previous messages to avoid
    if previous_messages:
        # Extract 2-3 key phrases from each previous message
        key_phrases = []
        for msg in previous_messages[-3:]:  # Consider last 3 messages
            words = msg.split()
            # Get some 3-word phrases to avoid
            if len(words) > 3:
                for i in range(len(words) - 2):
                    if random.random() < 0.3:  # Only sample some phrases
                        phrase = " ".join(words[i:i+3])
                        if len(phrase) > 10:  # Only meaningful phrases
                            key_phrases.append(phrase)
        
        # Add these phrases to avoid
        if key_phrases:
            for phrase in key_phrases[:5]:  # Limit to 5 phrases
                generation_instruction += f"\n- \"{phrase}\""
    
    # Add specific structural diversity based on iteration
    if iteration % 4 == 0:
        generation_instruction += "\nCreate a message that uses a question-answer format."
    elif iteration % 4 == 1:
        generation_instruction += "\nCreate a message that uses a conditional 'when-then' structure."
    elif iteration % 4 == 2:
        generation_instruction += "\nCreate a message that uses a comparison or contrast structure."
    else:
        generation_instruction += "\nCreate a message that uses a personal reflection format."
    
    # Get construct info for more targeted generation
    construct_info = all_constructs.get(construct_name, {})
    
    # Get examples to potentially avoid similar phrasing
    construct_examples = construct_info.get("examples", [])
    
    max_attempts = 3
    message = None
    
    for attempt in range(max_attempts):
        # Generate message with diversity instructions
        message = generator.generate_message(
            construct_name,
            context=context,
            generation_instruction=generation_instruction,
            diversity_mode=True,
            previous_messages=previous_messages
        )
        
        # Check if it's similar to previous messages
        if not check_message_similarity(message, previous_messages, threshold=0.8):
            # We found a sufficiently different message
            break
        
        # If too similar, increase temperature and try again
        print(f"  Generated message too semantically similar, retrying with higher temperature...")
        generator.temperature = min(0.95, generator.temperature + 0.1)
    
    # Reset generator temperature
    generator.temperature = original_temp
    
    return message

def generate_and_evaluate_messages(construct_name, num_messages=10, 
                                 generator_temp=0.7, evaluator_temp=0.2,
                                 generator_model="meta-llama/Llama-3.3-70B-Instruct-Turbo", 
                                 evaluator_model="gpt-4o",
                                 output_dir="test_results"):
    """Generate and evaluate messages for a construct with enhanced diversity.
    
    Args:
        construct_name: Name of the construct to test
        num_messages: Number of messages to generate and evaluate
        generator_temp: Temperature for the generator
        evaluator_temp: Temperature for the evaluator
        generator_model: Model for the generator
        evaluator_model: Model for the evaluator
        output_dir: Directory to save results
        
    Returns:
        dict: Test results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nInitializing generator ({generator_model}) and evaluator ({evaluator_model})...")
    
    # Initialize generator and evaluator
    generator = LlamaGenerator(
        model=generator_model,
        temperature=generator_temp
    )
    
    evaluator = GPTEvaluator(
        model=evaluator_model,
        temperature=evaluator_temp
    )
    
    # Get construct info from constants
    construct_info = all_constructs.get(construct_name, {})
    if not construct_info:
        raise ValueError(f"Unknown construct: {construct_name}")
    
    # Track results
    messages = []
    evaluations = []
    evaluation_results = []
    generation_times = []
    evaluation_times = []
    
    print(f"\nGenerating and evaluating {num_messages} messages for '{construct_name}'...")
    
    for i in range(1, num_messages + 1):
        print(f"\nMessage {i}/{num_messages}:")
        
        # Generate message with enhanced diversity
        start_time = time.time()
        message = generate_diverse_message(
            generator, 
            construct_name, 
            messages,  # Pass all previous messages
            i - 1,     # 0-based iteration
            diversity_level=0.7  # Higher diversity level
        )
        generation_time = time.time() - start_time
        generation_times.append(generation_time)
        
        messages.append(message)
        print(f"Generated: {message}")
        print(f"Generation time: {generation_time:.2f}s")
        
        # Calculate similarity with previous messages for reporting
        if len(messages) > 1:
            prev_message = messages[-2]  # Compare with the last message
            similarity = calculate_semantic_similarity(message, prev_message)
            print(f"Semantic similarity with previous message: {similarity:.2f}")
            
            # If we have multiple messages, report avg similarity with all previous
            if len(messages) > 2:
                prev_messages = messages[:-1]
                
                # Calculate semantic similarity with each previous message
                all_similarities = []
                for prev_msg in prev_messages:
                    sim = calculate_semantic_similarity(message, prev_msg)
                    all_similarities.append(sim)
                
                avg_similarity = sum(all_similarities) / len(all_similarities)
                print(f"Average semantic similarity with all previous messages: {avg_similarity:.2f}")
        
        # Evaluate message with timing
        start_time = time.time()
        evaluation = evaluator.evaluate_message_with_feedback(
            message,
            construct_name,
            context=None  # Let the evaluator use default context
        )
        evaluation_time = time.time() - start_time
        evaluation_times.append(evaluation_time)
        
        evaluations.append(evaluation)
        evaluation_results.append({
            "message": message,
            "ratings": evaluation["ratings"],
            "best_match_explanation": "N/A"  # Not included in standard evaluation
        })
        
        print(f"Evaluation score: {evaluation['score']}%")
        print(f"Evaluation time: {evaluation_time:.2f}s")
        
        # Show top competing constructs
        other_scores = {k: v for k, v in evaluation["ratings"].items() if k != construct_name}
        if other_scores:
            top_competing = sorted(other_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            top_competing_str = ", ".join([f"{name} ({score}%)" for name, score in top_competing])
            print(f"Top competing constructs: {top_competing_str}")
    
    # Calculate summary statistics
    avg_score = np.mean([e["score"] for e in evaluations]).item()  # Convert numpy types to Python native types
    avg_generation_time = np.mean(generation_times).item()
    avg_evaluation_time = np.mean(evaluation_times).item()
    
    # Calculate message diversity metrics using semantic similarity
    diversity_metrics = {}
    if len(messages) > 1:
        # Calculate pairwise semantic similarities
        pairwise_similarities = calculate_pairwise_similarities(messages)
        similarities = [sim for _, sim in pairwise_similarities]
        
        avg_similarity = sum(similarities) / len(similarities)
        max_similarity = max(similarities)
        min_similarity = min(similarities)
        
        diversity_metrics = {
            "average_similarity": avg_similarity,
            "max_similarity": max_similarity,
            "min_similarity": min_similarity,
            "diversity_score": 1.0 - avg_similarity,  # Inverse of similarity
            "pairwise_similarities": pairwise_similarities
        }
        
        print(f"\nSemantic Diversity Metrics:")
        print(f"  Average semantic similarity between messages: {avg_similarity:.2f}")
        print(f"  Maximum semantic similarity between any two messages: {max_similarity:.2f}")
        print(f"  Minimum semantic similarity between any two messages: {min_similarity:.2f}")
        print(f"  Overall diversity score: {1.0 - avg_similarity:.2f}")
    
    # Generate visualization - IMPORTANT: Save path but don't include the actual chart object
    try:
        # Call the utility function but only store the path
        chart_path = plot_message_construct_barchart(evaluation_results, messages, 
                                                target_construct=construct_name,
                                                all_constructs=all_constructs)
    except Exception as e:
        print(f"Warning: Error generating visualization: {e}")
        chart_path = "visualization_error.png"
    
    # Save results to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{construct_name}_test_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Create a JSON-serializable copy of all ratings
    serializable_ratings = []
    for evaluation in evaluations:
        # Convert each rating dict to ensure all values are native Python types
        serializable_rating = {}
        for k, v in evaluation["ratings"].items():
            # Ensure we're storing native Python types, not numpy types
            if hasattr(v, "item"):  # Check if it's a numpy type
                serializable_rating[k] = v.item()
            else:
                serializable_rating[k] = float(v)
        serializable_ratings.append(serializable_rating)
    
    # Create a list of evaluation scores using native Python types
    evaluation_scores = []
    for e in evaluations:
        if hasattr(e["score"], "item"):  # Check if it's a numpy type
            evaluation_scores.append(e["score"].item())
        else:
            evaluation_scores.append(float(e["score"]))
    
    # Create a results dictionary with only JSON-serializable data
    json_results = {
        "construct": construct_name,
        "num_messages": num_messages,
        "generator_model": generator_model,
        "evaluator_model": evaluator_model,
        "generator_temperature": generator_temp,
        "evaluator_temperature": evaluator_temp,
        "avg_score": avg_score,
        "avg_generation_time": avg_generation_time,
        "avg_evaluation_time": avg_evaluation_time,
        "messages": messages,
        "evaluations": evaluation_scores,
        "all_ratings": serializable_ratings,
        "chart_path": chart_path,
        "diversity_metrics": diversity_metrics
    }
    
    # Save as JSON
    with open(filepath, "w") as f:
        json.dump(json_results, f, indent=2, default=default_serializer)
    
    print(f"\nTest results saved to: {filepath}")
    print(f"Visualization saved to: {filepath}")
    
    # Return the results for plotting - make sure all values are Python native types
    return {
        "construct": construct_name,
        "messages": messages,
        "evaluations": evaluation_scores,
        "all_ratings": serializable_ratings,
        "chart_path": chart_path,
        "diversity_metrics": diversity_metrics
    }

def plot_test_results(results, output_dir="test_results"):
    """Create visualization of test results with improved graphs matching message_optimizer style.
    
    Args:
        results: Test results from generate_and_evaluate_messages
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    import os
    from common.constants import all_constructs
    
    construct_name = results["construct"]
    messages = results["messages"]
    evaluations = results["evaluations"]
    all_ratings = results["all_ratings"]
    diversity_metrics = results.get("diversity_metrics", {})
    
    # Create a figure with multiple subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18), 
                                       gridspec_kw={'height_ratios': [1, 1, 0.7]})
    
    # Plot 1: Target construct scores versus top competing constructs across messages
    message_indices = list(range(1, len(messages) + 1))
    
    # Plot target construct scores
    ax1.plot(message_indices, evaluations, marker='o', label=construct_name, linewidth=2)
    
    # Identify top competing constructs across all messages
    all_competing = {}
    for ratings in all_ratings:
        for construct, score in ratings.items():
            if construct != construct_name:
                if construct not in all_competing:
                    all_competing[construct] = 0
                all_competing[construct] += float(score)
    
    # Get top 4 competing constructs overall
    top_competing = sorted(all_competing.items(), key=lambda x: x[1], reverse=True)[:4]
    top_competing_names = [c[0] for c in top_competing]
    
    # Plot top competing constructs
    colors = ['#EA4335', '#FBBC05', '#34A853', '#4285F4']
    for i, comp_name in enumerate(top_competing_names):
        comp_scores = [float(ratings.get(comp_name, 0)) for ratings in all_ratings]
        ax1.plot(message_indices, comp_scores, marker='s', label=comp_name, 
                 color=colors[i % len(colors)], linewidth=1.5, alpha=0.8)
    
    ax1.axhline(y=85, color='#EA4335', linestyle='--', alpha=0.7, label='Target threshold (85%)')
    ax1.set_title(f"Score Trends: Target vs Top Competing Constructs")
    ax1.set_xlabel("Message Number")
    ax1.set_ylabel("Score (%)")
    ax1.set_yticks(range(10, 110, 10))
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Plot 2: Average construct scores across all messages with error bars
    # Get all construct names
    all_construct_names = list(all_constructs.keys())
    
    # Calculate average scores and standard deviations across all messages
    avg_scores = {}
    std_devs = {}
    
    for construct in all_construct_names:
        scores = [float(ratings.get(construct, 0)) for ratings in all_ratings]
        avg_scores[construct] = np.mean(scores)
        std_devs[construct] = np.std(scores) if len(scores) > 1 else 0
    
    # Sort constructs by theory groups for better visualization
    constructs_by_theory = {}
    for construct in all_construct_names:
        theory = all_constructs[construct]["theory"]
        if theory not in constructs_by_theory:
            constructs_by_theory[theory] = []
        constructs_by_theory[theory].append(construct)
    
    # Create ordered list of constructs grouped by theory
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
    
    # Create bar colors, highlighting the target construct
    colors = ['darkblue' if construct == construct_name else 'gray' for construct in all_constructs_ordered]
    
    # Create bars with error bars
    ax2.bar(positions, values, color=colors, width=0.7, alpha=0.7)
    ax2.errorbar(positions, values, yerr=errors, fmt='none', ecolor='black', 
                capsize=4, elinewidth=1, capthick=1)
    
    # Format the plot
    ax2.set_title(f"Average Construct Scores Across All Messages", fontsize=14)
    ax2.set_ylabel("Average Score (%)", fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.set_xticks(positions)
    ax2.set_xticklabels(all_constructs_ordered, rotation=45, ha='right', fontsize=9)
    
    # Highlight target construct label
    if construct_name in all_constructs_ordered:
        target_idx = all_constructs_ordered.index(construct_name)
        plt.setp(ax2.get_xticklabels()[target_idx], color='darkblue', weight='bold')
    
    # Add grid lines
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Remove top and right spines
    for spine in ['top', 'right']:
        ax2.spines[spine].set_visible(False)
        
    # Plot 3: Message similarity matrix (if more than one message)
    if len(messages) > 1 and diversity_metrics and "pairwise_similarities" in diversity_metrics:
        if len(messages) <= 10: 
            # Get all pairwise similarities
            pairwise_similarities = diversity_metrics["pairwise_similarities"]
            pairs = [pair for pair, _ in pairwise_similarities]
            similarities = [sim for _, sim in pairwise_similarities]
            
            # Create a bar chart for message similarities
            bars = ax3.bar(pairs, similarities, color='#34A853')
            ax3.axhline(y=0.8, color='#EA4335', linestyle='--', alpha=0.7, 
                       label='Similarity threshold (0.8)')
            
            # Add text labels above the bars
            for i, v in enumerate(similarities):
                ax3.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=8)
                
            ax3.set_xticklabels(pairs, rotation=90, ha="right", fontsize=8)
            
            ax3.set_title("Pairwise Semantic Similarities")
            ax3.set_xlabel("Message Pairs")
            ax3.set_ylabel("Semantic Similarity (0-1)")
            ax3.set_ylim(0, 1.1)
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        else:
            # Just show summary diversity metrics as text
            ax3.axis('off')  # Hide the axes
            avg_sim = diversity_metrics.get("average_similarity", 0)
            max_sim = diversity_metrics.get("max_similarity", 0)
            min_sim = diversity_metrics.get("min_similarity", 0)
            div_score = diversity_metrics.get("diversity_score", 0)
            
            # Create a text box with diversity metrics
            textstr = '\n'.join((
                f'Semantic Diversity Metrics:',
                f'Average Semantic Similarity: {avg_sim:.2f}',
                f'Max Semantic Similarity: {max_sim:.2f}',
                f'Min Semantic Similarity: {min_sim:.2f}',
                f'Diversity Score: {div_score:.2f} (higher is better)'
            ))
            
            # Place a text box at the center of ax3
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax3.text(0.5, 0.5, textstr, transform=ax3.transAxes, fontsize=12,
                    verticalalignment='center', horizontalalignment='center', bbox=props)
    else:
        # If no diversity metrics, hide this plot
        ax3.axis('off')
    
    plt.tight_layout(pad=3.0)
    
    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{construct_name}_test_summary_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Test summary visualization saved to: {filepath}")
    plt.close(fig)
    results["chart_path"] = filename

def main():
    """Main function for the test script."""
    print("\nEnhanced Message Generator and Evaluator Test Script")
    print("===================================================")
    print("This script generates diverse messages and evaluates their alignment with psychological constructs.")
    
    # Display available constructs and get user selection
    all_construct_names = display_construct_choices()
    
    construct_choice = get_user_input("\nEnter the number corresponding to your theoretical concept", 
                                    default=1, cast_func=int)
    
    if 1 <= construct_choice <= len(all_construct_names):
        construct_name = all_construct_names[construct_choice - 1]
    else:
        print("Invalid choice. Using default: Autonomy")
        construct_name = "Autonomy"
    
    print(f"\nSelected construct: {construct_name}")
    
    # Get test parameters from user
    defaults = {
        "num_messages": 10,
        "generator_temp": 0.7,
        "evaluator_temp": 0.2,
        "generator_model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "evaluator_model": "gpt-4o",
        "output_dir": "test_results"
    }
    
    print("\nTest Parameters (press Enter to accept defaults):")
    print("----------------------------------------------")
    
    num_messages = get_user_input("Number of messages to generate and evaluate", 
                                defaults["num_messages"], int)
    generator_temp = get_user_input("Generator temperature (0.0-1.0)", 
                                  defaults["generator_temp"], float)
    evaluator_temp = get_user_input("Evaluator temperature (0.0-1.0)", 
                                  defaults["evaluator_temp"], float)
    generator_model = get_user_input("Generator model", 
                                   defaults["generator_model"])
    evaluator_model = get_user_input("Evaluator model", 
                                   defaults["evaluator_model"])
    output_dir = get_user_input("Output directory for results", 
                              defaults["output_dir"])
    
    # Run the test
    print("\nRunning test with enhanced semantic diversity measurement...")
    try:
        results = generate_and_evaluate_messages(
            construct_name,
            num_messages=num_messages,
            generator_temp=generator_temp,
            evaluator_temp=evaluator_temp,
            generator_model=generator_model,
            evaluator_model=evaluator_model,
            output_dir=output_dir
        )
        
        # Create visualization
        print("\nCreating test summary visualization with semantic diversity metrics...")
        plot_test_results(results, output_dir)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError during test execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()