# Research Analysis: Concept-Based Interventions on Academic Cheating

## Overview

This notebook analyzes the effectiveness of concept-based interventions in reducing academic cheating behavior while examining their effects on performance and user experience.

### Research Questions

- **RQ1a**: Do concept-based interventions reduce cheating behavior?
- **RQ1b**: Do the effects on cheating vary by concepts?
- **RQ2a**: Do the interventions affect performance and user experience?
- **RQ2b**: Do the effects on performance and experience vary by concepts?
- **RQ3**: How do concept-based interventions influence cheating behavior, performance and user experience through psychological mechanisms?

---

## 1. Data Setup and Preparation

### Purpose

Load data, create cheating categories, and prepare variables for analysis.

### Technical Details

- Categorizes cheating rates: 0 = non-cheater, 0-1 = partial cheater, 1 = full cheater
- Creates composite experience variable from satisfaction + engagement
- Prepares categorical variables for Bayesian modeling
- Calculates correlation patterns to guide model selection (5/6 groups have |r|>0.1, justifying multivariate approach)

```python
# ============================================================================
# PROJECT FOLDER STRUCTURE & DATA PREPARATION
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az

# Load and prepare data
df = pd.read_csv("../data/final_dataset.csv")

def categorize_cheating(rate):
    if rate == 0: return 0  # Non-cheater
    elif rate == 1: return 2  # Full cheater
    else: return 1  # Partial cheater

df['cheating_behavior'] = df['cheating_rate_main_round'].apply(categorize_cheating)
df['experience'] = (df['task_satisfaction'] + df['task_engagement']) / 2
df['performance'] = df['performance_score_including_cheated_words']

print(f"Dataset: {len(df)} participants")
print(f"Control: {len(control_data)}, Intervention: {len(df) - len(control_data)}")
```

---

## 2. Analysis Section 1: Effects on Cheating Behavior (RQ1a & RQ1b)

### 2.1 Descriptive Statistics of Cheating Behavior

### Purpose

Examine raw cheating rates between control and intervention groups to identify initial patterns.

### Technical Details

- Calculates proportions with 95% confidence intervals
- Creates visualization comparing control vs intervention groups
- Breaks down by cheating categories (non/partial/full)

```python
# ============================================================================
# 5.6.1.1. Descriptive Statistics of Cheating Behavior
# ============================================================================

print("5.6.1.1. Descriptive Statistics of Cheating Behavior")

# Calculate descriptive statistics
control_data = df[df['concept'] == 'control']
intervention_data = df[df['concept'] != 'control']

# Create visualization and calculate proportions
# [Visualization code for Figure 1]
```

### Key Findings

- Control group: 46.6% cheated [35.1%, 58.0%]
- Intervention group: 36.7% cheated [33.9%, 39.4%]
- Interventions particularly reduced full cheating (32.9% → 19.2%)
- Generated **Figure 1**: Bar charts comparing control vs intervention groups

---

### 2.2 Statistical Analysis of Cheating Behavior

### Purpose

Use Bayesian multinomial logistic regression to test intervention effectiveness statistically.

### Technical Details

- **Model**: Multinomial logistic regression with 3 outcomes (non/partial/full cheater)
- **Priors**: Empirical priors from control group baseline
- **Random Effects**: Controls for motivational message variations
- **Estimation**: 1000 samples, 4 chains, target_accept=0.9

```python
# ============================================================================
# 5.6.1.2. Statistical Analyses of Effect of Interventions on Cheating Behavior
# ============================================================================

# Bayesian Multinomial Logistic Regression
with pm.Model() as cheating_model:
    # Control group baseline (empirical priors)
    beta_partial_intercept = pm.Normal('beta_partial_intercept', mu=control_partial_logit, sigma=se_partial)
    beta_full_intercept = pm.Normal('beta_full_intercept', mu=control_full_logit, sigma=se_full)

    # Concept effects
    concept_effects_partial = pm.Normal('concept_effects_partial', mu=-0.5, sigma=1.0, shape=len(concepts))
    concept_effects_full = pm.Normal('concept_effects_full', mu=-0.5, sigma=1.0, shape=len(concepts))

    # [Complete model specification]
```

### Key Results

