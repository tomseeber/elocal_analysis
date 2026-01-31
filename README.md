# elocal_analysis

This repository was scaffolded following the cookiecutter-data-science layout (https://cookiecutter-data-science.drivendata.org/).

## Structure

- `data/` — data (raw/interim/processed/external) (gitignored)
- `notebooks/` — Jupyter notebooks
- `src/elocal_analysis/` — source code as a Python package
- `models/` — trained and serialized models
- `reports/` — generated analysis and figures
- `tests/` — unit and integration tests

## Quickstart

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
make test
# or
pytest -q
```
