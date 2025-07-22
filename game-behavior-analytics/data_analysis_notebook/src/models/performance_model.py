"""
Performance and experience analysis with message effects
"""

import pymc as pm
import numpy as np
import arviz as az

def analyze_performance_experience(df, encoding_info):
    """Analyze performance and experience outcomes with detailed results."""
    
    # Check correlations like original analysis
    corr_results = []
    cheating_labels = {0: 'Non-cheaters', 1: 'Partial cheaters', 2: 'Full cheaters'}
    
    for group_name, group_data in [('Control', df[df['concept'] == 'control']), 
                                   ('Intervention', df[df['concept'] != 'control'])]:
        for cheat_cat in [0, 1, 2]:
            subset = group_data[group_data['cheating_behavior'] == cheat_cat]
            if len(subset) >= 10:
                corr = subset[['performance', 'experience']].corr().iloc[0, 1]
                corr_results.append({
                    'Group': group_name,
                    'Cheating Category': cheating_labels[cheat_cat],
                    'n': len(subset),
                    'Correlation': round(corr, 3) if corr is not None else 'NA'
                })
                
    # Decision criterion like original
    significant_corrs = sum(
        1 for row in corr_results
        if isinstance(row['Correlation'], float) and abs(row['Correlation']) > 0.1 and row['n'] >= 10
    )
    use_multivariate = significant_corrs >= 3
    
    print(f"Decision: {significant_corrs}/6 groups have |r|>0.1")
    print(f"Using {'multivariate' if use_multivariate else 'separate'} model(s)")
    
    # Calculate descriptive statistics
    control_data = df[df['concept'] == 'control']
    intervention_data = df[df['concept'] != 'control']
    
    descriptive_stats = calculate_descriptive_stats(control_data, intervention_data)
    
    # Prepare data
    y_performance = df['performance'].values
    y_experience = df['experience'].values
    y_cheating = df['cheating_behavior'].values
    concept_codes = df['concept_codes'].values
    concepts = encoding_info['concepts']
    control_baselines = encoding_info['control_baselines']
    
    # Prepare message codes like original analysis
    message_ids = df['motivational_message_id'].astype('category')
    message_codes = message_ids.cat.codes.values
    
    if use_multivariate:
        effects = fit_multivariate_model(y_performance, y_experience, y_cheating, 
                                       concept_codes, concepts, control_baselines, 
                                       message_codes, message_ids)
    else:
        effects = fit_separate_models(y_performance, y_experience, y_cheating,
                                    concept_codes, concepts, control_baselines,
                                    message_codes, message_ids)
    
    # Add descriptive stats to results
    effects['descriptive_stats'] = descriptive_stats
    effects['correlation_results'] = corr_results
    
    print("✓ Performance/experience analysis completed")
    return effects

def calculate_descriptive_stats(control_data, intervention_data):
    """Calculate descriptive statistics like original analysis."""
    
    def calc_stats(data, name):
        mean_val = data.mean()
        std_val = data.std()
        n = len(data)
        se = std_val / np.sqrt(n)
        ci_low = mean_val - 1.96 * se
        ci_high = mean_val + 1.96 * se
        return {
            'name': name,
            'n': n,
            'mean': mean_val,
            'std': std_val,
            'ci_low': ci_low,
            'ci_high': ci_high
        }
    
    stats = {
        'performance': {
            'control': calc_stats(control_data['performance'], 'Control performance'),
            'intervention': calc_stats(intervention_data['performance'], 'Intervention performance')
        },
        'experience': {
            'control': calc_stats(control_data['experience'], 'Control experience'), 
            'intervention': calc_stats(intervention_data['experience'], 'Intervention experience')
        }
    }
    
    # By cheating behavior
    cheating_labels = {0: 'Non-cheater', 1: 'Partial cheater', 2: 'Full cheater'}
    
    for outcome in ['performance', 'experience']:
        stats[outcome]['by_cheating'] = {}
        
        for group_name, group_data in [('Control', control_data), ('Intervention', intervention_data)]:
            stats[outcome]['by_cheating'][group_name] = {}
            for cheat_cat in [0, 1, 2]:
                subset = group_data[group_data['cheating_behavior'] == cheat_cat][outcome]
                if len(subset) > 0:
                    stats[outcome]['by_cheating'][group_name][cheat_cat] = {
                        'mean': subset.mean(),
                        'std': subset.std(),
                        'n': len(subset)
                    }
    
    return stats

