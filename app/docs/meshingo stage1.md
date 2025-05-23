# meshingo stage1

Run a 1st stage bayesian optimization, leveraging full runs of meshing tools to train a surrogate model. This will take some time

| Attributes       | &nbsp;
|------------------|-------------
| Alias:           | s1, train

## Usage

```bash
meshingo stage1 TRAINING_STLS [OPTIONS]
```

## Examples

```bash
meshingo train --stage1-name Meshingo --n-trials 300 training_dataset/
```

## Environment Variables

#### *STAGE1_MAX_OCTREES*

Maximal allowed number of Octree levels generated by cfMesh tools.

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 9

## Arguments

#### *TRAINING_STLS*

Path to a folder with STL models used for the 1st optimization run

| Attributes      | &nbsp;
|-----------------|-------------
| Required:       | ✓ Yes

## Options

#### *--stage1-name STAGE1-NAME*

Name for stage1 optimization problem

| Attributes      | &nbsp;
|-----------------|-------------
| Required:       | ✓ Yes

#### *--n-parallel-trials N-PARALLEL-TRIALS*

Number of parallel trials for stage1 optimization run

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 2

#### *--n-trials N-TRIALS*

Max total number of trials to run in stage 1 optimization

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 300

#### *--stopping-improvement STOPPING-IMPROVEMENT*

Improvement bar for early stopping the stage 1 optimization

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 1e-3

#### *--trial-ttl TRIAL-TTL*

Trial Time-To-Live in seconds

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 3000


