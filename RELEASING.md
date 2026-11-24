# Releasing

The rules are the shared standard's
[releasing](docs/conventions/standard/releasing.md) and
[versioning](docs/conventions/standard/versioning.md): a release is a pull request
titled `chore(release): prepare X.Y.Z`, and the synced `release.yml` tags and
releases its squash commit when it merges. Never push or move a tag by hand.

This repository's specifics:

- `__version__` lives in `src/laminate_constitutive_model/__init__.py`;
  `pyproject.toml` reads it from there.
- The release PR moves the `## [Unreleased]` notes in `CHANGELOG.md` under
  `## [X.Y.Z] - YYYY-MM-DD`.
- The tag `v0.3.0` was made while `__version__` still said 0.2.0, and the
  changelog has no 0.3.0 section. `main` now carries 0.4.0, the next release;
  its changelog section notes what 0.3.0 contained.
- shell-fem and anisotropic-section-model pin this package by tag, so release here
  before them when they need a change.
- PyPI: `pypi: false` in `.github/repo.yml`. To publish, add a PyPI trusted
  publisher for `laminate-constitutive-model` (workflow `release.yml`,
  environment `pypi`), create the `pypi` environment in the repository settings,
  and set `pypi: true`.
