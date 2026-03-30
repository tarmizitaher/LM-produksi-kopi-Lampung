# Literature Review: Coffee & Climate in Indonesia

*Sprint 0.3 — Last updated: 2026-03-30*

---

## Summary Table

| # | First Author | Year | Focus | Journal | DOI/URL |
|---|-------------|------|-------|---------|---------|
| 1 | — | 2023 | Robusta suitability projection, 5 provinces incl. Lampung | IJSDP (IIETA) | [IIETA](https://iieta.org/journals/ijsdp/paper/10.18280/ijsdp.180409) |
| 2 | — | 2022 | Robusta suitability West Lampung + climate change | — | [ResearchGate](https://www.researchgate.net/publication/357882215) |
| 3 | Whibowo et al. | 2024 | Robusta suitability South Sumatra projections | J. Teknik Pertanian Lampung | [Unila](https://jurnal.fp.unila.ac.id/index.php/JTP/article/view/7918) |
| 4 | Bunn et al. | 2015 | Arabica suitability Indonesia — winner/loser | Reg. Environ. Change (Springer) | [Springer](https://link.springer.com/article/10.1007/s10113-014-0713-x) |
| 5 | — | — | Climate variability impacts on coffee yield, 5 centers | Coffee Science | [CoffeeScience](https://coffeescience.ufla.br/index.php/Coffeescience/article/view/1917) |
| 6 | — | 2021 | Temperature & rainfall impacts on Robusta bean quality | Weather Clim. Soc. | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2212096321000103) |
| 7 | — | 2022 | Early flowering changes Robusta yield response to stress | Sci. Total Environ. | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0048969722059356) |
| 8 | — | 2022 | Statistical weather impact on Robusta yield, Vietnam | Frontiers Environ. Sci. | [Frontiers](https://www.frontiersin.org/articles/10.3389/fenvs.2022.820916/full) |
| 9 | — | 2019 | 10-yr monitoring Robusta farms Vietnam & Indonesia | Sustainability (MDPI) | [ResearchGate](https://www.researchgate.net/publication/335506107) |
| 10 | — | — | Climate change impacts on coffee in Indonesia (review) | J. IASSSF | [Download](https://www.journal-iasssf.com/index.php/JCRECO/article/download/645/566/4400) |
| 11 | **Aprilia et al.** | **2025** | **ML + NASA POWER for coffee prediction in Lampung** | **J. Fisika Flux (ULM)** | **[ULM](https://ppjp.ulm.ac.id/journal/index.php/f/article/view/20980)** |

---

## Detailed Annotations

### 1. Robusta Coffee Climate Suitability — 5 Indonesian Provinces (2023) [KEY PAPER]
**Title:** Projection of Robusta Coffee's Climate Suitability for Sustainable Indonesian Coffee Production
**Journal:** IJSDP (IIETA)
**Method:** Maxent model, WorldClim climate data, RCP 2.6 & 8.5 scenarios
**Provinces:** Aceh, North Sumatra, South Sumatra, Bengkulu, **Lampung**
**Key Findings:**
- AUC values: 0.926-0.985 (highly reliable) — **Lampung AUC = 0.985**
- Highly suitable area in Lampung projected to **decrease from 1.63% to 0.56%** by 2050 (RCP 2.6)
- Temperature in driest quarter and diurnal temperature range most significant variables for Lampung
- All provinces except Bengkulu show declining suitability
**Relevance:** Directly establishes climate threat to Lampung coffee. Our study adds predictive capability.

### 2. Climatic Suitability for Robusta in West Lampung (2022) [KEY PAPER]
**Title:** Climatic Suitability for Robusta Coffee in West Lampung Under Climate Change
**Method:** Maxent + WorldClim
**Key Findings:**
- West Lampung currently supports 155,200 ha of coffee plantations
- Climate suitability expected to decrease under all scenarios
- Temperature-related variables most important
**Relevance:** West Lampung is our primary coffee district. Study uses Maxent only — no ML yield prediction.

### 3. Robusta Suitability in South Sumatra (2024)
**Title:** Climate Suitability Analysis of Robusta Coffee and Its Projections in South Sumatera Province
**Journal:** J. Teknik Pertanian Lampung (Unila)
**Key Findings:** South Sumatra maintains high suitability under most scenarios
**Relevance:** Neighboring province — could extend our study area for more data points.

### 4. ENSO/Climate Variability Impacts on Coffee Yield (Indonesia)
**Title:** The impacts of climate variability on coffee yield in five Indonesian coffee production centers
**Journal:** Coffee Science
**Key Findings:**
- Directly quantifies climate variability effects on Indonesian coffee
- Five production centers analyzed
**Relevance:** Establishes the climate-coffee link in Indonesia that our ML model aims to capture.

### 5. Temperature & Rainfall Impacts on Robusta Bean Quality (2021)
**Title:** Temperature and rainfall impacts on robusta coffee bean characteristics
**Journal:** Weather, Climate, and Society
**Key Findings:**
- Higher rainfall during harvest → increased defects
- Dry/warm conditions during flowering → better quality larger beans
- Rainfall timing matters more than total amount
**Relevance:** Supports our hypothesis (H2) that seasonal precipitation windows matter most.

### 6. Early Flowering Changes Robusta Yield Response (2022)
**Title:** Early flowering changes robusta coffee yield responses to climate stress and management
**Journal:** Science of the Total Environment
**Key Findings:**
- Altered flowering timing affects yield response to climate stress
- Phenological shifts must be considered in climate-yield models
**Relevance:** Important for understanding lag effects in our feature engineering.

### 7. ENSO Impact on Indonesian Coffee (Industry Reports)
**Key findings from multiple sources:**
- Indonesian coffee production declined **~20% during 2023-2024 El Nino**
- Production dropped from ~12M to <10M bags (60kg)
- El Nino causes later rainy season, prolonged dry season
- When positive IOD + El Nino co-occur → rainfall decrease amplified
- Highland Sumatra areas may benefit; lowland areas severely impacted
**Relevance:** Strong empirical evidence for H3 (El Nino → ≥15% decline).

---

## Synthesis

### Robusta Coffee Phenological Calendar (Indonesia)

| Month | Phase | Climate Sensitivity |
|-------|-------|-------------------|
| **Jun-Aug** | **Flowering** | Needs dry period (2-3 months) for bud differentiation; first rain triggers synchronized flowering |
| **Sep-Nov** | Fruit development | Rainfall needed for fruit filling; too much → defects |
| **Dec-Feb** | Fruit maturation | Moderate rainfall acceptable |
| **Mar-May** | **Harvest** | Dry preferred for quality; wet → mouldy beans |
| Apr-Jun | Vegetative growth | Rainfall supports new growth |

### Key Climate Variables for Robusta Coffee
| Variable | Optimal Range | Critical Threshold |
|----------|--------------|-------------------|
| Annual rainfall | 1,200-2,000 mm | <1,000 mm severe stress; >3,000 mm quality issues |
| Temperature | 22-28°C | >30°C heat stress; <15°C growth stops |
| Dry season | 2-3 months | <1 month insufficient for flowering trigger |
| Humidity | 70-80% | >90% → disease risk |
| Elevation | 200-800 m asl | Lower limit for Robusta |

### ENSO/IOD Effects on Indonesian Coffee
- **El Nino:** Delayed rainy season, prolonged drought → 15-20% yield decline
- **La Nina:** Excess rainfall → quality issues, but yield may increase
- **Positive IOD:** Amplifies El Nino drought effect
- **Combined El Nino + positive IOD:** Worst case — significant production loss

### 8. Aprilia et al. (2025) — ML + NASA POWER, Lampung [KEY PAPER — CLOSEST COMPETITOR]
**Title:** Integration of Machine Learning and NASA POWER Dataset for Predicting Coffee Production in Lampung
**Journal:** Jurnal Fisika Flux (Universitas Lambung Mangkurat)
**Method:** Random Forest + NASA POWER data (solar radiation, temperature, humidity, pressure, soil wetness, wind speed)
**Key Findings:**
- R² = 0.85, RMSE = 8.8%, MSE = 5.4%
- RF performed well for Lampung coffee prediction
- Built a website prototype for prediction
**Limitations (our advantage over this study):**
- Uses NASA POWER (coarser resolution) — not CHIRPS (0.05°, higher spatial detail)
- No SHAP/feature importance analysis
- No drought indices (SPI/SPEI)
- No ENSO/IOD analysis
- No ablation study or model comparison (only RF)
- Published in local journal (not Q1/Q2 international)
**Relevance:** This is the most comparable study. We must cite and clearly differentiate from it.

---

### Critical Research Gap (Updated)
**One study (Aprilia et al. 2025) used ML for coffee prediction in Lampung**, but with NASA POWER data and limited methodology.

**Our study advances beyond Aprilia et al. by:**
1. Using **CHIRPS** (0.05° resolution) instead of NASA POWER (0.5° resolution) — 10x spatial detail
2. Adding **drought indices (SPI)** as features — linking climate anomalies to yield
3. Including **ENSO/IOD** as predictors — capturing teleconnection effects
4. Comparing **multiple ML models** (RF, XGBoost, SVR, LR) — not just RF
5. Applying **SHAP analysis** — interpretable identification of key climate drivers
6. Conducting **CHIRPS validation** against BMKG — establishing data reliability
7. Building an **early warning framework** with lead-time analysis
8. Targeting **Q1/Q2 international journal** with rigorous methodology

**Our novelty statement remains strong** — this is the first study to combine CHIRPS + multi-model ML + drought indices + SHAP for Robusta coffee yield prediction in Indonesia.

---

*Note: Full author names and DOIs to be verified via CrossRef API before inclusion in paper.*
