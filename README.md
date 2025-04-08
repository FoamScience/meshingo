# Meshingo: A mesh size recommender system

> For a quick presentation of current state, look at
> [this presentation](https://foamscience.github.io/meshingo)

This is basically **an experimental** "unconventional" recommender system for minimum mesh cell
sizes that would result in a good balance between **full geometrical feature capturing**
and **minimal total mesh cell count**.

A few notes before getting started:
- The recommender system is **biased towards producing meshes with bigger cell sizes** on purpose
- There are measures in place to prevent over-fitting on the training dataset
  but this is difficult to guarantee; it's important to always add validation trials, which is
  skipped for now.
- The recommender system is fine-tuned for less-than-one-hour meshing operations which
  are carried out through [cfMesh] and that can be performed on a laptop.

## Try it immediately within an Apptainer container

```bash
apptainer pull meshingo.sif oras://ghcr.io/foamscience/meshingo:0.0.1
apptainer run meshingo.sif info # to see where things are, and what is available
git clone https://github.com/FoamScience/meshingo/
cd meshingo
cp <your-stl-file> testing_dataset
# Use the surrogate that is shipped with the container to get a few case configurations
apptainer run meshingo.sif 'meshingo validate
          --model /opt/surrogates/Meshingo
          --training-set /opt/surrogates/geometric_features.csv
          testing_dataset/<your-stl-file>'
# Inspect the respective meshDict files to minimal/maximal cell sizes
foamDictionary -expand <case_path>/system/meshDict
apptainer run meshingi.sif 'meshingo --help' # for more stuff to do
```

## First steps

The following command will install the Python package shipped within this repository
into a [uv]-managed virtual environment. It will also prompt you to install any other missing 
dependencies:
```bash
./app/meshingo install
```

## Concept and Principles

The recommender system works in two stages:
1. Surrogate model "training", performed only once
1. Surrogate model "tuning" on target surface STL, performed on each target surface STL

### Surrogate model training

The surrogate model is typically a Gaussian Process trained by a Bayesian Algorithm.
[foamBO] is used to automatize the selection of acquisition functions and even the Bayesian
Algorithm, based on the optimization parameters and objectives.

1. Prepare a bunch of (meshable) surface STLs and put them into `training_dataset` folder. Random
   surfaces for industrial parts that you can get from all over the internet will do...
1. Run 
   ```bash
    export STAGE1_MAX_OCTREES=9 # Optional, default is 9, more means more RAM usage
    ./app/meshingo train --stage1-name Meshingo training_dataset
   ```
   - These STL files will be processed to produce a `training_dataset/geometric_features.csv`
     with computed geometric features for each surface STL:
     - flatness
     - surface-to-volume ratio
     - min, mean and max curvature
     - minimal feature-capturing edge length: This is calculated by piercing the STL with
       rays from a surrounding sphere and calculating the minimal intersection distances.
     - sharpness
   > [!NOTE]
   > It might be a good idea at this point to load the CSV into a Pandas database and check
   > the distribution of the different geometric features! These distributions will contribute
   > to the model's bias.
   - Then a Bayesian Optimization run will start.
   - Trials are setup to run locally and will be stored in `trials/` folder for reference
   - This first optimization run has essentially two sets of parameters:
     1. The geometric features (flatness, max-curvature, ..., etc). The "most-similar" surface STL in the
        training dataset will be used for the actual meshing operations.
     1. Coefficients for these geometric features (flatness coeff, max-curvature coeff, ..., etc)
        that weigh the geometrical features when deciding on a mesh cell size.
     1. In addition to these sets of parameters, there is also a parameter of the ratio of max/min cell size,
        as well as a coefficient for minimal feature-capturing edge length. 

Detailed settings for the optimization run can be found in [`stage1/stage_1.yaml`](stage1/stage_1.yaml)
although the `meshingo stage1` command interfaces the most-commonly modified ones.

Once the training is done, it is recommended to run the following to see if the set of geometric features
is homogeneous in terms of "feature importance" to the cell size objective (differences within 5% in this case):
```bash
./app/meshingo bias-scan --stage1-name Meshingo --threshold 0.05
```

### Surrogate model tuning on target STL file

The following command will start the tuning stage
```bash
./app/meshingo stage2 --stage1-name Meshingo --stage2-name MY_TARGET <path_to_STL>
```

Detailed settings for the tuning optimization can be found [in `stage2/stage_2.yaml`](stage2/stage_2.yaml)
although the `meshingo stage2` command interfaces the most-commonly modified ones.

Essentially, instead of using a training set of surface STLs, the geometric features are
fixed, and inferred from the target STL. The optimizer then using the surrogate model
from the previous stage to optimize the previous objectives **and their confidence intervals**
(that the surrogate model provides) on the coefficients set of parameters from stage 1.

The verdict is then given in JSON format (`stage2/verdict.json`) containing the top 3
pareto-frontier points from stage 2 optimization which are associated with the highest
confidence.


[cfMesh]: https://cfmesh.com/cfmesh-open-source/
[foamBO]: https://github.com/FoamScience/OpenFOAM-Multi-Objective-Optimization
[uv]: https://github.com/astral-sh/uv
