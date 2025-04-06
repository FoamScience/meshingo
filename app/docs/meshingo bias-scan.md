# meshingo bias-scan

Check if the stage 1 bayesian optimization produced a surrogate model that favorizes some parameters over the others.

| Attributes       | &nbsp;
|------------------|-------------
| Alias:           | bs

## Usage

```bash
meshingo bias-scan [OPTIONS]
```

## Examples

```bash
meshingo bias-scan --stage1-name Meshingo --threshold 0.1
```

## Options

#### *--stage1-name STAGE1-NAME*

Name for stage1 optimization problem

| Attributes      | &nbsp;
|-----------------|-------------
| Required:       | ✓ Yes

#### *--threshold THRESHOLD*

Maximal tolerable difference in feature importance for cell size objective

| Attributes      | &nbsp;
|-----------------|-------------
| Default Value:  | 0.05

#### *--ignore*

Don't fail even if the model is heavily biased


