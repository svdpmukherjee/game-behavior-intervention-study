"""
Bayesian multinomial model for cheating behavior
"""

import pymc as pm
import numpy as np
import arviz as az

def analyze_cheating_behavior(df, encoding_info):
    """Fit cheating model and return results for external printing/plotting."""
    
    # Prepare data
    y_cheating = df['cheating_behavior'].values
    concept_codes = df['concept_codes'].values
    concepts = encoding_info['concepts']
    control_baselines = encoding_info['control_baselines']
    
    # Prepare message codes
    message_ids = df['motivational_message_id'].astype('category')
    message_codes = message_ids.cat.codes.values
    
    # Calculate empirical priors
    counts = control_baselines['cheating_counts']
    n_non, n_partial, n_full = counts[0], counts[1], counts[2]
    control_partial_logit = np.log(n_partial / n_non) if n_non > 0 else -2
    control_full_logit = np.log(n_full / n_non) if n_non > 0 else -1
    se_partial = np.sqrt(1/n_partial + 1/n_non) if n_partial > 0 and n_non > 0 else 1.0
    se_full = np.sqrt(1/n_full + 1/n_non) if n_full > 0 and n_non > 0 else 1.0
    
    # Fit model
    with pm.Model() as model:
        # Control group baseline (empirical priors)
        beta_partial_intercept = pm.Normal('beta_partial_intercept', mu=control_partial_logit, sigma=se_partial)
        beta_full_intercept = pm.Normal('beta_full_intercept', mu=control_full_logit, sigma=se_full)
        
        # Concept effects
        concept_effects_partial = pm.Normal('concept_effects_partial', mu=-0.5, sigma=1.0, shape=len(concepts))
        concept_effects_full = pm.Normal('concept_effects_full', mu=-0.5, sigma=1.0, shape=len(concepts))
        
        # Message random effects
        message_effects_partial = pm.Normal('message_effects_partial', mu=0, sigma=0.5, shape=len(message_ids.cat.categories))
        message_effects_full = pm.Normal('message_effects_full', mu=0, sigma=0.5, shape=len(message_ids.cat.categories))
        
        # Linear predictors
        eta_partial = (beta_partial_intercept + message_effects_partial[message_codes] + 
                       pm.math.switch(concept_codes > 0, concept_effects_partial[concept_codes - 1], 0))
        eta_full = (beta_full_intercept + message_effects_full[message_codes] + 
                    pm.math.switch(concept_codes > 0, concept_effects_full[concept_codes - 1], 0))
        
        # Multinomial logistic probabilities
        logits = pm.math.stack([pm.math.zeros(eta_partial.shape), eta_partial, eta_full], axis=1)
        probs = pm.math.softmax(logits, axis=1)
        
        pm.Categorical('cheating_obs', p=probs, observed=y_cheating)
    
    print("Fitting cheating behavior model...")
    with model:
        trace = pm.sample(1000, tune=500, chains=4, cores=4, target_accept=0.9, random_seed=42, progressbar=False)
    
    # Calculate effects for external use
    effects = calculate_effects(trace, concepts, control_baselines, df)
    
    print("✓ Cheating model completed")
    
    return trace, {**effects, 'model': model}

