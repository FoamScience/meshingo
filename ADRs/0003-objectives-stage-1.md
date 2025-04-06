---
layout: adr
title: Objective Functions in Stage 1
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - Selection of Gaussian Process (GP) as Surrogate Model
    - STL Representation and Featurization
status: enforced
date: 2025-03-03
decision_makers:
    - elwardi
adr_tags:
  - backend
  - optimization
---

## Context and Problem Statement

Stage 1 of the BO pipeline trains a general surrogate model across multiple STL geometries.
To do this effectively, the model must learn objectives that encourage generalization rather
than overfitting to specific STL instances. The need for multi-objective optimizations is pretty
much an assumption here.

What objective functions should Stage 1 optimize to ensure the surrogate model remains
broadly useful for unseen STL inputs?

## Decision Drivers

- Surrogate model should generalize across STL geometries, not memorize.
- Objectives must capture performance-relevant characteristics for downstream cell size prediction.
- The model must support uncertainty-aware optimization in Stage 2.
- Model must be trainable with moderate computational resources.

## Considered Options

- **Direct loss on ground-truth cell size, and few other aspects**
  Straightforward regression objective, but risks overfitting and lacks uncertainty-awareness.

- **Variational or probabilistic loss (e.g., Negative Log Likelihood)**  
  Encourages well-calibrated uncertainty estimates; more compatible with BO framework.

- **Meta-objectives: generalization gap, variance minimization across tasks**  
  Focuses on learning transferable patterns rather than local accuracy.

## Decision Outcome

Chosen option: **Multi-objective loss combining direct losses on cell size, cell count,
possible mesh issues, and surface-to-mesh volume ratio**. This encourages the model
to be accurate while also confident and general across different STL geometries.

### Consequences

- **Positive**: Encourages well-calibrated predictions with strong generalization.
            Supports informative uncertainty estimates needed in Stage 2.
- **Neutral**: Requires tuning of weights between multiple objectives, but manageable in practice by simply decaying some.
- **Negative**: May require more careful cross-validation.

### Confirmation

Compliance is confirmed by:
- The list of objectives in `foamBO` configuration for stage 1 `problem.objectives` must reflect
  the mentioned aspects.

## More information

- The use of thresholds on these objectives is debatable...
- The objective values are "normalized" to some extent, essentially to make judging the
  model's hyper volume easier (leading to easier convergence confidence)
