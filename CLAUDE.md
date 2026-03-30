# CHIRPS-ML Coffee Yield Prediction — Lampung, Indonesia

## Project Overview
Research project: **Predicting Robusta coffee yield in Lampung using CHIRPS satellite precipitation data and Machine Learning**. Target: publication in Q1/Q2 international journal (Int. J. of Climatology, Remote Sensing MDPI, or Agricultural Water Management).

## Project Structure
```
.
├── CLAUDE.md                  # This file — project rules for Claude
├── CHIRPS_Lampung/
│   ├── PRD_Riset_CHIRPS_ML_Kopi_Lampung.md  # Full PRD
│   └── exercise/              # Earlier exercise/sample data
├── src/                       # Source code (modular Python scripts)
│   ├── data_collection/       # Scripts to download CHIRPS, ERA5, MODIS, BPS
│   ├── preprocessing/         # Cleaning, clipping, feature engineering
│   ├── modeling/              # ML model training & tuning
│   ├── evaluation/            # Metrics, SHAP, comparison
│   └── visualization/         # Maps, charts, figures for paper
├── data/
│   ├── raw/                   # Original unmodified downloads
│   ├── interim/               # Intermediate cleaned data
│   ├── processed/             # Final analysis-ready datasets
│   └── external/              # Third-party reference data (ENSO, IOD indices)
├── notebooks/                 # Jupyter notebooks for EDA & experiments
├── reports/
│   ├── figures/               # Publication-quality figures
│   └── tables/                # Result tables for paper
├── configs/                   # Model hyperparameters, paths, constants
├── tests/                     # Unit tests for data pipeline
└── docs/                      # Additional documentation
```

## Tech Stack
- **Language:** Python 3.10+
- **Data:** pandas, numpy, xarray, rioxarray
- **Geospatial:** rasterio, geopandas (install as needed)
- **ML:** scikit-learn, xgboost
- **Deep Learning (optional):** pytorch or tensorflow
- **Interpretability:** shap
- **Visualization:** matplotlib, seaborn
- **Notebook:** jupyter

## Coding Conventions

### Python Style
- Follow PEP 8. Use snake_case for functions/variables, PascalCase for classes.
- Type hints on all public function signatures.
- Docstrings: Google style, concise — one-liner for simple helpers.
- Max line length: 100 characters.

### Data Pipeline Rules
- **Never modify raw data.** Raw downloads go in `data/raw/`, processing outputs go in `data/interim/` or `data/processed/`.
- All data paths must be defined in `configs/paths.py` — never hardcode absolute paths in scripts.
- Every processing step must be reproducible: scripts read input → produce output, no manual steps.
- CSV files use UTF-8 encoding. GeoTIFF for raster data.

### ML Rules
- Always set `random_state=42` for reproducibility.
- Log all experiment parameters and results.
- Save trained models in `models/` with descriptive names including date and metric.
- Never train on test data. Test set (2021-2023) must remain untouched until final evaluation.

### Research Integrity
- Clearly distinguish between sample/synthetic data (in `exercise/`) and real data (in `data/`).
- All figures must include data source attribution.
- Report negative results honestly — if a model performs poorly, document why.
- Cite all data sources and methods properly.

## Key Commands
- `python -m src.data_collection.<module>` — Download specific datasets
- `python -m src.preprocessing.pipeline` — Run full preprocessing pipeline
- `python -m src.modeling.train` — Train models
- `python -m src.evaluation.compare` — Compare model results
- `pytest tests/` — Run tests

## Important Context
- **Study area:** Lampung Province, Indonesia (103.5°E–106.0°E, 3.5°S–6.0°S)
- **Period:** 2010–2023 (limited by BPS coffee production data availability)
- **Target variable:** Robusta coffee productivity (kg/ha) from BPS
- **Primary input:** CHIRPS v2.0 monthly precipitation
- **Key challenge:** Small dataset (~182 points = 13 kabupaten × 14 years). Use appropriate models (RF, XGBoost, SVR) and validation (Leave-One-Year-Out CV).
- **ENSO/IOD indices** are important predictors — Lampung is sensitive to both.

## What NOT to Do
- Do not install heavy packages (GDAL, cartopy) without asking first — check available alternatives.
- Do not download large global datasets without clipping to Lampung bbox first.
- Do not create notebooks for production code — notebooks are for EDA only, reusable code goes in `src/`.
- Do not commit data files to git — use .gitignore.
- Do not over-engineer; this is a research project, not production software.
