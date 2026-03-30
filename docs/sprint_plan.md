# Sprint Plan
## CHIRPS-ML Coffee Yield Prediction — Lampung, Indonesia

*6 sprints × 2 weeks = ~3 months active work + 2 months writing/revision*
*Target submission: September 2026*

---

## Sprint 0 — Setup & Literature (Week 1-2 / Apr 1-13, 2026)
**Goal:** Solid foundation before touching data

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 0.1 | Deep literature review — CHIRPS validation studies in Southeast Asia | `docs/litrev_chirps_validation.md` (annotated summary of 10-15 papers) | RQ1 |
| 0.2 | Deep literature review — ML crop yield prediction | `docs/litrev_ml_yield.md` (annotated summary of 10-15 papers) | RQ3 |
| 0.3 | Deep literature review — coffee & climate in Indonesia | `docs/litrev_coffee_climate.md` (annotated summary of 8-10 papers) | RQ2 |
| 0.4 | Fetch & verify all BibTeX entries via CrossRef | `docs/references.bib` (~30-40 entries) | All |
| 0.5 | Register accounts: Copernicus CDS, NASA Earthdata | Access credentials ready | — |
| 0.6 | Draft institutional letter for BMKG data request | Letter sent | RQ1 |

**Exit criteria:** Literature review complete, all accounts registered, BMKG request submitted

---

## Sprint 1 — Data Collection (Week 3-4 / Apr 14-27, 2026)
**Goal:** All datasets downloaded and inventoried

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 1.1 | Download CHIRPS v2.0 monthly (1981-2025), clip to Lampung | `data/raw/chirps/` | RQ1,2,3 |
| 1.2 | Download ERA5 monthly (2010-2025) for Lampung bbox | `data/raw/era5/` | RQ2,3 |
| 1.3 | Download MODIS NDVI MOD13A3 (2010-2025) for Lampung | `data/raw/modis/` | RQ3 |
| 1.4 | Collect BPS coffee production data (2010-2023) per kabupaten | `data/raw/bps/` | RQ2,3,4 |
| 1.5 | Download ENSO Nino 3.4 & IOD DMI indices | `data/external/` | RQ2 |
| 1.6 | Download DEM SRTM/DEMNAS for Lampung | `data/raw/dem/` | RQ3 |
| 1.7 | Collect BMKG station data (if received) | `data/raw/bmkg/` | RQ1 |
| 1.8 | Run `/data-check` — verify completeness | Data inventory report | All |

**Exit criteria:** All downloadable data acquired, metadata files created, `/data-check` shows ≥80% complete

---

## Sprint 2 — Preprocessing & Validation (Week 5-6 / Apr 28 - May 11, 2026)
**Goal:** Clean data + CHIRPS validated → answers RQ1

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 2.1 | Build preprocessing pipeline (`src/preprocessing/`) | Reproducible pipeline script | All |
| 2.2 | Extract CHIRPS time series for BMKG station locations | `data/interim/chirps_at_stations.csv` | RQ1 |
| 2.3 | **CHIRPS validation vs BMKG** — correlation, bias, RMSE, POD, FAR | Validation metrics table + scatter plots | **RQ1** |
| 2.4 | Spatial bias map of CHIRPS over Lampung | `reports/figures/fig1_chirps_validation.png` | **RQ1** |
| 2.5 | Compute SPI-3, SPI-6, SPI-12 from CHIRPS (baseline 1981-2023) | `data/interim/spi_lampung.csv` | RQ2 |
| 2.6 | Aggregate CHIRPS to kabupaten-level seasonal features | `data/interim/chirps_features.csv` | RQ2,3 |
| 2.7 | Extract ERA5 features per kabupaten | `data/interim/era5_features.csv` | RQ3 |
| 2.8 | Extract MODIS NDVI/EVI per kabupaten | `data/interim/modis_features.csv` | RQ3 |
| 2.9 | Merge all features + BPS target into analysis dataset | `data/processed/analysis_dataset.csv` | All |
| 2.10 | Write Results Section 4.1 (CHIRPS Validation) | Paper draft section | RQ1 |

**Exit criteria:** RQ1 answered (H1 tested), analysis dataset ready, no missing values unexplained

---

## Sprint 3 — EDA & Feature Analysis (Week 7-8 / May 12-25, 2026)
**Goal:** Understand climate-yield relationships → answers RQ2

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 3.1 | EDA notebook: distributions, trends, seasonality | `notebooks/01_eda.ipynb` | RQ2 |
| 3.2 | Correlation analysis: all features vs productivity | Correlation matrix heatmap | **RQ2** |
| 3.3 | Time series analysis: productivity vs SPI per kabupaten | Time series overlay plots | **RQ2a,b** |
| 3.4 | ENSO composite analysis: productivity in El Nino vs La Nina vs Neutral years | Composite bar chart | **RQ2c** |
| 3.5 | IOD composite analysis | Composite analysis | **RQ2c** |
| 3.6 | Identify collinear features, decide on feature selection strategy | Feature selection report | RQ3 |
| 3.7 | Write Results Section 4.2 (Climate-Yield Relationships) | Paper draft section | RQ2 |

**Exit criteria:** RQ2 answered (H2, H3 tested), key climate drivers identified, feature set finalized

---

