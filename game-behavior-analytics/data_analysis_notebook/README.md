# Research Analysis: Concept-Based Interventions on Academic Cheating

## Overview

This notebook analyzes the effectiveness of concept-based interventions in reducing academic cheating behavior while examining their effects on performance and user experience.

### Research Questions

- **RQ1a**: Do concept-based interventions reduce cheating behavior?
- **RQ1b**: Do the effects on cheating vary by concepts?
- **RQ2a**: Do the interventions affect performance and user experience?
- **RQ2b**: Do the effects on performance and experience vary by concepts?
- **RQ3**: How do concept-based interventions influence cheating behavior, performance and user experience?

---

## 1. Data Setup and Preparation

### Purpose

Load data, create cheating categories, and prepare variables for analysis.

### Technical Details

- Categorizes cheating rates: 0 = non-cheater, 0-1 = partial cheater, 1 = full cheater
- Creates composite experience variable from satisfaction + engagement
- Prepares categorical variables for Bayesian modeling
- Calculates correlation patterns to guide model selection

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
- **Best Concepts**: Reference Group Identification (+17.4%), Cognitive Inconsistency (+14.3%), Autonomy (+13.5%)
- **Weakest Concepts**: Achievement-focused concepts (Performance Accomplishments, Emotional Arousal)

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

## 4. Analysis Section 3: Mediation and Moderation Analysis (RQ3)

### 4.1 Mediator and Moderator Variable Setup

### Purpose

Identify and prepare psychological mechanisms and individual difference variables.

### Technical Details

- **4 Mediators**: Need Fulfillment, Self-Efficacy, Norm Perception, Cognitive Discomfort
- **2 Moderators**: Perceived Ability, Moral Disengagement
- **Standardization**: Z-scores for all continuous variables
- **Correlation Analysis**: Documents mediator intercorrelations

```python
# ============================================================================
# 5.6.3.1. MEDIATOR AND MODERATOR VARIABLES
# ============================================================================

# 4 mediators (post-test, intervention-responsive)
mediator_vars = {
    'overall_need_fulfillment': 'Need Fulfillment',
    'task_specific_self_efficacy': 'Self Efficacy',
    'norm_perception': 'Norm Perception',
    'cognitive_discomfort': 'Discomfort'
}

# [Standardization and correlation analysis]
```

---

### 4.2 Mediation and Moderation Models

### Purpose

Test psychological pathways: Concepts → Mediators → Outcomes + Moderation effects.

### Technical Details

- **PATH A**: Concepts → Mediators (group-specific effects)
- **PATH B**: Mediators → Outcomes (controlling for direct effects)
- **PATH C'**: Direct concept → outcome effects
- **MODERATION**: Moderator × Concept interactions
- **Estimation**: Separate models for computational efficiency

```python
# ============================================================================
# 5.6.3.2. MEDIATION + MODERATION MODELS
# ============================================================================

# MODEL 3A: Concepts → Mediators (PATH A)
with pm.Model() as mediator_model:
    for med_name, med_values in available_mediators.items():
        # Group-specific baselines and concept effects
        # [Complete mediation model]

# MODEL 3B: Mediators + Concepts → Outcomes + Moderation
with pm.Model() as outcome_model:
    # PATH B: Mediator → Performance/Experience
    # PATH C': Direct concept → outcomes
    # MODERATION: Moderator × Concept interactions
    # [Complete outcome model]
```

---

### 4.3 Mediation Results Visualization

### Purpose

Visualize which mediators effectively transmit intervention effects to outcomes.

### Technical Details

- Forest plots showing mediator → outcome effects (PATH B)
- Separate analysis for performance vs experience
- Groups results by cheating behavior categories
- Highlights significant pathways (HDI excludes zero)

```python
# ============================================================================
# FOREST PLOT: MEDIATORS → OUTCOMES (PATH B)
# ============================================================================

def create_path_b_forest_plot():
    # Extract PATH B effects from posterior
    # Create forest plots for each outcome
    # Highlight significant mediator effects
    # [Detailed visualization code]
```

### Key Findings

- **Need Fulfillment**: Positive effects on both performance and experience
- **Cognitive Discomfort**: Negative effects on both outcomes (harmful mediator)
- **Self-Efficacy & Norm Perception**: Mixed effects across groups
- **Limited mediation overall**: Most effects small and unreliable

---

### 4.4 Overall Intervention → Mediator Effects

### Purpose

Test whether interventions successfully activate intended psychological mediators.

### Technical Details

- Calculates overall intervention effects (averaged across concepts)
- Separate analysis for each cheating behavior group
- Uses standardized effect sizes for interpretability

```python
# ============================================================================
# FOREST PLOT: OVERALL INTERVENTION → MEDIATORS (PATH A)
# ============================================================================

def create_overall_intervention_mediators_plot():
    # Calculate overall effects across all concepts
    # Create 2×2 subplot for 4 mediators
    # Show effects by cheating group
    # [Visualization code]
```

### Key Findings

- **Minimal activation** of intended mediators
- **All effects near zero** with wide credible intervals
- **No reliable differences** across cheating behavior groups
- Limited support for intended psychological mechanisms

---

### 4.5 Moderation Analysis

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

### 4.6 Complete Pathway Results

### Purpose

Comprehensive summary of all mediation and moderation pathways tested.

### Technical Details

- **360 mediation effects**: 15 concepts × 4 mediators × 2 outcomes × 3 groups
- **180 moderation effects**: 2 moderators × 15 concepts × 2 outcomes × 3 groups
- **Indirect effects**: Calculated as PATH A × PATH B
- **Posterior summaries**: Mean and 95% HDI for all effects

```python
# ============================================================================
# FINAL RESULTS: ALL PATHWAYS
# ============================================================================

print("COMPLETE MEDIATION EFFECTS (Posterior Means + 95% HDI):")
# [Comprehensive results tables]

print("COMPLETE MODERATION EFFECTS (Posterior Means + 95% HDI):")
# [Complete moderation results]
```

---

### 4.7 Network Visualization

### Purpose

Visual summary of mediation patterns organized by psychological theory and cheating group.

### Technical Details

- **4×3 network grid**: Theories × cheating groups
- **Node types**: Concepts (colored by theory), mediators, outcomes
- **Edge thickness**: Proportional to effect size
- **Threshold**: Only shows effects > 0.03 for clarity

```python
# ============================================================================
# NETWORK VISUALIZATION: ALL CONCEPTS BY THEORY × CHEATING GROUPS
# ============================================================================

def create_theory_mediation_networks():
    # Create 4×3 subplot grid
    # Network graphs: Concepts → Mediators → Outcomes
    # Color-coded by theory and group
    # [Network visualization code]
```

### Key Insights

- **Theory-specific patterns**: Different theories show varying mediation strengths
- **Group differences**: Mediation patterns vary by cheating behavior
- **Sparse networks**: Most pathways are weak, suggesting limited mediation
