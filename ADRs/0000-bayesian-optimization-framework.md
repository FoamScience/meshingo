---
layout: adr
title: Use of a 2-Stage Bayesian Optimization Framework
status: enforced
date: 2025-03-02
decision_makers:
    - elwardi
adr_tags:
  - backend
---

## Context and Problem Statement

The project aims to suggest "good-enough" cell sizes for input geometries represented as STL files.
A standard Bayesian Optimization (BO) loop may overfit to specific training geometries or fail
to balance exploration and precision efficiently.

How can we design the BO pipeline to generalize well across unseen STLs while refining cell
size predictions effectively?

## Decision Drivers

- [x] Need for generalization across varying STL geometries.
- [x] Importance of capturing uncertainty to guide efficient sampling.
- [x] Desire to decouple model training (generalization) from fine-tuning (precision).
- [x] Scalability to new datasets without retraining the full system.

## Considered Options

- **Single-stage Bayesian Optimization**  
  A monolithic BO pipeline that learns a surrogate model and performs optimization in one stage.

- **2-Stage Bayesian Optimization Framework**  
  - Stage 1 trains a general surrogate model on diverse STL geometries.  
  - Stage 2 uses this model to refine predictions and reduce confidence
    intervals.

## Decision Outcome

Chosen option: **2-Stage Bayesian Optimization Framework**, because it cleanly separates general
model learning from specific instance refinement. This supports better generalization (stage 1)
and targeted accuracy improvements (stage 2), in alignment with our decision drivers.

### Consequences

- **Positive**: Improves modularity; surrogate models can be reused across STL inputs.
             Enhances generalization and interpretability of uncertainty.
- **Neutral**: Requires more careful pipeline orchestration (between stages), but reuses most infrastructure.
- **Negative**: Increase in runtime and implementation complexity due to added coordination between stages.


### Confirmation

Compliance is confirmed by the presence of two discrete BO phases in the implementation, with clear interfaces:
1. Stage 1: Surrogate training on a diverse STL dataset.
2. Stage 2: Refinement using acquisition function conditioned on Stage 1 model.

## More information

To keep stage 1 as general as possible, the training STLs are not direct parameters, instead
geometric features and associated coefficients are used to select the "most similar" STL file
out of training data.
