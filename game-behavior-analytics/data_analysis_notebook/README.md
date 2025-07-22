# Research Analysis: Concept-Based Interventions on Academic Cheating

## Research Story & Analysis Guide

This research investigates whether simple psychological messages can reduce academic cheating without harming student performance or experience. The analysis follows a systematic progression from basic questions to deeper mechanistic understanding.

### Core Research Questions

- **RQ1**: Do concept-based interventions reduce cheating? Which concepts work best?
- **RQ2**: Do interventions create unwanted side effects on performance or experience?
- **RQ3**: How do these interventions actually work psychologically?

---

## Project Structure

```
game-behavior-analytics/
├── data/
│   └── final_dataset.xlsx              # Research dataset
├── src/
│   ├── data/
│   │   ├── data_loader.py             # Load and validate data
│   │   └── preprocessor.py            # Create derived variables
│   ├── models/
│   │   ├── cheating_model.py          # Bayesian cheating analysis
│   │   ├── performance_model.py       # Performance/experience analysis
│   │   ├── pathway_model.py           # Pathway analysis
│   │   └── network_model.py           # Network analysis
│   └── visualization/
│       └── plots.py                   # All plotting functions
└── notebooks/
    └── analysis.ipynb           # Main analysis notebook
```

---

## Analysis Journey

### Step 1: Data Preparation - Setting the Foundation

**The Question**: How do we measure cheating behavior in a meaningful way?

**Our Approach**: We categorize participants into three groups based on their cheating intensity:

- **Non-cheaters** (0% cheating rate)
- **Partial cheaters** (some cheating, but not everything)
- **Full cheaters** (100% cheating rate)

This three-category system captures the reality that cheating isn't binary - people cheat to different degrees.

```python
# Creates cheating categories and composite variables
from src.data.data_loader import load_and_validate_data
from src.data.preprocessor import preprocess_data
```

---

### Step 2: RQ1 - Does It Work? (Cheating Behavior Analysis)

**The Question**: Do our psychological messages actually reduce cheating compared to a control group?

**Why This Matters**: Before diving into mechanisms, we need to establish that the intervention works at all. This is our primary effectiveness test.

#### 2.1 Looking at the Raw Numbers

We start with simple descriptive statistics to see the basic pattern:

- Control group: 46.6% cheated
- Intervention groups: 36.7% cheated

This gives us initial evidence, but we need statistical models to be confident.

#### 2.2 Bayesian Statistical Model

**Why Bayesian?** Traditional statistics give us p-values, but Bayesian methods give us probability distributions - we can say "there's a 95% chance the effect is between X and Y."

**Why Multinomial Logistic Regression?** Since we have three cheating categories (none/partial/full), we need a model that handles multiple outcomes simultaneously.

**Model Logic**:

```
For each person: P(cheating level) = f(intervention concept + control variables)
```

**What We Found**: Interventions increase honest behavior by ~12% and reduce full cheating by ~11%. Some concepts (like "Reference Group Identification") work much better than others.

```python
from src.models.cheating_model import analyze_cheating_behavior
cheating_trace, cheating_effects = analyze_cheating_behavior(df, encoding_info)
```

---

### Step 3: RQ2 - What's the Cost? (Performance & Experience Analysis)

**The Question**: Do interventions create unintended negative consequences?

**Why This Matters**: Educators worry that integrity interventions might stress students or harm performance. We need to test this concern directly.

**The Challenge**: Performance and experience are related - students who perform better often enjoy the task more. We need to model them together.

#### Multivariate Bayesian Model

**Why Multivariate?** We model performance and experience simultaneously because they're correlated (r ≈ 0.12). Separate models would ignore this relationship.

**Why Hierarchical?** The relationship between performance and experience varies by cheating group, so we allow flexible effects.

**Model Logic**:

```
Performance = f(baseline by cheating group + intervention effects + correlation with experience)
Experience = f(baseline by cheating group + intervention effects + correlation with performance)
```

**What We Found**: No meaningful effects on either outcome. All effects hover around zero with wide confidence intervals - interventions don't help or harm these outcomes.

```python
from src.models.performance_model import analyze_performance_experience
perf_exp_effects = analyze_performance_experience(df, encoding_info)
```

---

### Step 4: RQ3 - How Does It Work? (Psychological Mechanisms)

**The Question**: If interventions work without side effects, what's happening psychologically?

**Why This Matters**: Understanding mechanisms helps us design better interventions and explains why some concepts work better than others.

#### 4.1 Pathway Analysis - Following the Causal Chain

**The Theory**: Interventions → activate psychological mechanisms → change behavior

We test this in separate steps:

1. Do concepts activate intended psychological mechanisms?
2. Do activated mechanisms influence cheating behavior?
3. Do mechanisms also influence performance/experience?

**Why Separate Models?** Complex mediation is hard to estimate in one model. Separate models let us isolate each causal step clearly.

**The Mechanisms We Test**:

- **Need Satisfaction/Frustration** (from Self-Determination Theory)
- **Self-Efficacy** (confidence in abilities)
- **Norm Perception** (what others do/expect)
- **Cognitive Discomfort** (psychological tension from inconsistency)

**What We Found**: Limited evidence for the intended pathways. Most mechanisms show weak activation and small effects on outcomes.

```python
from src.models.pathway_model import analyze_psychological_pathways
pathway_results = analyze_psychological_pathways(df, encoding_info)
```

#### 4.2 Network Analysis - The Big Picture

**The Question**: How do psychological variables connect to each other and outcomes?

**Why Networks?** Instead of assuming linear pathways, networks reveal the full pattern of psychological connections.

**Method**: Partial correlation networks show which variables are directly connected (controlling for all others).

**What We Found**: Sparse networks with few strong connections, suggesting simple psychological structures rather than complex mediation.

```python
from src.models.network_model import analyze_networks_by_concept
network_results, labels = analyze_networks_by_concept(df)
```

---

## Research Insights

### What Works

- **Concept-based interventions effectively reduce cheating** (especially full cheating)
- **No performance or experience costs** - addressing educator concerns
- **Some concepts much more effective** than others, suggesting targeted design matters

### What We Don't Fully Understand

- **Mechanisms remain unclear** - traditional psychological pathways show weak effects
- **Alternative explanations needed** - interventions work, but not through expected routes
- **Individual differences** may play larger roles than captured

### Implications for Practice

- **Safe to implement** - no evidence of harmful side effects
- **Focus on effective concepts** - Reference Group Identification, Cognitive Inconsistency, Autonomy
- **Avoid achievement-focused messages** - Performance Accomplishments, Emotional Arousal show weaker effects

---

## Using This Code

The analysis follows this logical progression in `analysis.ipynb`:

1. **Data Setup** → Clean and categorize variables
2. **Descriptive Analysis** → Explore raw patterns
3. **RQ1 Models** → Test intervention effectiveness
4. **RQ2 Models** → Test for side effects
5. **RQ3 Models** → Investigate mechanisms
6. **Interpretation** → Synthesize findings

Each code section includes model diagnostics (trace plots, convergence checks) to ensure reliable results.

---

## Technical Requirements

```
pymc >= 5.0      # Bayesian modeling
arviz >= 0.15    # Model diagnostics
pandas >= 1.5    # Data manipulation
numpy >= 1.24    # Numerical computing
matplotlib >= 3.6 # Visualization
scikit-learn >= 1.2 # Network estimation
```
