---
layout: adr
title: Meshing Tool Selection for Stage 1
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - STL Representation and Featurization
status: enforced
date: 2025-03-03
decision_makers:
    - elwardi
adr_tags:
  - backend
  - meshing
---

## Context and Problem Statement

For Stage 1 of the 2-stage Bayesian Optimization pipeline, a flexible and robust meshing tool must be chosen
to mesh the STL files. The choice of the meshing tool will impact both the computational efficiency and th
e quality of the surrogate model's predictions.

What meshing tool should be selected for Stage 1 to ensure optimal mesh quality, performance,
and integration with OpenFOAM?

## Decision Drivers

- [x] The meshing tool must generate 3D hex-dominated meshes for OpenFOAM simulations
   - 2D meshes are less attractive for automated workflows
   - hex are chosen on a whim really
- [x] It must provide an efficient mesh generation process.
- [x] It should be flexible and scalable, handling complex geometries efficiently.

## Considered Options

- **cfMesh (CartesianMesh)**  
  A tool tailored for generating high-quality Cartesian grids for OpenFOAM.

- **snappyHexMesh**  
  A widely used meshing tool for OpenFOAM that can generate both hex-dominant meshes.
  More flexible but potentially slower for most meshing operations.

- **GMSH**  
  An open-source meshing tool that supports a variety of mesh types, including
  hex-dominant grids. However, it requires additional integration efforts with
  OpenFOAM and might be less efficient for large grids.

## Decision Outcome

Chosen option: **cfMesh (CartesianMesh)**, specifically for generating 3D
hex-dominated meshes. This tool only needs the maximal cell size as input.

### Consequences

- **Positive**: 
  - High-quality, hex-dominated mesh generation.
  - Low-maintenance requiring only a maximal cell size and feature edges.
  - Easy to add mesh features later, eg. Boundary layers, refinements, ..., etc
  - Can handle low-quality surface meshes well
  
- **Neutral**: 
  - Requires some initial setup (feature edges computation) and familiarity with
    cfMesh-specific parameters, but it is well-documented and widely used within the OpenFOAM community.
  
- **Negative**: 
  - Can produce the strangest meshing bugs due to its highly automated nature

### Confirmation

Compliance is confirmed by:
- The `template_case` must have a valid `system/meshDict`
- `template_case/Allrun.stage1` must call `cartesianMesh` to produce the ground truth
  for stage 1 training.

## More information

Alternatives to cfMesh might be more efficient and less error-prone but most of the
considered options require much more setup (eg. `snappyHexMesh` will require a pure-hex
background mesh, and a gazillion of settings in its `system/snappyMeshDict`).


