---
layout: adr
title: Cross-Validation
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - Selection of Gaussian Process (GP) as Surrogate Model
    - STL Representation and Featurization
status: under-review
date: 2025-03-03
decision_makers:
    - elwardi
adr_tags:
  - backend
  - validation
---

## Context and Problem Statement

The success of the 2-stage Bayesian Optimization (BO) framework depends on the robustness
of the surrogate models, especially in terms of their generalization ability to unseen STL
inputs.

Proper validation is essential to ensure the surrogate model's performance and confidence
estimates are reliable.

How should we validate the performance of the surrogate model, ensuring both its accuracy
and uncertainty estimates before deployment in production?

## Decision Drivers

- Model must generalize well across different STL geometries and maintain accuracy and uncertainty.
- Validation strategy must be computationally feasible and scalable to large STL datasets.
- Cross-validation or a similar strategy is needed to avoid overfitting to the training dataset.

## Considered Options

- **foamBO's cross-validation**  
  Split the training set into `K` subsets and rotate through them for validation.
  Helps assess model stability and generalization across different STL geometries.

- **Leave-One-Out Cross-Validation (LOO-CV)**  
  Similar to K-fold but uses a single STL geometry as the validation set at a time.
  This could be computationally expensive for large datasets but ensures thorough testing for each input.

- **Bootstrap Resampling**  
  Sample subsets of the training data with replacement and train multiple models.
  Provides a way to estimate model variability and assess confidence intervals.

- **Hold-out Validation Set**  
  Split the dataset into a training set and a fixed hold-out validation set.
  Simpler and faster but may not be as robust as cross-validation methods for generalization.

## Decision Outcome


Chosen option: **Cross-validation from foamBO**, as it integrates directly with the Bayesian
Optimization framework and supports efficient K-fold cross-validation, including advanced
functionality for handling hyperparameter tuning.

### Consequences

- **Positive**: Utilizes Ax's built-in capabilities for cross-validation,
            streamlining the process and ensuring integration with the BO pipeline.
            It supports model tuning and optimization across multiple folds automatically.
- **Neutral**: While computationally feasible, using Ax may add some overhead in terms of
           learning how to integrate with the system. Still, the time saved by using an
           integrated solution outweighs this.
- **Negative**: Could be limited in customizability as implementing custom behavior will require
            changes to `foamBO` code.

### Confirmation

Compliance is confirmed by populating the `validate` section of the optimization configuration files.

## More information

For now, this has low priority since it can be performed after-the-fact, and is independent of the
training process.
