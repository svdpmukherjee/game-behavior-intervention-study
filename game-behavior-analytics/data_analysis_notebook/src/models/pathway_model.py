"""
Pathway analysis for psychological mechanisms (RQ3)
"""

import pymc as pm
import numpy as np
import arviz as az
import pandas as pd

def analyze_psychological_pathways(df, encoding_info):
    """Analyze psychological pathways: Concepts → Mechanisms → Outcomes"""
    
    # Check available mediators
    mediator_vars = {
        'overall_need_satisfaction': 'Need Satisfaction',
        'overall_need_frustration': 'Need Frustration', 
        'task_specific_self_efficacy': 'Self Efficacy',
        'norm_perception': 'Norm Perception',
        'cognitive_discomfort': 'Discomfort'
    }
    
    # Check availability and standardize
    available_mediators = {}
    
    print("\n" + "="*60)
    print("PATHWAY ANALYSIS VARIABLE CHECK")
    print("="*60)
    
    print("PSYCHOLOGICAL MECHANISMS:")
    for var, label in mediator_vars.items():
        if var in df.columns and df[var].notna().sum() > 100:
            available_mediators[label] = (df[var] - df[var].mean()) / df[var].std()
            print(f"✓ {label}: {df[var].notna().sum()} values")
        else:
            print(f"✗ {label}: NOT FOUND or insufficient data")
    
    if len(available_mediators) < 2:
        print("X Insufficient mechanisms for pathway analysis")
        return None
    
    print(f"\nAnalyzing pathways with {len(available_mediators)} mechanisms")
    
    # Prepare data
    y_cheating = df['cheating_behavior'].values
    y_performance = df['performance'].values
    y_experience = df['experience'].values
    concept_codes = df['concept_codes'].values
    concepts = encoding_info['concepts']
    control_baselines = encoding_info['control_baselines']
    
    # Prepare mechanism matrix
    mechanism_keys = list(available_mediators.keys())
    mechanism_matrix = np.column_stack([available_mediators[key] for key in mechanism_keys])
    
    # ========================================================================
    # MODEL 1: Individual Concepts → Psychological Mechanisms
    # ========================================================================
    print("\nFitting: Individual Concepts → Psychological Mechanisms")
    
    # Calculate concept-specific effects on mechanisms
    # Calculate concept-specific effects on mechanisms
    concept_mechanism_results = {}
    
    # Add overall intervention effect
    control_mechanisms = mechanism_matrix[df['concept'] == 'control']
    intervention_mechanisms = mechanism_matrix[df['concept'] != 'control']
    
    overall_effects = {}
    for i, mech_name in enumerate(mechanism_keys):
        control_mech = control_mechanisms[:, i]
        intervention_mech = intervention_mechanisms[:, i]
        
        # Raw difference (not standardized)
        effect_mean = intervention_mech.mean() - control_mech.mean()
        
        # Standard error for confidence interval
        control_se = control_mech.std() / np.sqrt(len(control_mech))
        intervention_se = intervention_mech.std() / np.sqrt(len(intervention_mech))
        pooled_se = np.sqrt(control_se**2 + intervention_se**2)
        
        from scipy import stats
        df_pooled = len(control_mech) + len(intervention_mech) - 2
        t_crit = stats.t.ppf(0.975, df_pooled)
        hdi_low = effect_mean - t_crit * pooled_se
        hdi_high = effect_mean + t_crit * pooled_se
        
        overall_effects[mech_name] = {
            'mean': effect_mean,
            'hdi': np.array([hdi_low, hdi_high])
        }
    
    concept_mechanism_results['overall_intervention'] = overall_effects
    
    # Calculate individual concept effects
    for concept in concepts:
        if concept in df['concept'].values:
            concept_data = mechanism_matrix[df['concept'] == concept]
            if len(concept_data) >= 10:  # Minimum sample size
                
                concept_effects = {}
                for i, mech_name in enumerate(mechanism_keys):
                    control_mech = control_mechanisms[:, i]
                    concept_mech = concept_data[:, i]
                    
                    # Raw difference (not standardized)
                    effect_mean = concept_mech.mean() - control_mech.mean()
                    
                    # Standard error for confidence interval
                    control_se = control_mech.std() / np.sqrt(len(control_mech))
                    concept_se = concept_mech.std() / np.sqrt(len(concept_mech))
                    pooled_se = np.sqrt(control_se**2 + concept_se**2)
                    
                    df_pooled = len(control_mech) + len(concept_mech) - 2
                    t_crit = stats.t.ppf(0.975, df_pooled)
                    hdi_low = effect_mean - t_crit * pooled_se
                    hdi_high = effect_mean + t_crit * pooled_se
                    
                    concept_effects[mech_name] = {
                        'mean': effect_mean,
                        'hdi': np.array([hdi_low, hdi_high])
                    }
                
                concept_mechanism_results[concept] = concept_effects
    
    # ========================================================================
    # MODEL 2: Psychological Mechanisms → Cheating Behavior  
    # ========================================================================
    print("Fitting: Psychological Mechanisms → Cheating Behavior")
    
    # Control baselines
    counts = control_baselines['cheating_counts']
    n_non, n_partial, n_full = counts[0], counts[1], counts[2]
    control_partial_logit = np.log(n_partial / n_non) if n_non > 0 else -2
    control_full_logit = np.log(n_full / n_non) if n_non > 0 else -1
    se_partial = np.sqrt(1/n_partial + 1/n_non) if n_partial > 0 and n_non > 0 else 1.0
    se_full = np.sqrt(1/n_full + 1/n_non) if n_full > 0 and n_non > 0 else 1.0
    
    with pm.Model() as mechanisms_to_cheating_model:
        # Control group baseline
        beta_partial_intercept = pm.Normal('beta_partial_intercept', mu=control_partial_logit, sigma=se_partial)
        beta_full_intercept = pm.Normal('beta_full_intercept', mu=control_full_logit, sigma=se_full)
        
        # Mechanism effects on cheating
        mech_effects_partial = pm.Normal('mech_effects_partial', mu=0, sigma=0.5, shape=len(mechanism_keys))
        mech_effects_full = pm.Normal('mech_effects_full', mu=0, sigma=0.5, shape=len(mechanism_keys))
        
        # Linear predictors
        eta_partial = beta_partial_intercept
        eta_full = beta_full_intercept
        
        for mech_idx in range(len(mechanism_keys)):
            eta_partial += mechanism_matrix[:, mech_idx] * mech_effects_partial[mech_idx]
            eta_full += mechanism_matrix[:, mech_idx] * mech_effects_full[mech_idx]
        
        # Multinomial logistic probabilities
        logits = pm.math.stack([pm.math.zeros(eta_partial.shape), eta_partial, eta_full], axis=1)
        probs = pm.math.softmax(logits, axis=1)
        
        pm.Categorical('cheating_obs', p=probs, observed=y_cheating)
    
    with mechanisms_to_cheating_model:
        trace_mech_cheating = pm.sample(1000, tune=500, chains=4, cores=4, random_seed=42, progressbar=False)
    
    # ========================================================================
    # MODEL 3: Psychological Mechanisms → Performance/Experience
    # ========================================================================
    print("Fitting: Psychological Mechanisms → Performance/Experience")
    
    control_means_perf = control_baselines['performance_by_cheating']
    control_means_exp = control_baselines['experience_by_cheating']
    
    with pm.Model() as mechanisms_to_outcomes_model:
        # Mechanism effects on outcomes BY CHEATING GROUP
        perf_mech_effects = pm.Normal('perf_mech_effects', mu=0, sigma=1.0, shape=(len(mechanism_keys), 3))
        exp_mech_effects = pm.Normal('exp_mech_effects', mu=0, sigma=0.3, shape=(len(mechanism_keys), 3))
        
        # Baselines by cheating group
        perf_baseline = pm.Normal('perf_baseline', mu=control_means_perf, sigma=2.0, shape=3)
        exp_baseline = pm.Normal('exp_baseline', mu=control_means_exp, sigma=0.3, shape=3)
        
        # Linear predictors
        mu_perf = perf_baseline[y_cheating]
        mu_exp = exp_baseline[y_cheating]
        
        for mech_idx in range(len(mechanism_keys)):
            mu_perf += mechanism_matrix[:, mech_idx] * perf_mech_effects[mech_idx, y_cheating]
            mu_exp += mechanism_matrix[:, mech_idx] * exp_mech_effects[mech_idx, y_cheating]
        
        # Likelihoods
        pm.Normal('performance', mu=mu_perf, sigma=pm.HalfNormal('perf_sigma', sigma=5.0), observed=y_performance)
        pm.Normal('experience', mu=mu_exp, sigma=pm.HalfNormal('exp_sigma', sigma=0.5), observed=y_experience)
    
    with mechanisms_to_outcomes_model:
        trace_mech_outcomes = pm.sample(1000, tune=500, chains=4, cores=4, random_seed=42, progressbar=False)
    
    # ========================================================================
    # Extract and format results
    # ========================================================================
    
    # Mechanisms → Cheating
    beta_partial_samples = trace_mech_cheating.posterior['beta_partial_intercept'].values.flatten()
    beta_full_samples = trace_mech_cheating.posterior['beta_full_intercept'].values.flatten()
    mech_effects_partial = trace_mech_cheating.posterior['mech_effects_partial'].values.reshape(-1, len(mechanism_keys))
    mech_effects_full = trace_mech_cheating.posterior['mech_effects_full'].values.reshape(-1, len(mechanism_keys))
    
    # Baseline probabilities
    baseline_logits = np.column_stack([np.zeros(len(beta_partial_samples)), beta_partial_samples, beta_full_samples])
    baseline_probs = np.exp(baseline_logits) / np.exp(baseline_logits).sum(axis=1, keepdims=True)
    
    mechanism_cheating_results = {}
    for i, mech_name in enumerate(mechanism_keys):
        # For 1 SD increase
        new_logits = np.column_stack([
            np.zeros(len(beta_partial_samples)),
            beta_partial_samples + mech_effects_partial[:, i],
            beta_full_samples + mech_effects_full[:, i]
        ])
        new_probs = np.exp(new_logits) / np.exp(new_logits).sum(axis=1, keepdims=True)
        
        # Probability changes (percentage points)
        non_change = (new_probs[:, 0] - baseline_probs[:, 0]) * 100
        partial_change = (new_probs[:, 1] - baseline_probs[:, 1]) * 100
        full_change = (new_probs[:, 2] - baseline_probs[:, 2]) * 100
        
        mechanism_cheating_results[mech_name] = {
            'non': {'mean': non_change.mean(), 'hdi': az.hdi(non_change, hdi_prob=0.95)},
            'partial': {'mean': partial_change.mean(), 'hdi': az.hdi(partial_change, hdi_prob=0.95)},
            'full': {'mean': full_change.mean(), 'hdi': az.hdi(full_change, hdi_prob=0.95)}
        }
    
    # Mechanisms → Performance/Experience
    perf_med_effects = trace_mech_outcomes.posterior['perf_mech_effects'].values.reshape(-1, len(mechanism_keys), 3)
    exp_med_effects = trace_mech_outcomes.posterior['exp_mech_effects'].values.reshape(-1, len(mechanism_keys), 3)
    
    mechanism_perf_results = {}
    mechanism_exp_results = {}
    
    for i, mech_name in enumerate(mechanism_keys):
        mechanism_perf_results[mech_name] = {
            'by_group': [
                {'mean': perf_med_effects[:, i, j].mean(), 'hdi': az.hdi(perf_med_effects[:, i, j], hdi_prob=0.95)}
                for j in range(3)
            ]
        }
        mechanism_exp_results[mech_name] = {
            'by_group': [
                {'mean': exp_med_effects[:, i, j].mean(), 'hdi': az.hdi(exp_med_effects[:, i, j], hdi_prob=0.95)}
                for j in range(3)
            ]
        }
    
    print("✓ Pathway analysis completed")
    
    return {
        'concept_to_mechanisms': concept_mechanism_results,
        'mechanisms_to_cheating': mechanism_cheating_results,
        'mechanisms_to_performance': mechanism_perf_results,
        'mechanisms_to_experience': mechanism_exp_results,
        'mechanism_names': mechanism_keys,
        'control_baselines': control_baselines
    }