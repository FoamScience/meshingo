---
layout: adr
title: Meshingo CLI
related:
    - Use of a 2-Stage Bayesian Optimization Framework
    - Meshing Tool Selection for Stage 1
status: enforced
date: 2025-03-18
decision_makers:
    - elwardi
adr_tags:
  - backend
  - cli
  - automation
---

## Context and Problem Statement

A clean, user-friendly command-line interface (CLI) is needed to facilitate and automate the
BO workflow starting from having a target STL ending with getting a suitable cell size value.

The CLI should allow for easy installation of dependencies, management of STL files,
training of surrogate models, validation, and fine-tuning of the optimization process,
all while keeping all steps efficient and reproducible.

What CLI solution should we use to streamline and automate the meshing and optimization tasks?

## Decision Drivers

- Need for a simple, easy-to-use interface for users to interact with
  the complex meshing and optimization system.
- Attempt to bury some of the implementation details
  (eg. How `foamBO` is configured for each stage)
- Must support all critical steps in the workflow, including installation,
  data preparation, training, validation, and fine-tuning.
- Automation should be flexible and extendable to accommodate future
  workflows and model updates.

## Considered Options

- **Bashly Framework**  
  A framework to build robust command-line interfaces in Bash with simple syntax and support
  for argument parsing, subcommands, and user-friendly error handling.

- **Python CLI Frameworks (e.g., Click, argparse)**  
  Using Python-based CLI frameworks, which could offer more features but add complexity and dependencies.

## Decision Outcome

Chosen option: **Bashly** mainly, a tool for building CLI applications in Bash.
It creates simple, intuitive, and automated CLI sections matching workflows for meshing, training,
validation, and fine-tuning, with minimal overhead and dependencies.

Python CLI frameworks are still used for higher-level access to implementation details.

### Consequences

- **Positive**: 
  - Provides a simple, fast CLI that can easily be invoked in any shell environment, streamlining the user experience.
  - Automation of critical steps with minimal configuration, ensuring a smooth workflow.
  - Easy to extend in the future with new subcommands or features without significant overhead.
  
- **Neutral**: 
  - Bashly, being Bash-based, is fast and integrates well into CI/CD pipelines or development
    workflows, but lacks the rich feature set of pretty CLI tools.
  
- **Negative**: 
  - More limited compared to Python alternatives in terms of advanced functionality,
    but the need of advanced functionality is currently not expected.

### Confirmation

Compliance is confirmed by:
- An implementation of a clean CLI using Bashly in the `app` folder.
- Ensuring all steps can be executed without misconfiguration.

## More information

The separation of steps allows for more flexible surrogate-model usage but has
the side of effect of mixing up surrogate models and the data used to train them since
no versioning (of the CSV files) is implemented yet.
