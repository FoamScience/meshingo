# meshingo stage2

Fine-tune surrogate model from stage 1 on target STL, and reach a verdict for the top three (3) "good-enough" cell sizes.

| Attributes       | &nbsp;
|------------------|-------------
| Alias:           | s2, predict

## Usage

```bash
meshingo stage2 TARGET_STL [OPTIONS]
```

## Examples

```bash
meshingo predict --stage1-name Meshingo --stage2-name Test testing_dataset/model.stl
```

## Arguments

#### *TARGET_STL*

Path to the target STL to guess the cell size for

| Attributes      | &nbsp;
|-----------------|-------------
| Required:       | ✓ Yes

## Options

#### *--stage1-name STAGE1-NAME*

Name for stage1 optimization problem

| Attributes      | &nbsp;
|-----------------|-------------
| Required:       | ✓ Yes

#### *--stage2-name STAGE2-NAME*

Name for stage2 optimization problem

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