- **Overall Effect**: +12% honest test-taking, -11% full cheating
- **Best Concepts**: Reference Group Identification (+17.4%), Cognitive Inconsistency (+14.3%), Autonomy (+13.5%), Verbal Persuasion (+12.8%)
- **Weakest Concepts**: Achievement-focused concepts (Performance Accomplishments, Emotional Arousal)
- Generated **Figure 2**: Overall intervention effect forest plot
- Generated **Figure 3**: Concept-specific effects by psychological theory

---

### 2.3 Forest Plots for Cheating Effects

### Purpose

Visualize overall and concept-specific intervention effects with uncertainty quantification.

### Technical Details

- Uses posterior samples to calculate 95% credible intervals
- Two plots: overall intervention effect and by-concept effects
- Color-codes by psychological theory
- Highlights most effective concept per theory

```python
# ============================================================================
# FOREST PLOTS FOR CHEATING BEHAVIOR (posterior with 95% HDI)
# ============================================================================

def create_forest_plots():
    # Plot 1: Overall intervention effect
    # Plot 2: By-concept effects grouped by theory
    # [Detailed plotting code]
```

---

## 3. Analysis Section 2: Effects on Performance and Experience (RQ2a & RQ2b)

### 3.1 Descriptive Statistics

### Purpose

Examine whether interventions affect performance and user experience outcomes.

### Technical Details

- Compares means and confidence intervals between groups
- Analyzes patterns by cheating behavior category
- Assesses correlation structures to guide modeling approach

```python
# ============================================================================
# 5.6.2.1 & 5.6.2.2. Descriptive Statistics of Performance and Experience
# ============================================================================

# Performance analysis
control_perf_stats = calculate_stats(control_perf, "Control group performance")
intervention_perf_stats = calculate_stats(intervention_perf, "Intervention group performance")

# Experience analysis
# [Similar analysis for experience ratings]
```

### Key Findings

- **Performance**: Minimal difference (Control: 20.60, Intervention: 19.34)
- **Experience**: Nearly identical (Control: 5.55, Intervention: 5.60 on 7-point scale)
- **No concerning patterns** across cheating behavior groups
- Generated **Figure 4**: Performance distributions by group and cheating behavior
- Generated **Figure 5**: Experience distributions by group and cheating behavior

---

### 3.2 Multivariate Statistical Analysis

### Purpose

Joint modeling of performance and experience outcomes accounting for their correlation.

### Technical Details

- **Model Choice**: Multivariate Bayesian model (5/6 groups had |r|>0.1)
- **Structure**: Hierarchical with concept × cheating category interactions
- **Correlation**: Models performance-experience correlation (ρ = 0.123)
- **Controls**: Random effects for motivational messages

```python
# ============================================================================
# 5.6.2.3. Statistical Analyses of Effect on Performance and User Experience
# ============================================================================

with pm.Model() as multivariate_model:
    # Control baselines by cheating category
    mu_exp_control = pm.Normal('mu_exp_control', mu=control_means_exp, sigma=0.3, shape=3)
    mu_perf_control = pm.Normal('mu_perf_control', mu=control_means_perf, sigma=3.0, shape=3)

    # Concept effects with interactions
    # [Complete multivariate model]
```

### Key Results

- **All 95% credible intervals include zero** for both outcomes
- **No performance costs** from interventions
- **No experience degradation** across any cheating group
- Interventions achieve integrity goals without negative side effects
- Generated **Figure 6**: Forest plot showing overall intervention effects on performance and experience by cheating group

---

### 3.3 Forest Plots for Performance and Experience Effects

### Purpose

Visualize overall intervention effects on performance and experience with uncertainty quantification.

### Technical Details

- Uses posterior samples from multivariate model
- Shows effects by cheating behavior groups (non/partial/full cheaters)
- Displays 95% credible intervals for all effects
- Includes control group baselines for context

```python
# ============================================================================
# FOREST PLOTS FOR PERFORMANCE AND EXPERIENCE (posterior)
# RQ2a & RQ2b: Do interventions affect performance/experience? Do effects vary by concepts?
# ============================================================================

def create_overall_effects_plot():
    """Create forest plot using pre-calculated overall effects"""

    # Control baselines for context
    control_baselines = {
        'Performance': control_means_perf,  # [14.67, 20.60, 30.25]
        'Experience': control_means_exp     # [5.52, 5.69, 5.55]
    }

    # Plot overall intervention effects with credible intervals
    # Separate panels for performance vs experience
    # [Detailed plotting code]
```

