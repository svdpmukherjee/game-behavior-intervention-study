"""
Minimal network analysis for psychological mechanisms
"""

import numpy as np
import pandas as pd
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler

def prepare_network_data(df):
    """Prepare standardized network data"""
    
    network_vars = {
        'need_satisfaction': 'overall_need_satisfaction',
        'need_frustration': 'overall_need_frustration', 
        'self_efficacy': 'task_specific_self_efficacy',
        'norm_perception': 'norm_perception',
        'cognitive_discomfort': 'cognitive_discomfort',
        'cheating': 'cheating_behavior',
        'performance': 'performance', 
        'experience': 'experience'
    }
    
    network_data = df[list(network_vars.values())].copy()
    network_data.columns = list(network_vars.keys())
    
    scaler = StandardScaler()
    network_data_scaled = pd.DataFrame(
        scaler.fit_transform(network_data),
        columns=network_data.columns,
        index=network_data.index
    )
    
    return network_data_scaled

def estimate_partial_correlations(data):
    """Estimate partial correlation matrix"""
    
    model = GraphicalLassoCV(cv=5, max_iter=1000)
    model.fit(data)
    
    # Convert precision to partial correlations
    precision = model.precision_
    diag_sqrt = np.sqrt(np.diag(precision))
    partial_corr = -precision / np.outer(diag_sqrt, diag_sqrt)
    np.fill_diagonal(partial_corr, 0)
    
    return partial_corr

def analyze_networks_by_concept(df):
    """Analyze networks for control + each concept"""
    
    network_data = prepare_network_data(df)
    labels = list(network_data.columns)
    
    # Concept order by theory
    theory_order = [
        'control',
        # Self-Determination
        'autonomy', 'competence', 'relatedness',
        # Cognitive Dissonance  
        'self_concept', 'cognitive_inconsistency', 'dissonance_arousal', 'dissonance_reduction',
        # Self-Efficacy
        'performance_accomplishments', 'vicarious_experience', 'verbal_persuasion', 'emotional_arousal',
        # Social Norms
        'descriptive_norms', 'injunctive_norms', 'social_sanctions', 'reference_group_identification'
    ]
    
    results = {}
    
    for concept in theory_order:
        if concept in df['concept'].values:
            concept_data = network_data[df['concept'] == concept]
            if len(concept_data) >= 10:  # Minimum sample size
                partial_corr = estimate_partial_correlations(concept_data)
                results[concept] = {
                    'partial_correlations': partial_corr,
                    'n_participants': len(concept_data)
                }
    
    return results, labels

def analyze_networks_with_overall_intervention(df):
    """Analyze networks for overall intervention + each concept"""
    
    network_data = prepare_network_data(df)
    labels = list(network_data.columns)
    
    # Concept order by theory
    theory_order = [
        'control',  # Control group
        'overall_intervention',  # Combined intervention effect
        # Self-Determination
        'autonomy', 'competence', 'relatedness',
        # Cognitive Dissonance  
        'self_concept', 'cognitive_inconsistency', 'dissonance_arousal', 'dissonance_reduction',
        # Self-Efficacy
        'performance_accomplishments', 'vicarious_experience', 'verbal_persuasion', 'emotional_arousal',
        # Social Norms
        'descriptive_norms', 'injunctive_norms', 'social_sanctions', 'reference_group_identification'
    ]
    
    results = {}
    
    for concept in theory_order:
        if concept == 'overall_intervention':
            # Combine all intervention data (exclude control)
            concept_data = network_data[df['concept'] != 'control']
            concept_label = 'Overall Intervention'
        elif concept in df['concept'].values:
            concept_data = network_data[df['concept'] == concept]
            concept_label = concept
        else:
            continue
            
        if len(concept_data) >= 10:  # Minimum sample size
            partial_corr = estimate_partial_correlations(concept_data)
            results[concept] = {
                'partial_correlations': partial_corr,
                'n_participants': len(concept_data)
            }
    
    return results, labels

def get_partial_correlation_tables(network_results, labels):
    """Extract partial correlation values as tables"""
    
    tables = {}
    
    for concept, results in network_results.items():
        matrix = results['partial_correlations']
        
        # Create correlation table
        corr_table = pd.DataFrame(matrix, index=labels, columns=labels)
        tables[concept] = corr_table
    
    return tables