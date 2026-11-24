# Contributing

The rules are in [AGENTS.md](AGENTS.md) and the shared standard in
[docs/conventions/standard/](docs/conventions/standard/README.md): work through a
pull request with a Conventional Commit title, one concern per pull request, and a
`CHANGELOG.md` line under `## [Unreleased]` ending with the PR number.

## Checks

CI runs the same checks (`tests.yml`):

```bash
pip install -e ".[dev]"     
pip install -r requirements/lint.txt
ruff check .                    # lint (pinned ruff)
pytest -q                       # the test suite
python examples/run_all.py      # every example, with its figures
python -m build                 # sdist and wheel
python -m twine check --strict dist/*
```

Commit regenerated example figures only when the example's subject changed.
