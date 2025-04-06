---
layout: adr
title: Optimization Strategy in Stage 2
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - Objective Functions in Stage 1
    - Selection of Gaussian Process (GP) as Surrogate Model
status: deprecated
date: 2025-04-04
decision_makers:
    - elwardi
adr_tags:
  - backend
  - optimization
---

## Context and Problem Statement

After Stage 1 trains a generalized surrogate model across STL geometries,
Stage 2 must refine the prediction for a specific STL input.
This involves minimizing prediction uncertainty while optimizing (some of) the original objectives for that particular input.

What optimization strategy should Stage 2 use to effectively leverage the surrogate model and
balance uncertainty reduction with objective maximization?

## Decision Drivers

- Need to reduce predictive uncertainty (confidence interval width) for individual STL instances.
- Optimization must stay sample-efficient and leverage GP uncertainty.
- Should exploit structure learned in Stage 1 while refining to local optima.

## Considered Options

- **Minimize Confidence Interval Width directly**  
  Focused on uncertainty reduction, not necessarily performance improvement.

- **Multi-objective: combine uncertainty minimization with objective optimization**  
  Dual-focus strategy that refines prediction quality while improving suggested design.

- **Greedy or heuristic search using surrogate model mean**  
  Fast but ignores uncertainty and may fail in uncertain regions.

## Decision Outcome

Chosen option: **Multi-objective strategy combining confidence interval minimization
and original objective optimization**. This supports both certainty and effectiveness
in the final cell size recommendation.

### Consequences

- **Positive**: Produces confident, high-performing recommendations.
- **Neutral**: Requires tuning of trade-off parameter between uncertainty
           and performance, but this can be learned or adaptive.
- **Negative**: Optimization is slower than greedy methods due to dual objectives.

### Confirmation

Compliance is confirmed by:
- The list of objectives in `foamBO` configuration for stage 2 `problem.objectives` must contain
  both some original (core, stage 1) objectives like cell size, in addition to objectives
  representing reported surrogate uncertainties on the those original objectives.

## More information

- Currently, the implementation is not mature enough to consider this ADR as "enforced",
  so substantial experimentation is needed to figure out how to best perform the fine tuning.

This ADR will potentially be replaced by:
- Ditching BO for this stage and finding a better alternative
- Employing active learning, or even multi-fidelity BO
