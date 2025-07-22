"""
Concise data loading and validation.
"""

import pandas as pd
import numpy as np

def load_and_validate_data(file_path: str = "../data/final_dataset.csv") -> pd.DataFrame:
    """Load and validate the research dataset."""
    
    # Load data - handle both Excel and CSV
    df = pd.read_csv(file_path)

    print(f"Dataset loaded: {len(df)} participants, {len(df.columns)} variables")
    
    # Basic validation and cleaning
    initial_size = len(df)
    
    # Remove duplicates and invalid data
    if 'prolific_id' in df.columns:
        df = df.drop_duplicates(subset=['prolific_id'])
    
    # Ensure cheating rate is valid
    if 'cheating_rate_main_round' in df.columns:
        df = df[df['cheating_rate_main_round'].between(0, 1, inclusive='both')]
    
    # Remove missing key variables
    key_vars = ['cheating_rate_main_round', 'performance_score_including_cheated_words', 
                'task_satisfaction', 'task_engagement']
    
    # Only check variables that exist in the dataset
    existing_key_vars = [var for var in key_vars if var in df.columns]
    if existing_key_vars:
        df = df.dropna(subset=existing_key_vars)
    
    removed = initial_size - len(df)
    if removed > 0:
        print(f"Cleaned: {removed} participants removed, {len(df)} remaining")
    
    return df