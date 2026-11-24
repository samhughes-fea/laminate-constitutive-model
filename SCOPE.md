# Scope

`laminate-constitutive-model` is the constitutive behaviour of composite plies
and laminates, on its own.

## In scope

- Orthotropic materials (2D and 3D), material cards and the material library,
  temperature-dependent and hygrothermal properties.
- Plies and laminates: Q, Q̄, stiffness invariants, ABD and offsets.
- Section stiffness of the through-thickness theories (CLPT, FSDT, refined
  zig-zag, layerwise) as generalised section matrices.
- Ply stress and strain recovery, failure criteria and array exposures.
- Exact elasticity solutions used as benchmarks (Pagano's plate).

## Out of scope

| Topic | Where it belongs |
| --- | --- |
| Blade and section geometry | [implicit-geometry-kernel](https://github.com/samhughes-fea/implicit-geometry-kernel) |
| Shell and solid finite elements, meshing | [shell-fem](https://github.com/samhughes-fea/shell-fem) |
| Cross-section stiffness of a whole section | [anisotropic-section-model](https://github.com/samhughes-fea/anisotropic-section-model) |
| Beam solvers | [1d-fem](https://github.com/samhughes-fea/1d-fem) |

A feature that needs geometry, a mesh or a solver belongs downstream.
