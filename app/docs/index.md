# meshingo

A cell-size recommendation system for CFD meshes;  
  
**Idea**:  
  
From an STL file describing the (water-tight) flow domain, guess a "good-enough" minimal cell size (to be used at feature-edges) and a ratio between smallest and biggest cell size in the mesh. These parameters can then be used to mesh the surface STLs in an **unattended way**.  
  
This naturally seemed like a ML task, and to save on the number of meshing operations needed, Bayesian Optimization is used to "train" a surrogate model, then fine-tune it on the target STL model.  
  
The surrogate model is tuned into the following directions (these are hard-coded):  
1. Favorizing bigger cell sizes to produce meshes that are as coarse as possible while detecting all important surface features. This is enforced by applying a decay function to cell-size objective functions.  
1. Producing Hex-based meshing, using [(open-source version of) cfMesh's](https://cfmesh.com/cfmesh-open-source/) `cartesianMesh`. The tool's workflow is already pretty automated, and all it needs is a small nudge towards good cell sizes.  
  
The tuning stage can be configured into the following directions:  
1. Favorizing meshes needing less than `STAGE1_MAX_OCTREES` levels of refinement in order to control RAM usage during training. By default, fast meshing operations requiring less than 16GB of RAM are promoted.  
1. Controlling Bias towards features of the training dataset, through the distributions of STL geometric features.  
  
&gt; [!IMPORTANT]  
&gt; Experimental at best, still figuring out the best objective functions, parameters to consider, and STL model types to train on.  


| Attributes       | &nbsp;
|------------------|-------------
| Version:         | 0.1.0

## Usage

```bash
meshingo COMMAND
```

## Dependencies

#### *git*

install git through your package manager

#### *uv*

install by running $(curl -LsSf https://astral.sh/uv/install.sh | sh)

#### *cartesianMesh*

source etc/bashrc from an OpenFOAM installation with cfMesh compiled

#### *surfaceCheck*

source etc/bashrc from an OpenFOAM installation

## Commands

- [install](meshingo%20install) - Install Python dependencies, assuming you have uv
- [stage1](meshingo%20stage1) - Run a 1st stage bayesian optimization, leveraging full runs of meshing tools to train a surrogate model. This will take some time
- [validate](meshingo%20validate) - Infer settings from a saved surrogate model, and run corresponding meshing case.
- [bias-scan](meshingo%20bias-scan) - Check if the stage 1 bayesian optimization produced a surrogate model that favorizes some parameters over the others.
- [stage2](meshingo%20stage2) - Fine-tune surrogate model from stage 1 on target STL, and reach a verdict for the top three (3) "good-enough" cell sizes.


