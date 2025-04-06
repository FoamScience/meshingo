---
theme: default
fonts:
  sans: Fira Sans
  mono: Fira Mono
title: "Meshingo: A cell size recommender system"
author: Mohammed Elwardi Fadeli
keywords: meshing,cfd,bayesian-optimization,optimization,machine-learning,surrogate-model,cfmesh
info: false
class: text-center
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
  logo: "/images/nhr-tu-logo.png"
  darkLogo: "/images/nhr-tu-dark-logo.png"
  logoWidth: 180
  github: https://github.com/FoamScience
  footer: Bayesian Optimization for CFD meshing tasks
  date: Apr. 2025
# open graph
# seoMeta:
#  ogImage: https://cover.sli.dev
addons:
  - slidev-addon-python-runner
  - slidev-addon-tikzjax
python:
  installs: ["cowsay"]
  prelude: |
    GREETING_FROM_PRELUDE = "Hello, Slidev!"
  loadPackagesFromImports: true
  suppressDeprecationWarnings: true
  alwaysReload: false
  loadPyodideOptions: {}
---

# [Meshingo](https://github.com/FoamScience/meshingo): A cell size recommender system

Fully automatizing [cfMesh](https://cfmesh.com/cfmesh-open-source/) mesh generation...

---
transition: fade-out
layout: center
hideInToc: true
---

# Table of Content

<Toc maxDepth="3" />


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
