"""Utility functions for processing model outputs and results."""

import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def extract_construct_ratings(analysis_text, construct_names):
    """Extract ratings for each construct from the analysis text."""
    ratings = {}
    
    for construct in construct_names:
        # Try different patterns
        patterns = [
            rf"{construct}:\s*(\d+)%",  # "Construct: 75%"
            rf"{construct}\s*-\s*(\d+)%",  # "Construct - 75%"
            rf"-\s*{construct}:\s*(\d+)%"  # "- Construct: 75%"
        ]
        
        rating_found = False
        for pattern in patterns:
            matches = re.findall(pattern, analysis_text, re.IGNORECASE)
            if matches and matches[0].isdigit():
                ratings[construct] = int(matches[0])
                rating_found = True
                break
        
        if not rating_found:
            # Try a more relaxed approach - find a percentage near the construct name
            construct_index = analysis_text.find(construct)
            if construct_index != -1:
                # Look for a percentage within the next 100 characters
                sub_text = analysis_text[construct_index:construct_index+100]
                percent_match = re.search(r'(\d+)%', sub_text)
                if percent_match:
                    ratings[construct] = int(percent_match.group(1))
                else:
                    print(f"Warning: Could not extract rating for {construct}. Setting to 0.")
                    ratings[construct] = 0
            else:
                print(f"Warning: Could not extract rating for {construct}. Setting to 0.")
                ratings[construct] = 0
    
    return ratings

def plot_message_construct_barchart(results, messages, target_construct=None, all_constructs=None, ax=None):
    """Create a bar chart visualization of construct scores for each message."""
    all_construct_names = list(all_constructs.keys())
    
    # Group results by message
    message_results = {}
    for msg_idx, message in enumerate(messages):
        message_results[msg_idx] = [r for r in results if r["message"] == message]
    
    # Calculate average scores and std deviations for each message-construct pair
    avg_scores = {}
    std_devs = {}
    
    for msg_idx, message_data in message_results.items():
        avg_scores[msg_idx] = {}
        std_devs[msg_idx] = {}
        
        for construct in all_construct_names:
            scores = [r["ratings"].get(construct, 0) for r in message_data]
            avg_scores[msg_idx][construct] = np.mean(scores)
            std_devs[msg_idx][construct] = np.std(scores) if len(scores) > 1 else 0
    
    # Create figure with subplots (one per message) if no axis provided
    num_messages = len(messages)
    if ax is None:
        fig, axs = plt.subplots(num_messages, 1, figsize=(18, 4 * num_messages))
        
        if num_messages == 1:
            axs = [axs]  # Make it iterable
    else:
        # Use the provided axis
        axs = [ax]
    
    # Set a clean, modern style
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    
    # Get target construct theory for coloring
    target_theory = None
    if target_construct and target_construct in all_constructs:
        target_theory = all_constructs[target_construct]["theory"]
    
    for msg_idx, ax in enumerate(axs):
        constructs = all_construct_names
        scores = [avg_scores[msg_idx][c] for c in constructs]
        errors = [std_devs[msg_idx][c] for c in constructs]
        
        # Create bar colors
        colors = ['lightgray'] * len(constructs)
        
        # Color bars by theory
        for i, construct in enumerate(constructs):
            construct_theory = all_constructs[construct]["theory"]
            
            # If we have a target construct, highlight its theory
            if target_construct and construct_theory == target_theory:
                colors[i] = '#5B9BD5'  # Light blue for constructs from the same theory
            
            # Highlight the target construct specifically
            if target_construct and construct == target_construct:
                colors[i] = '#2F5597'  # Darker blue for the target construct
            
        # Plot the bars with error bars
        ax.bar(constructs, scores, color=colors, edgecolor='none', width=0.7)
        
        # Add error bars
        ax.errorbar(
            constructs, scores, yerr=errors, fmt='none', ecolor='black', 
            capsize=4, elinewidth=1, capthick=1
        )
            
        # Highlight the threshold line
        ax.axhline(y=70, color='#FF9999', linestyle='-', alpha=0.7, linewidth=1)
        
        # Add title and labels
        short_message = (messages[msg_idx][:60] + '...') if len(messages[msg_idx]) > 60 else messages[msg_idx]
        ax.set_title(f"Message {msg_idx+1}: \"{short_message}\"", fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_ylabel("Alignment Score (%)", fontsize=10)
        
        # Format x-axis labels
        if target_construct:
            # Highlight the target construct in the labels
            plt.setp(ax.get_xticklabels()[constructs.index(target_construct)], color='#2F5597', weight='bold')
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9)
        
        # Add grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        
        # Remove top and right spines
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
    
    # Only save if we created a new figure
    if ax is None:
        plt.tight_layout()
        
        os.makedirs("evaluation_results", exist_ok=True)
        
        # Format filename according to convention
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        construct_name = target_construct if target_construct else "all_constructs"
        
        filename = f"{construct_name}_{timestamp}.png"
        filepath = os.path.join("evaluation_results", filename)
        
        # Save the plot
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Bar chart saved as {filepath}")
        
        return filepath
    else:
        # Return the modified axis
        return ax

