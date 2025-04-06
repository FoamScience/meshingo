---
layout: adr
title: STL Representation and Featurization
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - Selection of Gaussian Process (GP) as Surrogate Model
status: enforced
date: 2025-03-03
decision_makers:
    - elwardi
adr_tags:
  - backend
---

## Context and Problem Statement

Machine learning models require fixed-size, vectorized inputs but our inputs are
surface geometries. For the BO framework to operate effectively, raw STL geometries
must transform into meaningful, learnable features.

What representation best captures shape characteristics while enhancing the discovery
around optimization objectives (mainly cell count, cell size, and possible mesh issues)?

## Decision Drivers

- [x] Must preserve key geometric or topological features relevant to cell size optimization.
- [x] Featurization should produce fixed-length, continuous vectors.
- [x] Efficiency and scalability across large STL datasets.
- [ ] Representation must be invariant to rotation, scale, and mesh resolution.

## Considered Options

- **Voxelization**  
  Convert the 3D space into a binary or occupancy grid.
  Simple but resolution-limited and memory-heavy.

- **Shape Embedding via PointNet or Deep Learning**  
  Use a neural network to embed point clouds or mesh features into a latent space.
  High expressivity, but requires training and may generalize poorly out-of-the-box.

- **Hand-crafted Geometric Features (e.g., minimum edge length, sharpness, flatness, volume-to-surface ratio... etc)**  
  Fast to compute and interpretable, but may miss fine-grained shape nuances.

## Decision Outcome

Chosen option: **Hand-crafted Geometric Features**.  This balances expressiveness and interpretability,
while remaining compatible with GP modeling and generalization across diverse STLs.

### Consequences

- **Positive**: Captures detailed geometry. Generalizes across surface types and scales.
- **Neutral**: Requires pre-computation of geometric features of training/target STLs,
           but the pipeline is reusable and is not expected to be computationally expensive.
- **Negative**: Introduces moderate preprocessing time; and creates a possible decoupling between
            surrogate models and the way geometric features were computed while training them.


### Confirmation

Compliance is confirmed by:
- Existence and usage of `compute-geometric-features` entry point in the `meshingo` Python package.
- The CLI calls this entry point before the training starts.

## More information

Saving computed geometric features to a CSV simplifies choosing the most similar STL for the parameters
suggested by the surrogate model. But it opens a gate for de-coupling the surrogate model from the
way the features were computed for its training. This is currently unresolved.
