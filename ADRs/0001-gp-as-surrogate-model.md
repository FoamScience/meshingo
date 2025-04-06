---
layout: adr
title: Selection of Gaussian Process (GP) as Surrogate Model
related:
    - Use of a 2-Stage Bayesian Optimization Framework
status: enforced
date: 2025-03-02
decision_makers:
    - elwardi
adr_tags:
  - backend
---

## Context and Problem Statement

The surrogate model in the 2-stage Bayesian Optimization (BO) pipeline plays
a central role in approximating objective functions and quantifying uncertainty.
We need a model that supports efficient active learning, provides well-calibrated confidence intervals,
and handles small-to-moderate training datasets robustly.

What surrogate model architecture best aligns with these requirements?

## Decision Drivers

- Need for principled uncertainty estimation to guide sampling.
- Moderate dataset size where non-parametric methods remain feasible.
- Support for continuous input spaces and smooth objective functions.
- Compatibility with acquisition functions used by `ax-platform`.
- Availability in the `ax-platform` (hence in `foamBO`)

## Considered Options

- **Gaussian Process (GP)**  
  Non-parametric probabilistic model that offers posterior mean and variance estimates,
  well-suited for BO with small-to-medium data.

- **Random Forest Regressor (RF)**  
  Ensemble method that provides uncertainty estimates via bootstrapping,
  but may struggle with smooth function modeling and gradients.

- **Neural Network (NN) Surrogate**  
  Scalable and flexible, particularly in high dimensions. However, requires large
  datasets and more complex calibration for uncertainty estimation (e.g., via deep ensembles).

## Decision Outcome

Chosen option: **Gaussian Process (GP)**, because it provides closed-form posterior distributions,
strong uncertainty estimates, and performs well with limited training samples. This directly
supports both stages of the BO pipeline.

### Consequences

- **Positive**: Enables sample-efficient learning, integrates cleanly with automatically-picked acquisition 
            functions. Well-suited for low-sample, high-cost settings.
- **Neutral**: May require kernel tuning and scale poorly with very large datasets — but fits foreseeable problem size well.
- **Negative**: Limited scalability and fixed kernel assumptions may become bottlenecks in
            high-dimensional STL featurizations if not addressed.


### Confirmation

Compliance is confirmed by:
- `problem.models` in `foamBO` configuration files either says (`auto`, `GPEI` or `BOTORCH`)

## More information

- `SAASBO` effects are to be investigated.
- `auto` will generally pick a GP model given the continuous parameter space used.
