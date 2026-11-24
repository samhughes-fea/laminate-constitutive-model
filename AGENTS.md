<!-- guidelines:start (shared development standard 0.1.1; edit it there, not here) -->
## Shared rules

These rules hold in every tool repository; the full standard is in
[docs/conventions/standard/](docs/conventions/standard/README.md). The rules
under "Hard rules" below this block are this repository's own.

1. **Read before changing.** This file, `SCOPE.md`, then the plan doc named in
   `.github/repo.yml`.
2. **Work through pull requests.** `main` is protected. One concern per pull
   request; the title is a Conventional Commit
   ([commits](docs/conventions/standard/commits.md)) and becomes the squash commit.
3. **Keep the plan doc current** in the same pull request as the work.
4. **No private data.** Never commit confidential inputs or name a private
   project ([data and security](docs/conventions/standard/data-and-security.md)).
5. **Generic source.** `src/` and `tests/` never name or special-case a
   downstream project.
6. **Deprecate before removing** ([API stability](docs/conventions/standard/api-stability.md)).
7. **Golden numbers move only on purpose**, with the `golden-change` label and
   the reason in the changelog.
8. **Never remove `needs-decision`**; record a lasting decision in `docs/decisions/`.
9. **Releases follow the workflow.** Prepare the release pull request; never push
   or move a tag ([releasing](docs/conventions/standard/releasing.md)).
10. **Label everything**: one type, its areas, any flag
    ([labels](docs/conventions/standard/labels.md)).
11. **Example figures are committed** and embedded in the example README; commit a
    regenerated PNG only when the example's subject changed.
12. **Re-run only what failed** while fixing a failing check.
<!-- guidelines:end -->

Read this before changing the repository. It applies to people and to coding
agents alike. [SCOPE.md](SCOPE.md) says what belongs here;
[CONTRIBUTING.md](CONTRIBUTING.md) lists the checks.

## Hard rules

These are this repository's own rules, numbered on from the shared ones above.

13. **NumPy only.** `src/` depends on NumPy (and the standard library) alone: no
    geometry, mesh, solver or plotting import. `tests/test_import_boundary.py`
    checks every import, including ones inside functions.
14. **Imports point down.** Nothing here imports the geometry kernel, shell-fem,
    anisotropic-section-model or 1d-fem; they build on this package.
15. **The old import name** `composite_laminate_model` only re-exports the public
    API with a `DeprecationWarning`; never add code to it.
16. **Release before the consumers.** shell-fem and anisotropic-section-model pin
    this package by tag, so a change they need is released here first
    ([RELEASING.md](RELEASING.md)).

## Working conventions

- Commit scopes and `area:` labels are in [.github/repo.yml](.github/repo.yml) and
  [.github/labels.yml](.github/labels.yml).
- Run the checks in [CONTRIBUTING.md](CONTRIBUTING.md) before pushing.
- New failure criteria register through the criteria registry and come with a
  published reference case in `tests/`.