def fit_multivariate_model(y_perf, y_exp, y_cheat, concept_codes, concepts, baselines, 
                          message_codes, message_ids):
    """Fit multivariate model for correlated outcomes like original analysis."""
    
    with pm.Model() as model:
        # Control baselines by cheating category
        mu_perf_ctrl = pm.Normal('mu_perf_ctrl', mu=baselines['performance_by_cheating'], sigma=3.0, shape=3)
        mu_exp_ctrl = pm.Normal('mu_exp_ctrl', mu=baselines['experience_by_cheating'], sigma=0.3, shape=3)
        
        # Concept effects (main effects)
        concept_perf_main = pm.Normal('concept_perf_main', mu=0, sigma=2.0, shape=len(concepts))
        concept_exp_main = pm.Normal('concept_exp_main', mu=0, sigma=0.2, shape=len(concepts))
        
        # Concept × cheating category interactions
        concept_perf_interactions = pm.Normal('concept_perf_interactions', mu=0, sigma=1.5, shape=(len(concepts), 3))
        concept_exp_interactions = pm.Normal('concept_exp_interactions', mu=0, sigma=0.15, shape=(len(concepts), 3))
        
        # Message effects (like original analysis)
        msg_perf = pm.Normal('msg_perf', mu=0, sigma=0.5, shape=len(message_ids.cat.categories))
        msg_exp = pm.Normal('msg_exp', mu=0, sigma=0.1, shape=len(message_ids.cat.categories))
        
        # Linear predictors
        mu_perf = (mu_perf_ctrl[y_cheat] + msg_perf[message_codes] +
                   pm.math.switch(concept_codes > 0,
                                 concept_perf_main[concept_codes - 1] + concept_perf_interactions[concept_codes - 1, y_cheat], 0))

        mu_exp = (mu_exp_ctrl[y_cheat] + msg_exp[message_codes] +
                  pm.math.switch(concept_codes > 0,
                                concept_exp_main[concept_codes - 1] + concept_exp_interactions[concept_codes - 1, y_cheat], 0))
        
        # Covariance structure
        sigma_perf = pm.HalfNormal('sigma_perf', sigma=5.0)
        sigma_exp = pm.HalfNormal('sigma_exp', sigma=0.4)
        rho = pm.Uniform('rho', lower=-0.5, upper=0.5)
        
        cov = pm.math.stack([[sigma_exp**2, rho*sigma_exp*sigma_perf],
                            [rho*sigma_exp*sigma_perf, sigma_perf**2]])
        
        # Multivariate likelihood
        outcomes = pm.math.stack([y_exp, y_perf], axis=1)
        means = pm.math.stack([mu_exp, mu_perf], axis=1)
        pm.MvNormal('outcomes', mu=means, cov=cov, observed=outcomes)
    
    with model:
        trace = pm.sample(1000, tune=500, chains=4, cores=1, target_accept=0.9, random_seed=42, progressbar=False)
    
    # Calculate overall effects by cheating group (like original analysis)
    exp_main = trace.posterior['concept_exp_main'].values.reshape(-1, len(concepts))
    exp_int = trace.posterior['concept_exp_interactions'].values.reshape(-1, len(concepts), 3)
    perf_main = trace.posterior['concept_perf_main'].values.reshape(-1, len(concepts))
    perf_int = trace.posterior['concept_perf_interactions'].values.reshape(-1, len(concepts), 3)

    # Calculate overall effects (raw score differences from control)
    overall_perf_non = np.mean([perf_main[:, i] + perf_int[:, i, 0] for i in range(len(concepts))], axis=0)
    overall_perf_partial = np.mean([perf_main[:, i] + perf_int[:, i, 1] for i in range(len(concepts))], axis=0)
    overall_perf_full = np.mean([perf_main[:, i] + perf_int[:, i, 2] for i in range(len(concepts))], axis=0)

    overall_exp_non = np.mean([exp_main[:, i] + exp_int[:, i, 0] for i in range(len(concepts))], axis=0)
    overall_exp_partial = np.mean([exp_main[:, i] + exp_int[:, i, 1] for i in range(len(concepts))], axis=0)
    overall_exp_full = np.mean([exp_main[:, i] + exp_int[:, i, 2] for i in range(len(concepts))], axis=0)

    # Store results exactly like original analysis
    multivariate_results = {
        'perf_non': {'mean': overall_perf_non.mean(), 'hdi': az.hdi(overall_perf_non, hdi_prob=0.95)},
        'perf_partial': {'mean': overall_perf_partial.mean(), 'hdi': az.hdi(overall_perf_partial, hdi_prob=0.95)},
        'perf_full': {'mean': overall_perf_full.mean(), 'hdi': az.hdi(overall_perf_full, hdi_prob=0.95)},
        'exp_non': {'mean': overall_exp_non.mean(), 'hdi': az.hdi(overall_exp_non, hdi_prob=0.95)},
        'exp_partial': {'mean': overall_exp_partial.mean(), 'hdi': az.hdi(overall_exp_partial, hdi_prob=0.95)},
        'exp_full': {'mean': overall_exp_full.mean(), 'hdi': az.hdi(overall_exp_full, hdi_prob=0.95)}
    }
    
    # Calculate concept-specific effects like cheating model
    concept_effects = calculate_concept_effects(trace, concepts, baselines)
    
    return {
        'multivariate_results': multivariate_results,
        'concept_effects': concept_effects,
        'baselines': baselines,
        'trace': trace,
        'model': model
    }

