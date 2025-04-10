"""
Helper functions module.
Contains utility functions for the application.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

logger = logging.getLogger(__name__)

def default_serializer(obj):
    """
    Custom serializer to handle non-serializable objects.
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serializable representation of the object
    """
    if hasattr(obj, 'to_json'):
        return obj.to_json()  # If object has a JSON method
    if isinstance(obj, plt.Axes):
        return "Matplotlib Axes object (not serializable)"
    return str(obj)  # Convert any other unknown objects to string

def format_time(seconds: float) -> str:
    """
    Format time in seconds to a readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 0.1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 1:
        return f"{seconds:.2f}s"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds) // 60
        remaining_seconds = seconds - (minutes * 60)
        return f"{minutes}m {int(remaining_seconds)}s"

def create_evaluation_visualization(evaluation: Dict[str, Any], target_concept: str) -> Optional[Dict[str, Any]]:
    """
    Create visualizations from evaluation data.
    
    Args:
        evaluation: Evaluation results
        target_concept: Target psychological concept
        
    Returns:
        Dictionary with visualization data
    """
    if not evaluation:
        return None
    
    try:
        # Extract scores
        scores = evaluation.get("ratings", {})
        if not scores:
            return None
        
        # Sort scores
        sorted_concepts = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Separate target from other concepts
        target_score = scores.get(target_concept, 0)
        competing_concepts = [(k, v) for k, v in sorted_concepts if k != target_concept][:5]  # Top 5 competing
        
        # Prepare data for visualization
        vis_data = {
            "target": {
                "name": target_concept,
                "score": target_score
            },
            "competing": [{"name": k, "score": v} for k, v in competing_concepts],
            "all_scores": dict(sorted_concepts)
        }
        
        return vis_data
    
    except Exception as e:
        logger.error(f"Error creating evaluation visualization: {e}")
        return None

def export_messages_to_file(messages: List[str], concept_name: str) -> Optional[str]:
    """
    Export a list of messages to a file.
    
    Args:
        messages: List of messages to export
        concept_name: Name of the concept for filename
        
    Returns:
        Path to the exported file, or None if export failed
    """
    if not messages:
        return None
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join("exports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{concept_name}_messages_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w") as f:
            for i, message in enumerate(messages, 1):
                f.write(f"Message {i}:\n{message}\n\n")
        
        return filepath
    except Exception as e:
        logger.error(f"Error exporting messages to file: {e}")
        return None

def display_competing_concepts(evaluation_vis_data: Dict[str, Any]):
    """
    Display competing concepts visualization in Streamlit.
    
    Args:
        evaluation_vis_data: Visualization data for evaluation
    """
    if not evaluation_vis_data:
        return
    
    target = evaluation_vis_data["target"]
    competing = evaluation_vis_data["competing"]
    
    # Create two columns
    # col1, col2 = st.columns([1, 2])
    
    # with col1:
    #     st.metric("Target Score", f"{target['score']}%", delta=None)
    
    # with col2:
                    # Create a horizontal bar for the competing concepts
    if competing:
        # Create a simple markdown table
        st.markdown("**Top competing concepts:**")
        
        table_rows = []
        for concept in competing[:3]:  # Show top 3
            table_rows.append(f"| {concept['name']} | {concept['score']}% |")
        
        if table_rows:
            # st.markdown("| concept | Score |")
            # st.markdown("| --- | --- |")
            for row in table_rows:
                st.markdown(row)