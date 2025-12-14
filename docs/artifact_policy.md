# Artifact policy

## Tracked (committed)
- Source code (`src/`, `scripts/`)
- Documentation (`README.md`, `docs/`, `PROGRESS_LOG.md`)
- Paper TeX (`paper/*.tex`)
- Small, canonical run artifacts only when explicitly declared canonical.

## Not tracked by default
- `data/processed/` (run outputs)
- `figures/runs/`, `figures/latest/`
- LaTeX build outputs (`paper/**/*.pdf`, `.aux`, `.log`, etc.)

## Exceptions (canonical runs)
When we declare a run canonical, we may commit:
- `data/processed/runs/<run_id>/results.csv`
- `data/processed/runs/<run_id>/run_meta.json`
- `figures/runs/<run_id>/*.png`

But default is: keep the repo light unless a result paper-levelis 
