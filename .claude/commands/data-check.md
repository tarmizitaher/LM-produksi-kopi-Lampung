# Data Inventory Check

Audit the current state of all datasets in the project.

## Instructions
1. Scan `data/raw/`, `data/interim/`, `data/processed/`, and `data/external/` directories
2. For each file found, report:
   - Filename, size, last modified date
   - Data type (CSV, GeoTIFF, NetCDF, etc.)
   - Row/column count (for tabular data)
   - Spatial extent and resolution (for raster data)
3. Cross-reference with the data requirements in `CHIRPS_Lampung/PRD_Riset_CHIRPS_ML_Kopi_Lampung.md` Section 6
4. Report which datasets are:
   - ✅ Available and ready
   - ⚠️ Available but needs preprocessing
   - ❌ Missing — not yet downloaded
5. Suggest next steps for missing data

## Output Format
Produce a markdown table summarizing data status.
