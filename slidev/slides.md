---
theme: default
fonts:
  sans: Fira Sans
  mono: Fira Mono
title: "Meshingo: A cell size recommender system"
titleTemplate: "%s"
author: Mohammed Elwardi Fadeli
keywords: meshing,cfd,bayesian-optimization,optimization,machine-learning,surrogate-model,cfmesh
info: |
  Leveraging bayesian-optimization algorithms to predict a good-enough cell size starting just from
  a (meshable) STL model. The optimization is performed on meshing-only OpenFOAM cases using foamBO
  framework and the trials use cfMesh meshing workflows to mesh the input STLs based on the settings
  chosen by the bayesian algorithm.
drawings:
  persist: false
transition: slide-left
mdc: true
exportFilename: meshingo
export:
  format: pdf
  timeout: 30000
  dark: false
  withClicks: false
  withToc: true
trueslash: false
lineNumbers: true
monaco: true
aspectRatio: 16/9

themeConfig:
  logo: "images/nhr-tu-logo.png"
  darkLogo: "images/nhr-tu-dark-logo.png"
  logoWidth: 180
  github: https://github.com/FoamScience
  footer: Bayesian Optimization for CFD meshing tasks
  date: Apr. 2025
seoMeta:
  ogImage: "https://foamscience.github.io/meshingo/images/thumbnail.png"
  ogUrl: "https://foamscience.github.io/meshingo"
download: https://foamscience.github.io/meshingo/meshingo.pdf"
addons:
  - slidev-addon-python-runner
  - slidev-addon-tikzjax
python:
  loadPackagesFromImports: true
  suppressDeprecationWarnings: true
  alwaysReload: false
  loadPyodideOptions: {}

class: text-center
---

# [Meshingo](https://github.com/FoamScience/meshingo): A cell size recommender system

Fully automatizing [cfMesh](https://cfmesh.com/cfmesh-open-source/) mesh generation...

---
transition: fade-out
layout: center
hideInToc: true
---

# Table of Content

<Toc maxDepth=3 />


---
src: 01-motivation.md
---

---
src: 02-opt-setup.md
---

---
src: 03-critic.md
---


---
layout: center
class: text-center
hideInToc: true
---

# Thank you for your attention

[GitHub](https://github.com/FoamScience/meshingo) · [More stuff like this](https://github.com/FoamScience)
