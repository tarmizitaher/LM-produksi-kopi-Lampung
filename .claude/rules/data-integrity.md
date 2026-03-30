# Data Integrity & Reproducibility Rules

## Raw Data is Sacred
- **NEVER** modify files in `data/raw/`. Raw data must remain exactly as downloaded.
- All transformations produce new files in `data/interim/` or `data/processed/`.
- If raw data has errors, document them — do not silently fix.

## Provenance Tracking
Every dataset in `data/raw/` must have a companion metadata file (`*_metadata.json`) recording:
```json
{
  "source": "CHC UCSB",
  "url": "https://data.chc.ucsb.edu/products/CHIRPS-2.0/...",
  "download_date": "2026-04-15",
  "description": "CHIRPS v2.0 monthly precipitation, Lampung bbox",
  "spatial_extent": {"west": 103.5, "south": -6.0, "east": 106.0, "north": -3.5},
  "temporal_extent": {"start": "1981-01", "end": "2025-12"},
  "format": "GeoTIFF",
  "license": "Public domain"
}
```

## Reproducibility
- All processing steps must be scripted — no manual Excel/spreadsheet steps
- Every script must be runnable end-to-end: `python -m src.preprocessing.pipeline`
- Random seed: always `random_state=42` (defined in `configs/paths.py`)
- Pin library versions in `requirements.txt` when finalizing results
- Document any manual data acquisition steps (e.g., BMKG surat request) in `docs/data_acquisition_log.md`

## Data Validation Checks
Before any analysis, verify:
- No unexpected NaN/null values (or document why they exist)
- Value ranges are physically plausible (e.g., precipitation >= 0, NDVI between -1 and 1)
- Temporal continuity — no missing months without explanation
- Spatial completeness — all kabupaten present for all years
- Units are consistent across all sources

## Train/Test Separation
- **Test set (2021-2023) must NEVER be used during model development**
- No feature engineering decisions based on test set patterns
- No hyperparameter tuning using test set performance
- Test set is used exactly once: for final model evaluation
- Document this clearly in the paper methodology section

## Sensitive Data
- BMKG station-level data may have usage restrictions — check terms
- Do not commit raw BMKG data to public GitHub repos without permission
- BPS data is public but cite the source properly
