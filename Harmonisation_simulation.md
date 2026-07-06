# Simulation plan for testing DiagnoseHarmonise harmonisation workflows

## Aim

Data harmonisation is the process by which technical differences are estimated and removed from data collected from different sources, scanners, sites, or batches. In tabular neuroimaging data, these differences may appear as shifts in feature means, changes in feature variance, or more complicated dependencies between batch, biological covariates, and derived image-derived phenotypes.

The aim of this simulation framework is to generate a series of controlled datasets with known technical bias structures, run one or more harmonisation methods on each dataset, and then use DiagnoseHarmonise to assess whether the simulated batch effects have been reduced without removing meaningful biological signal.

Most common tabular harmonisation methods use linear regression, location adjustment, scale adjustment, or variants of these approaches. Therefore, the simulations are deliberately organised from simple cases that match standard model assumptions through to more difficult cases involving non-linear covariate effects, covariate imbalance, interaction effects, and spatially structured feature effects.

## General notation

Let:

- \(Y_{i,j}\) be the observed value for subject/sample \(i\) and feature \(j\).
- \(i = 1, \dots, N\) index samples.
- \(j = 1, \dots, F\) index features.
- \(b(i)\) be the batch, site, scanner, or acquisition source for sample \(i\).
- \(X_i^k\) be the value of covariate \(k\) for sample \(i\), for example age, sex, diagnosis, disease status, or motion.
- \(\alpha_j\) be a feature-specific intercept.
- \(\beta_j^k\) be the effect of covariate \(k\) on feature \(j\).
- \(\gamma_{b,j}\) be an additive batch effect for batch \(b\) and feature \(j\).
- \(\delta_{b,j}\) be a multiplicative batch effect for batch \(b\) and feature \(j\).
- \(\epsilon_{i,j}\) be random noise.
- \(f_j(\cdot)\) represent a feature-specific non-linear covariate function.
- \(\theta_j^{k,l}\) represent an interaction effect between two covariates.
- \(\vartheta_{b,j}^k\) represent a batch-by-covariate interaction effect.

The base data matrix has shape \(N \times F\), where rows are samples and columns are features. These simulations are designed for feature-level harmonisation tests, not image-level harmonisation.

---

## Scenario 1: Standard batch model

### Purpose

This scenario tests the simplest case: linear covariate effects plus additive and/or multiplicative batch effects. This is the setting closest to the assumptions of standard ComBat-style harmonisation.

### Simulation equation

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### Suggested variants

Simulate several versions of this scenario by adding and removing terms:

1. No batch effect: biological covariates only.
2. Additive batch effect only: \(\gamma_{b,j}\).
3. Multiplicative batch effect only: \(\delta_{b,j}\epsilon_{i,j}\).
4. Additive and multiplicative batch effects together.

### What this tests

This simulation checks whether a harmonisation method can remove conventional location and scale batch effects while preserving linear biological covariate effects.

---

## Scenario 2: Non-linear covariate effects

### Purpose

This scenario tests whether harmonisation methods behave sensibly when the true biological covariate effects are not fully linear. For example, age may have a quadratic, spline-like, threshold, or saturating association with an imaging-derived feature.

### Simulation equation

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + f_j(X_i^k) + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

A more general version allows one or more continuous covariates to have non-linear effects:

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + \sum_k f_{j,k}(X_i^k) + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### Suggested variants

Useful choices for \(f_{j,k}\) include:

\[
f_{j,k}(X_i^k) = \lambda_{j,k}(X_i^k)^2
\]

\[
f_{j,k}(X_i^k) = \lambda_{j,k}\sin(X_i^k)
\]

\[
f_{j,k}(X_i^k) = \lambda_{j,k}\log(1 + X_i^k)
\]

The non-linear effect can be shared across features, feature-specific, or present only in a subset of features.

### What this tests

This simulation checks whether apparent residual batch effects are actually caused by model misspecification of biological covariates. A purely linear harmonisation model may incorrectly attribute non-linear biological variation to batch if covariates are unevenly distributed across batches.

---

## Scenario 3: Biological covariate interactions

### Purpose

This scenario tests the effect of interactions between biological covariates, such as age-by-sex, age-by-disease, disease-by-sex, or age-by-motion. These effects are biologically meaningful but may be difficult for simpler harmonisation models to preserve if they are not included in the design matrix.

### Simulation equation

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + \sum_{k < l} \theta_j^{k,l} X_i^k X_i^l + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### Example

For age and sex:

