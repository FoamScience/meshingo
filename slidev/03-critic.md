---
transition: fade-in
layout: two-cols
layoutClass: gap-16
---

# Critique and Discussions

- Focusing on **Automation & Unattended Meshing**
- Data-Efficient Surrogate Model Training, not needing 1000s of STLs as a GNN/CNN would
- BO is a good match since meshing operations can be so expensive


<br/>

- Mediocre handling of geometric features importances
  - `min(flatness*Cf, sharpness*Cs, ...)`
  - Maybe a CNN on voxalized STLs is better?

::right::

<br/><br/>

- Graph Neural Networks (GNNs) as replacement for Stage 1
  as GNNs are better suited for learning spatial relationships in geometric data
- Running a simple potential flow through the mesh can reveal where refinement is needed... 
- Discontinuities not well modeled , assuming smooth meshing responses is not wise...
- Multi-scale geometries may require more than a single max-to-min cell size ratio
- Heavy bias towards the `cartesianMesh` configuration (eg. no boundary layers... etc)