### Key Findings

- **Performance changes**: All near zero (range: -0.13 to +0.10 points)
- **Experience changes**: All minimal (range: -0.001 to +0.012 on 7-point scale)
- **No group differences**: Consistent null effects across cheating behaviors
- **Practical interpretation**: Interventions neither help nor harm these outcomes

---

## 4. Analysis Section 3: Psychological Mechanism Analysis (RQ3)

### 4.1 Psychological Mechanism Variable Setup

### Purpose

Identify and prepare psychological mechanisms and individual difference variables for pathway analysis.

### Technical Details

- **5 Psychological Mechanisms**: Need Satisfaction, Need Frustration, Self-Efficacy, Norm Perception, Cognitive Discomfort
- **2 Moderators**: Perceived Ability, Moral Disengagement
- **Standardization**: Z-scores for all continuous variables
- **Correlation Analysis**: Documents mechanism intercorrelations

```python
# ============================================================================
# 5.6.3.1. PSYCHOLOGICAL MECHANISM AND MODERATOR VARIABLES
# ============================================================================

# 5 psychological mechanisms (post-test, intervention-responsive)
mechanism_vars = {
    'overall_need_satisfaction': 'Need Satisfaction',
    'overall_need_frustration': 'Need Frustration',
    'task_specific_self_efficacy': 'Self Efficacy',
    'norm_perception': 'Norm Perception',
    'cognitive_discomfort': 'Discomfort'
}

# [Standardization and correlation analysis]
```

---

### 4.2 Psychological Mechanism Models

### Purpose

Test psychological pathways: Concepts → Mechanisms → Outcomes + Moderation effects.

### Technical Details

- **PATH A**: Concepts → Psychological Mechanisms (group-specific effects)
- **PATH B**: Psychological Mechanisms → Outcomes (controlling for direct effects)
- **PATH C'**: Direct concept → outcome effects
- **MODERATION**: Moderator × Concept interactions
- **Estimation**: Separate models for computational efficiency

```python
# ============================================================================
# 5.6.3.2. PSYCHOLOGICAL MECHANISM MODELS
# ============================================================================

# MODEL 1: Concepts → Psychological Mechanisms (PATH A)
with pm.Model() as mechanism_model:
    for mech_name, mech_values in available_mechanisms.items():
        # Group-specific baselines and concept effects
        # [Complete pathway model]

# MODEL 2: Psychological Mechanisms → Outcomes + Moderation
with pm.Model() as outcome_model:
    # PATH B: Mechanism → Performance/Experience
    # PATH C': Direct concept → outcomes
    # MODERATION: Moderator × Concept interactions
    # [Complete outcome model]
```

---

### 4.3 Concept → Psychological Mechanism Effects (PATH A)

### Purpose

Visualize which concepts activate which psychological mechanisms across cheating groups.

### Technical Details

- Heatmap showing concept → mechanism effects by cheating behavior categories
- Separate analysis for each mechanism (Need Satisfaction, Need Frustration, Self-Efficacy, Norm Perception, Cognitive Discomfort)
- Color-coded by psychological theory and effect magnitude
- Reports effects > |0.15| for interpretability

```python
# ============================================================================
# HEATMAP: CONCEPTS → PSYCHOLOGICAL MECHANISMS
# ============================================================================

def create_concept_mechanism_heatmap():
    # Create 2×3 subplot grid for 5 mechanisms
    # Heatmap: Concepts → Mechanisms → Groups
    # Color-coded by theory and group
    # [Heatmap visualization code]
```

### Key Findings

- **Need Satisfaction**: Strongest effects from Vicarious Experience (+0.375 for Full cheaters), Emotional Arousal (-0.276 for Partial cheaters)
- **Need Frustration**: Reduced by Vicarious Experience (-0.295 for Full cheaters), Reference Group Identification (-0.278 for Full cheaters)
- **Self-Efficacy**: Boosted by Vicarious Experience (+0.328 for Full cheaters), reduced by Verbal Persuasion (-0.302 for Full cheaters)
- **Norm Perception**: Enhanced by Vicarious Experience (+0.342 for Full cheaters), Dissonance Reduction (+0.311 for Full cheaters)
- **Cognitive Discomfort**: Increased by Self Concept (+0.397 for Full cheaters), reduced by Autonomy (-0.222 for Full cheaters)