def generate_message_summary(results, messages, target_construct=None):
    """Generate a summary of the message analysis results."""
    # Group results by message
    message_results = {}
    for msg_idx, message in enumerate(messages):
        message_results[msg_idx] = [r for r in results if r["message"] == message]
    
    summary = {
        "messages": {},
        "overall": {}
    }
    
    if target_construct:
        summary["target_construct"] = target_construct
    
    # Calculate average scores for each message
    for msg_idx, message in enumerate(messages):
        message_data = message_results[msg_idx]
        avg_ratings = {}
        
        # Access all_constructs from the results data
        # Get the first result to access the constructs
        first_result = message_data[0]
        all_constructs_keys = first_result["ratings"].keys()
        
        for construct in all_constructs_keys:
            scores = [r["ratings"].get(construct, 0) for r in message_data]
            avg_ratings[construct] = np.mean(scores)
        
        # Find best construct match
        best_construct = max(avg_ratings.items(), key=lambda x: x[1])
        
        # Get explanations from all iterations
        explanations = [r.get("best_match_explanation", "") for r in message_data]
        
        summary["messages"][msg_idx] = {
            "text": message,
            "avg_ratings": avg_ratings,
            "best_construct": best_construct[0],
            "best_construct_score": best_construct[1],
            "explanations": explanations
        }
        
        # Add target construct information if applicable
        if target_construct:
            target_score = avg_ratings.get(target_construct, 0)
            is_best_match = (best_construct[0] == target_construct)
            
            summary["messages"][msg_idx]["target_construct_score"] = target_score
            summary["messages"][msg_idx]["target_is_best_match"] = is_best_match
    
    # Calculate overall statistics
    if target_construct:
        target_scores = [summary["messages"][idx]["target_construct_score"] for idx in summary["messages"]]
        target_match_count = sum(1 for idx in summary["messages"] if summary["messages"][idx]["target_is_best_match"])
        
        summary["overall"]["avg_target_score"] = np.mean(target_scores)
        summary["overall"]["target_match_percentage"] = (target_match_count / len(messages)) * 100
    
    # Find overall best construct across all messages
    first_msg_ratings = summary["messages"][0]["avg_ratings"]
    all_constructs_avg = {construct: 0 for construct in first_msg_ratings}
    
    for construct in all_constructs_avg:
        scores = [summary["messages"][idx]["avg_ratings"].get(construct, 0) for idx in summary["messages"]]
        all_constructs_avg[construct] = np.mean(scores)
    
    overall_best_construct = max(all_constructs_avg.items(), key=lambda x: x[1])
    summary["overall"]["all_constructs_avg"] = all_constructs_avg
    summary["overall"]["overall_best_construct"] = overall_best_construct[0]
    summary["overall"]["overall_best_score"] = overall_best_construct[1]
    
    return summary