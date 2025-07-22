"""
Concise data preprocessing for analysis.
"""

import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Complete preprocessing pipeline."""
    
    df = df.copy()
    
    # Create derived variables
    df['cheating_behavior'] = df['cheating_rate_main_round'].apply(
        lambda x: 0 if x == 0 else (2 if x == 1 else 1)  # 0=non, 1=partial, 2=full
    )
    df['cheated_binary'] = (df['cheating_behavior'] > 0).astype(int)  # Add binary version
    df['experience'] = (df['task_satisfaction'] + df['task_engagement']) / 2
    df['performance'] = df['performance_score_including_cheated_words']
    
    # Extract concepts from message IDs
    if 'motivational_message_id' in df.columns:
        df['concept'] = df['motivational_message_id'].str.replace(r'_\d+$', '', regex=True)
        # Set control group
        control_mask = df['theory'].str.contains('control', case=False, na=False)
        df.loc[control_mask, 'concept'] = 'control'
    else:
        df['concept'] = df['theory'].fillna('control')
    
    # Prepare categorical encoding
    concept_cats = df['concept'].astype('category')
    if 'control' in concept_cats.cat.categories:
        concept_cats = concept_cats.cat.reorder_categories(
            ['control'] + [c for c in concept_cats.cat.categories if c != 'control']
        )
    df['concept_codes'] = concept_cats.cat.codes
    
    # Get control baselines
    control_data = df[df['concept'] == 'control']
    control_baselines = {
        'cheating_counts': control_data['cheating_behavior'].value_counts().sort_index(),
        'performance_by_cheating': [
            control_data[control_data['cheating_behavior'] == i]['performance'].mean() 
            for i in range(3)
        ],
        'experience_by_cheating': [
            control_data[control_data['cheating_behavior'] == i]['experience'].mean() 
            for i in range(3)
        ]
    }
    
    # Encoding info
    encoding_info = {
        'concepts': list(concept_cats.cat.categories[1:]),  # Exclude control
        'control_baselines': control_baselines
    }
    
    print(f"Preprocessing complete: {len(encoding_info['concepts'])} intervention concepts")
    print(f"Control group: {len(control_data)} participants")
    
    return df, encoding_info