\[
Y_{i,j} = \alpha_j + \beta_j^{age}age_i + \beta_j^{sex}sex_i + \theta_j^{age,sex}(age_i \times sex_i) + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### What this tests

This simulation checks whether harmonisation preserves meaningful interaction effects between biological variables. It also tests whether omitting interaction terms leads to misleading conclusions about residual batch effects.

---

## Scenario 4: Covariate distributions depend on batch

### Purpose

This scenario tests a common multi-site problem: the biological covariate distribution differs between batches. For example, one site may contain older participants, a different sex ratio, more patients, or a different disease severity profile.

### Continuous covariates

For a continuous covariate, simulate the covariate distribution as batch-dependent:

\[
X_i^k \mid b(i)=b \sim \mathcal{N}(\mu_{b,k}, \sigma_{b,k}^2)
\]

This can be extended to non-Gaussian distributions, including skewed, heavy-tailed, or bimodal covariate distributions.

### Categorical covariates

For a binary categorical covariate:

\[
P(X_i^{categorical}=1 \mid b(i)=b) = p_b
\]

For example, disease prevalence or sex ratio may differ by batch.

### Outcome equation

The observed feature values can still be generated using the standard batch model:

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### What this tests

This simulation separates two issues that are often confused: genuine technical batch effects and biological differences that are correlated with batch. A good harmonisation method should reduce technical variation without removing biological structure that happens to be unevenly distributed across batches.

---

## Scenario 5: Covariate-by-batch interactions

### Purpose

This scenario tests cases where the covariate effect itself differs by batch. For example, the age effect may be steeper in one scanner than another, or disease effects may be measured differently across sites.

### Simulation equation

\[
Y_{i,j} = \alpha_j + \sum_k \beta_j^k X_i^k + \sum_k \vartheta_{b,j}^k X_i^k + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

This can also be written as a batch-specific covariate effect:

\[
Y_{i,j} = \alpha_j + \sum_k \left(\beta_j^k + \vartheta_{b,j}^k\right)X_i^k + \gamma_{b,j} + \delta_{b,j}\epsilon_{i,j}
\]

### What this tests

This simulation checks whether harmonisation methods can handle batch-dependent biological slopes. This is harder than simple location/scale correction because the technical effect is entangled with a covariate effect.

---

## Scenario 6: Combined complicated scenario

### Purpose

This scenario combines the previous mechanisms into a single difficult simulation. It is intended as a stress test for harmonisation workflows.

### Simulation equation

\[
Y_{i,j} = \alpha_j
+ \sum_k \beta_j^k X_i^k
+ \sum_{k < l} \theta_j^{k,l}X_i^kX_i^l
+ f_j(X_i^k, X_i^l)
+ \sum_k \vartheta_{b,j}^k X_i^k
+ \gamma_{b,j}
+ \delta_{b,j}\epsilon_{i,j}
\]

### Components included

This scenario may include:

- additive batch effects;
- multiplicative batch effects;
- uneven covariate distributions between batches;
- non-linear covariate effects;
- biological covariate interactions;
- covariate-by-batch interactions;
- feature-specific mixtures of the above effects.

### What this tests

This simulation assesses how harmonisation performs when several realistic sources of complexity occur together. It is useful for identifying failure modes, such as overcorrection, undercorrection, residual batch structure, or loss of biological signal.

---

## Scenario 7: Spatially dependent feature effects

### Purpose

Image-derived metrics often have spatial structure. Even when working with a tabular \(N \times F\) feature matrix, each feature may correspond to a spatial location, region, vertex, voxel, parcel, or tract. This scenario simulates spatially dependent covariate and batch effects while still testing tabular harmonisation methods.

### Feature locations

Assign each feature \(j\) a synthetic spatial coordinate:

\[
s_j = (x_j, y_j, z_j)
\]

where \(x_j\), \(y_j\), and \(z_j\) represent the simulated location of feature \(j\).

### Spatially dependent batch effects

Let additive and multiplicative batch effects vary smoothly or regionally over feature space:

\[
\gamma_{b,j} = g_b(s_j)
\]

\[
\delta_{b,j} = d_b(s_j)
\]

where \(g_b(\cdot)\) and \(d_b(\cdot)\) are spatial functions. For example, these could be generated using region labels, Gaussian fields, radial basis functions, or smooth coordinate-dependent functions.

### Spatially dependent covariate effects

The biological covariate effect can also vary by location:

\[
\beta_j^k = h_k(s_j)
\]

giving:

\[
Y_{i,j} = \alpha_j + \sum_k h_k(s_j)X_i^k + g_b(s_j) + d_b(s_j)\epsilon_{i,j}
\]

A more complicated spatial version can include non-linear and interaction effects:

\[
Y_{i,j} = \alpha_j
+ \sum_k h_k(s_j)X_i^k
+ \sum_k f_{j,k}(X_i^k)
+ \sum_{k < l}\theta_j^{k,l}X_i^kX_i^l
+ g_b(s_j)
+ d_b(s_j)\epsilon_{i,j}
\]

### What this tests

This simulation checks whether tabular harmonisation methods can handle feature effects that are not independent and identically distributed across the feature axis. It is especially relevant for image-derived phenotypes where adjacent or anatomically related features may share similar technical and biological effects.

---

## Recommended simulation workflow

For each scenario:

1. Generate covariates.
2. Generate feature-specific biological effects.
3. Generate batch labels.
4. Generate additive and/or multiplicative batch effects.
5. Generate the observed data matrix \(Y\).
6. Run the harmonisation method.
7. Run DiagnoseHarmonise before and after harmonisation.
8. Compare residual batch effects, retained covariate effects, and changes in feature variance/covariance structure.

## Suggested evaluation questions

For each simulation, record whether harmonisation:

- reduces mean differences between batches;
- reduces scale differences between batches;
- reduces batch separability in PCA, UMAP, clustering, or classification diagnostics;
- preserves known biological covariate effects;
- preserves known interaction effects when they are intended to remain;
- avoids removing biological signal that is unevenly distributed across batches;
- reduces spatially structured technical effects without flattening spatially structured biology.

## Practical Python implementation notes

A clean implementation should separate the simulation into modular functions, for example:

```python
def simulate_covariates(...):
    ...

def simulate_batch_labels(...):
    ...

def simulate_feature_effects(...):
    ...

def simulate_batch_effects(...):
    ...

def simulate_dataset(...):
    ...
```

Each function should return both the simulated values and the ground-truth parameters used to generate them. This makes it possible to evaluate not only whether harmonisation removes visible batch effects, but also whether it preserves the known biological effects built into the data.