Mathematical Equation for the Multinomial Logistic Regression Model
The provided PyMC code implements a multinomial logistic regression model for a 3-category outcome (non-cheater, partial cheater, full cheater). Here's the mathematical representation:

Logit Equations
For participant $j$ with concept index $i$:

$$\mathbf{L}j = \begin{bmatrix} 0 \ \beta{\text{partial}} + \gamma_{\text{partial},i} \ \beta_{\text{full}} + \gamma_{\text{full},i} \end{bmatrix}$$

Where:

$\beta_{\text{partial}}$ and $\beta_{\text{full}}$ are intercept terms
$\gamma_{\text{partial},i}$ and $\gamma_{\text{full},i}$ are concept-specific effects
The first category (non-cheater) serves as the reference category with logit fixed at 0
Probability Calculation (Softmax)
The probabilities for each category are calculated using the softmax function:

$$P(Y_j = k) = \frac{e^{L_{j,k}}}{\sum_{m=1}^{3} e^{L_{j,m}}} \quad \text{for } k \in {1,2,3}$$

Likelihood Function
The observed cheating behavior is modeled as:

$$Y_j \sim \text{Categorical}(P(Y_j = 1), P(Y_j = 2), P(Y_j = 3))$$

This models the probability of each participant falling into one of the three cheating behavior categories based on the concept they were exposed to.
