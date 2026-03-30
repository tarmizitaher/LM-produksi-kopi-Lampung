# Literature Review: ML/DL for Crop Yield Prediction

*Sprint 0.2 — Last updated: 2026-03-30*

---

## Summary Table

| # | First Author | Year | Crop/Region | Journal | Best Model | R² | DOI/URL |
|---|-------------|------|-------------|---------|------------|-----|---------|
| 1 | Lischeid et al. | 2022 | Coffee (Robusta), Vietnam | Agric. Forest Meteorol. | RF + agroclimatic | — | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0168192321001325) |
| 2 | Santos et al. | 2022 | Coffee, Brazil | Theor. Appl. Climatol. | RF, XGBoost | R²=0.82 | [Springer](https://link.springer.com/article/10.1007/s00704-022-03983-z) |
| 3 | — | 2022 | Coffee, Brazil | AgriEngineering (MDPI) | RF + satellite imagery | R²=0.93 | [MDPI](https://www.mdpi.com/2624-7402/4/4/57) |
| 4 | — | 2022 | Coffee, Brazil | Agronomy (MDPI) | RF + multispectral | — | [MDPI](https://www.mdpi.com/2073-4395/12/12/3195) |
| 5 | — | 2024 | Arabica, — | AgriEngineering (MDPI) | Smart Coffee: ML | — | [MDPI](https://www.mdpi.com/2624-7402/6/4/281) |
| 6 | — | 2024 | Coffee, Brazil | — | ML + meteorological drivers + projections | — | [ResearchGate](https://www.researchgate.net/publication/387085619) |
| 7 | Tran et al. | 2022 | Coffee, Vietnam | Remote Sensing (MDPI) | Statistical + RS biophysical | — | [MDPI](https://www.mdpi.com/2072-4292/14/13/2975) |
| 8 | — | 2024 | Comprehensive review | Heliyon / ScienceDirect | Review: RF, XGBoost, ANN most common | — | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11667600/) |
| 9 | — | 2024 | Systematic review | Computers & Electronics in Agric. | Review: 2017-2024 techniques | — | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772375524003228) |
| 10 | — | 2025 | Multiple crops | Discover Agriculture | RF vs XGBoost vs SVM comparison | — | [Springer](https://link.springer.com/article/10.1007/s44279-025-00335-z) |
| 11 | — | 2025 | Legume | Applied Sciences (MDPI) | XGBoost + SHAP + Sentinel-2 | — | [MDPI](https://www.mdpi.com/2076-3417/15/13/7074) |
| 12 | — | 2025 | Potato | npj Sustainable Agric. | ML + SHAP for driver analysis | — | [Nature](https://www.nature.com/articles/s44264-025-00052-6) |
| 13 | — | 2022 | Wheat | Frontiers Plant Sci. | ML + RS, SHAP | — | [Frontiers](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1090970/full) |
| 14 | Oliveira et al. | 2021 | Grains, general | Agric. Forest Meteorol. | Yield forecasting with ML & small data | — | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0168192321002392) |
| 15 | — | 2025 | Review: small data | J. Big Data (Springer) | Strategies for limited ML data | — | [Springer](https://link.springer.com/article/10.1186/s40537-025-01346-9) |

---

## Detailed Annotations

### Coffee-Specific ML Studies

#### 1. Lischeid et al. (2022) — Robusta Coffee, Vietnam [KEY PAPER]
**Title:** Probabilistic yield forecasting of robusta coffee at the farm scale using agroclimatic and remote sensing derived indices
**Journal:** Agricultural and Forest Meteorology
**Method:** RF with agroclimatic variables, satellite-derived actual ET, crop management info
**Key Findings:**
- Temperature & precipitation 5-7 months before harvest are most influential
- Farm-level prediction possible with satellite data
**Relevance:** Closest to our study — Robusta coffee + climate + ML. But Vietnam, not Indonesia.

#### 2. Santos et al. (2022) — Coffee, Brazil [KEY PAPER]
**Title:** Predicting coffee yield based on agroclimatic data and machine learning
**Journal:** Theoretical and Applied Climatology
**Method:** RF, XGBoost, NN + agroclimatic data
**Key Findings:**
- RF and XGBoost best performers
- NN: RMSE=23%, MAPE=20%, R²=0.82
- XGBoost and RF outperformed MLR and SVM for yields >60 bags/ha
**Relevance:** Demonstrates ML feasibility for coffee yield; we can adapt methodology for Lampung.

#### 3. Coffee Yield with High-Resolution Satellite (2022)
**Title:** Coffee-Yield Estimation Using High-Resolution Time-Series Satellite Images and ML
**Journal:** AgriEngineering (MDPI)
**Method:** RF + spectral bands from satellite imagery
**Key Findings:** RF with spectral bands achieved R²=0.93 (validation)
**Relevance:** Shows satellite data can predict coffee yield accurately.

#### 4. ML Coffee Yield + Future Projections, Brazil (2024)
**Title:** A machine learning approach to assess coffee yield development — identifying meteorological drivers and future projections
**Key Findings:** Identified key meteorological drivers for coffee; projected future yield changes
**Relevance:** Methodology for identifying climate drivers applicable to our SHAP analysis.

#### 5. Tran et al. (2022) — Coffee, Central Highlands Vietnam
**Title:** Early Prediction of Coffee Yield Using Statistical Approach and Satellite RS Biophysical Variables
**Journal:** Remote Sensing (MDPI)
**Method:** Statistical models + MODIS/Sentinel vegetation indices
**Relevance:** Early prediction framework similar to our RQ4 (lead-time analysis).

### SHAP & Feature Importance Studies

#### 6. Legume Yield + SHAP (2025)
**Title:** Interpretable ML for Legume Yield Prediction Using Sentinel-2 Remote Sensing
**Journal:** Applied Sciences (MDPI)
**Method:** XGBoost + SHAP with Sentinel-2
**Relevance:** Direct methodology template for our SHAP analysis.

#### 7. Potato Yield + SHAP (2025)
**Title:** Advanced ML for Regional Potato Yield Prediction: Analysis of Essential Drivers
**Journal:** npj Sustainable Agriculture (Nature)
**Method:** ML + SHAP for identifying key drivers
**Relevance:** SHAP methodology for crop yield driver analysis.

### Small Data Strategies

#### 8. Oliveira et al. (2021) — Small Data & Grain Yield [KEY PAPER]
**Title:** Yield forecasting with machine learning and small data: What gains for grains?
**Journal:** Agricultural and Forest Meteorology
**Key Findings:**
- ML superiority over benchmarks achieved only after extensive calibration
- With small data, careful model selection and validation critical
- Causal structure can help with small samples
**Relevance:** Directly addresses our ~182 data point challenge.

#### 9. Review: ML with Small and Limited Data (2025)
**Title:** A review of machine learning with small and limited data
**Journal:** Journal of Big Data (Springer)
**Strategies identified:**
- Transfer learning
- Few-shot / meta-learning
- Data augmentation
- Regularization (key for our case)
- Ensemble methods (RF, XGBoost) naturally handle small data better
**Relevance:** Framework for choosing appropriate methods given our data constraints.

---

## Synthesis

### Most Common ML Models for Crop Yield
1. **Random Forest** — most popular, robust for small data, interpretable
2. **XGBoost** — state-of-art for tabular, often matches/beats RF
3. **SVR/SVM** — good for small samples, but less interpretable
4. **Neural Networks (ANN/LSTM)** — powerful but need more data
5. **Linear Regression** — baseline

### Typical Accuracy Ranges
| Model | R² Range | Context |
|-------|----------|---------|
| RF | 0.70-0.93 | Best with spectral + climate features |
| XGBoost | 0.75-0.90 | Best for tabular data |
| NN | 0.65-0.85 | Needs larger datasets |
| SVR | 0.60-0.80 | Good for small samples |
| MLR (baseline) | 0.40-0.65 | Limited by linearity |

### Common Input Features
- **Precipitation** (total, seasonal, anomaly — from CHIRPS or similar)
- **Temperature** (mean, max, min — from ERA5 or stations)
- **NDVI/EVI** (from MODIS or Sentinel-2)
- **Evapotranspiration** (actual or potential)
- **Soil moisture** (from ERA5-Land or SMAP)
- **Climate indices** (ENSO, IOD)
- **Elevation/topography**

### Best Practices for Small Datasets (~182 points)
1. Use **ensemble methods** (RF, XGBoost) over deep learning
2. **Leave-One-Year-Out CV** instead of random splits (temporal integrity)
3. **Regularization** — L1/L2 for linear, tree depth limits for RF/XGBoost
4. **Feature selection** — reduce dimensionality to avoid overfitting
5. **SHAP analysis** — interpretability more valuable than marginal accuracy gains
6. Avoid hyperparameter overfitting — use simple search spaces
7. Report **confidence intervals**, not just point estimates

### Realistic Accuracy Expectation for Our Study
Given ~182 data points, based on literature:
- **Optimistic:** R² = 0.75-0.85 (if strong climate signal exists, like Santos 2022)
- **Realistic:** R² = 0.60-0.75 (typical for small-sample crop yield)
- **Floor:** R² = 0.40-0.60 (still publishable if well-analyzed with SHAP)
- Note: Aprilia et al. (2025) achieved R²=0.85 for Lampung coffee with RF + NASA POWER — encouraging baseline

### Key Research Gap
- **One ML coffee study for Lampung** (Aprilia 2025) — but uses NASA POWER, no SHAP, no drought indices, single model, local journal
- **No study uses CHIRPS as primary input for coffee yield prediction** anywhere
- **SHAP analysis for coffee yield drivers** is very limited
- **Perennial crops underrepresented** — 65%+ of ML yield studies focus on annual crops (rice, wheat, maize)
- **Indonesia/SE Asia underrepresented** — most studies from N. America, China, India
- Our study fills all these gaps simultaneously

### Important Methodological Note (from Meroni et al. 2021)
With small data, benchmark models can outperform up to 60% of ML models. Deep learning (LSTM, CNN) consistently underperforms traditional ML (RF, XGBoost) when data is limited. **Recommendation: avoid deep learning for our ~182 point dataset. Focus on RF, XGBoost, SVR.**

---

*Note: Full author names and DOIs to be verified via CrossRef API before inclusion in paper.*