---

### 4.4 Psychological Mechanism → Cheating Results (PATH B - Primary)

### Purpose

Test which psychological mechanisms effectively reduce cheating behavior.

### Technical Details

- Uses posterior samples to calculate probability changes for 1 SD increase in each mechanism
- Separate analysis for non-cheater, partial cheater, and full cheater outcomes
- Displays 95% credible intervals for all effects
- Identifies mechanisms with reliable effects (HDI excludes zero)

```python
# ============================================================================
# FOREST PLOT: PSYCHOLOGICAL MECHANISMS → CHEATING BEHAVIOR
# ============================================================================

def create_mechanisms_cheating_forest_plot():
    """Forest plot showing how psychological mechanisms affect cheating behavior"""

    # Calculate probability changes for 1 SD mechanism increase
    # Create forest plots for each cheating category
    # Highlight significant mechanism effects
    # [Detailed visualization code]
```

### Key Findings

- **Need Satisfaction**: Reduces non-cheating (-5.0% [-9.2, -1.0]) and increases full cheating (+4.4% [+0.9, +8.1])
- **Cognitive Discomfort**: Reduces non-cheating (-3.0% [-6.4, +0.3]) and increases full cheating (+4.0% [+1.1, +6.9])
- **Need Frustration, Self-Efficacy, Norm Perception**: No reliable effects (all HDIs include zero)
- Limited evidence for psychological mechanisms as primary drivers of intervention effects

---

### 4.5 Psychological Mechanism → Performance/Experience (PATH B - Validation)

### Purpose

Validate psychological mechanism measures by examining their effects on performance and experience outcomes.

### Technical Details

- Analyzes mechanism → outcome effects separately by cheating behavior group
- Uses stratified validation model to account for group differences
- Shows effects with 95% credible intervals
- Confirms expected patterns for measure validation

```python
# ============================================================================
# FOREST PLOT: PSYCHOLOGICAL MECHANISMS → PERFORMANCE/EXPERIENCE
# ============================================================================

def create_mechanisms_perf_exp_forest_plot():
    # Extract mechanism effects by cheating group
    # Create forest plots for performance vs experience
    # Show group-specific patterns
    # [Mechanism validation visualization]
```

### Key Findings

- **Need Satisfaction**: Positive effects on both performance (+1.2 to +1.4 points) and experience (+0.16 to +0.24 points)
- **Cognitive Discomfort**: Negative effects on both performance (-1.1 to -1.4 points) and experience (-0.14 to -0.31 points)
- **Need Frustration**: Negative effects on performance (-0.7 to -1.7 points), minimal experience effects
- **Self-Efficacy & Norm Perception**: Mixed effects across groups
- Confirms expected patterns, validating psychological mechanism measures

---

### 4.6 Moderation Analysis

### Purpose

Test whether individual differences (ability, moral disengagement) moderate intervention effectiveness.

### Technical Details

- Analyzes Moderator × Concept interactions
- Averages effects across all concepts for overall patterns
- Examines both performance and experience outcomes

```python
# ============================================================================
# FOREST PLOT: OVERALL MODERATION EFFECTS
# ============================================================================

def create_overall_moderation_forest_plot():
    # Extract moderation effects from posterior
    # Average across concepts for overall effects
    # Separate plots for performance vs experience
    # [Moderation visualization code]
```

### Key Findings

- **No significant moderation** by perceived ability or moral disengagement
- **All credible intervals include zero**
- **Interventions equally effective** across individual difference levels

---

### 4.7 Complete Pathway Analysis Summary

### Purpose

Comprehensive summary of all psychological mechanism pathways tested.

### Technical Details

- **180+ mechanism effects**: 15 concepts × 5 mechanisms × 2 outcomes × 3 groups
- **120+ moderation effects**: 2 moderators × 15 concepts × 2 outcomes × 3 groups
- **Posterior summaries**: Mean and 95% HDI for all effects

### Key Insights

- **Limited mechanism activation**: Most concept → mechanism effects are small
- **Sparse pathway evidence**: Few reliable mechanism → outcome pathways
- **No strong moderation**: Individual differences don't moderate intervention effectiveness
- **Direct effects dominate**: Interventions work primarily through direct pathways rather than measured psychological mechanisms