## Sprint 4 — Modeling & Evaluation (Week 9-10 / May 26 - Jun 8, 2026)
**Goal:** Best model identified → answers RQ3

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 4.1 | Implement training pipeline (`src/modeling/train.py`) | Training script | RQ3 |
| 4.2 | Train baseline: Linear Regression | `/experiment-log log` | RQ3 |
| 4.3 | Train & tune: Random Forest (Leave-One-Year-Out CV) | `/experiment-log log` | **RQ3a** |
| 4.4 | Train & tune: XGBoost (Leave-One-Year-Out CV) | `/experiment-log log` | **RQ3a** |
| 4.5 | Train & tune: SVR (Leave-One-Year-Out CV) | `/experiment-log log` | **RQ3a** |
| 4.6 | **Ablation study**: CHIRPS-only → +ERA5 → +MODIS → +indices → full | Ablation table | **RQ3b** |
| 4.7 | **Parsimony analysis**: feature elimination curve | Minimum feature set | **RQ3c** |
| 4.8 | Final evaluation on test set (2021-2023) — ONE TIME ONLY | Test set metrics | **RQ3** |
| 4.9 | SHAP analysis on best model | SHAP summary + dependence plots | RQ2, RQ3 |
| 4.10 | `/experiment-log compare` — final model comparison | Comparison report | RQ3 |
| 4.11 | Write Results Section 4.3 (Model Performance) | Paper draft section | RQ3 |

**Exit criteria:** RQ3 answered (H4, H5 tested), best model selected, SHAP analysis complete

---

## Sprint 5 — Early Warning & Paper Writing (Week 11-14 / Jun 9 - Jul 6, 2026)
**Goal:** Answer RQ4 + complete first draft

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 5.1 | Lead-time analysis: predict with data up to Jun/Jul/Aug/Sep | Lead-time skill plot | **RQ4a** |
| 5.2 | Binary classification: above/below average productivity | Confusion matrix, sensitivity, specificity | **RQ4b** |
| 5.3 | Early warning framework diagram | Framework figure | **RQ4** |
| 5.4 | Write Results Section 4.4 (Early Warning) | Paper draft section | RQ4 |
| 5.5 | Write Introduction (with all references) | Paper draft section | All |
| 5.6 | Write Study Area & Data section | Paper draft section | All |
| 5.7 | Write Methodology section | Paper draft section | All |
| 5.8 | Write Discussion section | Paper draft section | All |
| 5.9 | Write Conclusion | Paper draft section | All |
| 5.10 | Write Abstract (LAST) | Paper draft section | All |
| 5.11 | Generate all publication-quality figures | `reports/figures/` (8-12 figures) | All |
| 5.12 | Compile all tables | `reports/tables/` (4-6 tables) | All |

**Exit criteria:** Complete first draft, all figures and tables generated, RQ4 answered (H6 tested)

---

## Sprint 6 — Review & Submission (Week 15-18 / Jul 7 - Aug 3, 2026)
**Goal:** Polished paper ready for submission

| # | Task | Deliverable | RQ |
|---|------|------------|-----|
| 6.1 | Self-review: use `/paper-draft review <section>` for each section | Revision notes | All |
| 6.2 | Check all references verified via CrossRef | Clean `references.bib` | All |
| 6.3 | Verify reproducibility: re-run full pipeline from scratch | Pipeline passes | All |
| 6.4 | Internal review by co-author(s) / advisor | Feedback incorporated | All |
| 6.5 | Language editing / proofreading | Polished manuscript | All |
| 6.6 | Format to target journal template | Formatted manuscript | All |
| 6.7 | Prepare supplementary materials (code, data description) | Supplementary files | All |
| 6.8 | Write cover letter | Cover letter | All |
| 6.9 | Submit to journal | Confirmation email | All |
| 6.10 | Upload code to GitHub + dataset to Zenodo | Public repository | All |

**Exit criteria:** Paper submitted, code/data publicly available

---

## Sprint Summary

| Sprint | Weeks | Focus | RQ Answered | Key Milestone |
|--------|-------|-------|-------------|--------------|
| **0** | 1-2 | Literature & Setup | — | Foundation ready |
| **1** | 3-4 | Data Collection | — | All data acquired |
| **2** | 5-6 | Preprocessing & Validation | **RQ1** | CHIRPS validated |
| **3** | 7-8 | EDA & Feature Analysis | **RQ2** | Climate drivers identified |
| **4** | 9-10 | Modeling & Evaluation | **RQ3** | Best model selected |
| **5** | 11-14 | Early Warning & Writing | **RQ4** | First draft complete |
| **6** | 15-18 | Review & Submission | — | Paper submitted |

---

## Risk Checkpoints

| After Sprint | Check | Action if Failed |
|-------------|-------|-----------------|
| Sprint 1 | BMKG data received? | Proceed without; use CHIRPS-only validation with spatial consistency check; cite prior Lampung validation studies |
| Sprint 2 | H1 accepted (CHIRPS r > 0.7)? | If r < 0.5, consider bias correction step; if still poor, pivot scope to "CHIRPS evaluation" paper |
| Sprint 3 | H2/H3 — clear climate-yield signal? | If no signal, add more features (soil, land use); expand to multi-province; discuss limitations honestly |
| Sprint 4 | H4 — R² > 0.75? | If R² < 0.5, pivot to classification (above/below average) instead of regression; still publishable |
| Sprint 5 | First draft coherent? | Extend timeline by 2 weeks; seek co-author help for weak sections |

---

*This plan is a living document. Update sprint status and adjust timelines as needed.*
*Last updated: 2026-03-30*