def calculate_effects(trace, concepts, control_baselines, df):
    """Calculate intervention effects from posterior - NO PRINTING."""
    
    # Extract samples
    beta_partial_intercept = trace.posterior['beta_partial_intercept'].values.flatten()
    beta_full_intercept = trace.posterior['beta_full_intercept'].values.flatten()
    concept_effects_partial = trace.posterior['concept_effects_partial'].values.reshape(-1, len(concepts))
    concept_effects_full = trace.posterior['concept_effects_full'].values.reshape(-1, len(concepts))
    
    # Control probabilities
    control_logits = np.column_stack([np.zeros(len(beta_partial_intercept)), beta_partial_intercept, beta_full_intercept])
    control_probs = np.exp(control_logits) / np.exp(control_logits).sum(axis=1, keepdims=True)
    
    # Overall intervention effects
    overall_partial = concept_effects_partial.mean(axis=1)
    overall_full = concept_effects_full.mean(axis=1)
    overall_logits = np.column_stack([np.zeros(len(beta_partial_intercept)), 
                                     beta_partial_intercept + overall_partial,
                                     beta_full_intercept + overall_full])
    overall_probs = np.exp(overall_logits) / np.exp(overall_logits).sum(axis=1, keepdims=True)
    
    # Calculate overall differences (percentage points)
    overall_effects = {}
    for i, cat in enumerate(['Non', 'Partial', 'Full']):
        diff = (overall_probs[:, i] - control_probs[:, i]) * 100
        overall_effects[cat] = {
            'mean': diff.mean(),
            'hdi': az.hdi(diff, hdi_prob=0.95)
        }
    
    # Calculate descriptive statistics
    control_data = df[df['concept'] == 'control']
    intervention_data = df[df['concept'] != 'control']
    
    descriptive_stats = {
        'control_n': len(control_data),
        'intervention_n': len(intervention_data),
        'control_cheated_pct': (control_data['cheating_behavior'] > 0).mean() * 100,
        'intervention_cheated_pct': (intervention_data['cheating_behavior'] > 0).mean() * 100,
        'control_breakdown': control_data['cheating_behavior'].value_counts(normalize=True).sort_index() * 100,
        'intervention_breakdown': intervention_data['cheating_behavior'].value_counts(normalize=True).sort_index() * 100
    }
    
    # Calculate concept-specific effects
    concept_effects = []
    
    # Order concepts by theory
    theory_order = [
        'autonomy', 'competence', 'relatedness',  # Self-Determination
        'self_concept', 'cognitive_inconsistency', 'dissonance_arousal', 'dissonance_reduction',  # Cognitive Dissonance
        'performance_accomplishments', 'vicarious_experience', 'verbal_persuasion', 'emotional_arousal',  # Self-Efficacy
        'descriptive_norms', 'injunctive_norms', 'social_sanctions', 'reference_group_identification'  # Social Norms
    ]

    # Theory mapping
    theory_map = {
        'autonomy': 'Self-Determination Theory', 'competence': 'Self-Determination Theory', 'relatedness': 'Self-Determination Theory',
        'self_concept': 'Cognitive Dissonance Theory', 'cognitive_inconsistency': 'Cognitive Dissonance Theory', 
        'dissonance_arousal': 'Cognitive Dissonance Theory', 'dissonance_reduction': 'Cognitive Dissonance Theory',
        'performance_accomplishments': 'Self-Efficacy Theory', 'vicarious_experience': 'Self-Efficacy Theory', 
        'verbal_persuasion': 'Self-Efficacy Theory', 'emotional_arousal': 'Self-Efficacy Theory',
        'descriptive_norms': 'Social Norms Theory', 'injunctive_norms': 'Social Norms Theory', 
        'social_sanctions': 'Social Norms Theory', 'reference_group_identification': 'Social Norms Theory'
    }
    for concept in theory_order:
        if concept in concepts:
            i = concepts.index(concept)
            
            # Calculate concept-specific probabilities
            concept_logits = np.column_stack([
                np.zeros(len(beta_partial_intercept)),
                beta_partial_intercept + concept_effects_partial[:, i],
                beta_full_intercept + concept_effects_full[:, i]
            ])
            concept_probs = np.exp(concept_logits) / np.exp(concept_logits).sum(axis=1, keepdims=True)     
            
            # Differences with HDI
            non_diff = (concept_probs[:, 0] - control_probs[:, 0]) * 100
            partial_diff = (concept_probs[:, 1] - control_probs[:, 1]) * 100
            full_diff = (concept_probs[:, 2] - control_probs[:, 2]) * 100
            
            concept_effects.append({
                'concept': concept,
                'concept_label': concept.replace('_', ' ').title(),
                'theory': theory_map.get(concept, 'Unknown Theory'),
                'non_mean': non_diff.mean(),
                'non_hdi': az.hdi(non_diff, hdi_prob=0.95),
                'partial_mean': partial_diff.mean(),
                'partial_hdi': az.hdi(partial_diff, hdi_prob=0.95),
                'full_mean': full_diff.mean(),
                'full_hdi': az.hdi(full_diff, hdi_prob=0.95)
            })
    
    return {
        'overall_effects': overall_effects,
        'concept_effects': concept_effects, 
        'control_probs': control_probs,
        'descriptive_stats': descriptive_stats,
        'trace': trace
    }