def calculate_concept_effects(trace, concepts, baselines):
    """Calculate concept-specific effects for performance and experience."""
    
    exp_main = trace.posterior['concept_exp_main'].values.reshape(-1, len(concepts))
    exp_int = trace.posterior['concept_exp_interactions'].values.reshape(-1, len(concepts), 3)
    perf_main = trace.posterior['concept_perf_main'].values.reshape(-1, len(concepts))
    perf_int = trace.posterior['concept_perf_interactions'].values.reshape(-1, len(concepts), 3)
    
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
    
    concept_effects = []
    
    for concept in theory_order:
        if concept in concepts:
            i = concepts.index(concept)
    
            # Performance effects by cheating group
            perf_non_effect = perf_main[:, i] + perf_int[:, i, 0]
            perf_partial_effect = perf_main[:, i] + perf_int[:, i, 1]
            perf_full_effect = perf_main[:, i] + perf_int[:, i, 2]
            
            # Experience effects by cheating group
            exp_non_effect = exp_main[:, i] + exp_int[:, i, 0]
            exp_partial_effect = exp_main[:, i] + exp_int[:, i, 1]
            exp_full_effect = exp_main[:, i] + exp_int[:, i, 2]
            
            concept_effects.append({
                'concept': concept,
                'concept_label': concept.replace('_', ' ').title(),
                'theory': theory_map.get(concept, 'Unknown Theory'),
                # Performance effects
                'perf_non_mean': perf_non_effect.mean(),
                'perf_non_hdi': az.hdi(perf_non_effect, hdi_prob=0.95),
                'perf_partial_mean': perf_partial_effect.mean(),
                'perf_partial_hdi': az.hdi(perf_partial_effect, hdi_prob=0.95),
                'perf_full_mean': perf_full_effect.mean(),
                'perf_full_hdi': az.hdi(perf_full_effect, hdi_prob=0.95),
                # Experience effects
                'exp_non_mean': exp_non_effect.mean(),
                'exp_non_hdi': az.hdi(exp_non_effect, hdi_prob=0.95),
                'exp_partial_mean': exp_partial_effect.mean(),
                'exp_partial_hdi': az.hdi(exp_partial_effect, hdi_prob=0.95),
                'exp_full_mean': exp_full_effect.mean(),
                'exp_full_hdi': az.hdi(exp_full_effect, hdi_prob=0.95)
            })
    
    return concept_effects

def fit_separate_models(y_perf, y_exp, y_cheat, concept_codes, concepts, baselines,
                       message_codes, message_ids):
    """Fit separate models for uncorrelated outcomes."""
    
    results = {}
    
    for outcome_name, y_outcome, sigma_prior, baseline_key in [
        ('performance', y_perf, 5.0, 'performance_by_cheating'),
        ('experience', y_exp, 0.5, 'experience_by_cheating')
    ]:
        
        with pm.Model() as model:
            mu_ctrl = pm.Normal('mu_ctrl', mu=baselines[baseline_key], sigma=1.0, shape=3)
            concept_effects = pm.Normal('concept_effects', mu=0, sigma=1.0, shape=len(concepts))
            msg_effects = pm.Normal('msg_effects', mu=0, sigma=0.5, shape=len(message_ids.cat.categories))
            
            mu = (mu_ctrl[y_cheat] + msg_effects[message_codes] + 
                  pm.math.switch(concept_codes > 0, concept_effects[concept_codes - 1], 0))
            sigma = pm.HalfNormal('sigma', sigma=sigma_prior)
            pm.Normal('outcome', mu=mu, sigma=sigma, observed=y_outcome)
        
        with model:
            trace = pm.sample(1000, tune=500, chains=4, cores=4, random_seed=42, progressbar=False)
        
        effects = trace.posterior['concept_effects'].values.flatten()
        results[outcome_name] = {'mean': effects.mean(), 'hdi': az.hdi(effects)}
    
    results['baselines'] = baselines
    return results