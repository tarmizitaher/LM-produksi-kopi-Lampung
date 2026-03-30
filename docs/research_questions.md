# Research Questions & Hypotheses
## CHIRPS-ML Coffee Yield Prediction — Lampung, Indonesia

*Version 2.0 — Refined for Q1/Q2 journal submission*

---

## Overarching Research Question

> **To what extent can satellite-derived precipitation data (CHIRPS), combined with machine learning, predict Robusta coffee productivity in Lampung, Indonesia — and which climate drivers matter most?**

---

## Specific Research Questions

### RQ1 — CHIRPS Validation (Foundation)
**How accurately does CHIRPS v2.0 represent precipitation patterns in Lampung's coffee-growing regions compared to BMKG gauge stations?**

- **Why it matters:** If CHIRPS is unreliable for Lampung, the entire study's premise falls apart. This must be established first.
- **Testable metrics:** Pearson correlation (r), bias (%), RMSE, probability of detection (POD), false alarm ratio (FAR)
- **Hypothesis H1:** CHIRPS monthly precipitation correlates with BMKG gauge data at r > 0.7 and bias < ±15% across Lampung's coffee districts
- **Expected output:** Validation table + scatter plots per station + spatial bias map

### RQ2 — Climate-Yield Relationship (Core Science)
**Which precipitation-derived variables exhibit the strongest influence on inter-annual variability of Robusta coffee productivity in Lampung?**

- **Why it matters:** This is the scientific contribution — understanding the climate-coffee nexus specific to Lampung's tropical monsoon system
- **Sub-questions:**
  - RQ2a: Is dry-season precipitation (Jun-Sep) more influential than wet-season precipitation on coffee productivity?
  - RQ2b: Do drought anomalies (SPI < -1) during the flowering phase (Jun-Aug) have a lagged negative effect on the subsequent harvest?
  - RQ2c: How do large-scale climate modes (ENSO, IOD) modulate the precipitation-productivity relationship in Lampung?
- **Hypothesis H2:** Dry-season precipitation and SPI during the flowering phase (Jun-Aug) are the top-2 most important predictors, outranking total annual precipitation
- **Hypothesis H3:** El Nino years (Nino 3.4 > 0.5°C) are associated with ≥15% decline in coffee productivity in Lampung
- **Expected output:** Correlation matrix, SHAP feature importance, partial dependence plots, ENSO composite analysis

### RQ3 — Predictive Modeling (Applied Contribution)
**Which machine learning approach provides the most accurate and robust prediction of Robusta coffee productivity using satellite-derived climate features?**

- **Why it matters:** Demonstrates practical value — can we actually forecast yield?
- **Sub-questions:**
  - RQ3a: Do ensemble models (RF, XGBoost) outperform linear regression and SVR for this small-sample, high-dimensional problem?
  - RQ3b: Does adding MODIS vegetation indices (NDVI/EVI) as features significantly improve prediction accuracy beyond precipitation-only models?
  - RQ3c: What is the minimum set of features needed to achieve ≥90% of the full model's performance? (parsimony analysis)
- **Hypothesis H4:** XGBoost achieves the best performance (R² > 0.75, MAPE < 12%) using the full feature set
- **Hypothesis H5:** A precipitation-only model (CHIRPS features) achieves ≥80% of the full model's R², demonstrating CHIRPS's standalone predictive value
- **Expected output:** Model comparison table, ablation study table, learning curves, prediction vs actual plots

### RQ4 — Early Warning Application (Impact)
**Can the best-performing model serve as a seasonal early warning tool for coffee productivity decline in Lampung?**

- **Why it matters:** Bridges the gap from science to policy — gives the research real-world applicability
- **Sub-questions:**
  - RQ4a: How far in advance (lead time) can the model predict below-average productivity?
  - RQ4b: What is the model's skill in detecting drought-induced productivity losses (sensitivity/specificity)?
- **Hypothesis H6:** Using precipitation data up to August (end of flowering), the model can predict the subsequent harvest productivity with R² > 0.60 (3-4 month lead time)
- **Expected output:** Lead-time analysis plot, confusion matrix for above/below-average classification, early warning framework diagram

---

## Mapping RQs to Paper Sections

| RQ | Paper Section | Key Figures/Tables |
|----|--------------|-------------------|
| RQ1 | 4.1 CHIRPS Validation | Fig. scatter plot, Table correlation metrics, Fig. spatial bias map |
| RQ2 | 4.2 Climate-Yield Relationships | Fig. SHAP summary, Fig. partial dependence, Fig. ENSO composite |
| RQ3 | 4.3 Model Performance | Table model comparison, Fig. ablation study, Fig. predicted vs actual |
| RQ4 | 4.4 Early Warning Application | Fig. lead-time skill, Table sensitivity/specificity |

## Mapping RQs to Hypotheses

| Hypothesis | RQ | Testable Criterion | Accept if... |
|-----------|-----|-------------------|-------------|
| H1 | RQ1 | CHIRPS vs BMKG correlation | r > 0.7, bias < ±15% |
| H2 | RQ2 | Feature importance ranking | Dry-season precip & flowering SPI in top-2 |
| H3 | RQ2c | ENSO-productivity composite | El Nino years show ≥15% productivity decline |
| H4 | RQ3 | Best model performance | R² > 0.75, MAPE < 12% |
| H5 | RQ3b | CHIRPS-only vs full model | CHIRPS-only achieves ≥80% of full R² |
| H6 | RQ4 | Lead-time prediction | R² > 0.60 at 3-month lead |

---

## Novelty Statement (for Introduction)

*This study makes three contributions:*
1. **First validation of CHIRPS against gauge data specifically for Lampung's coffee-growing districts** — prior validations in Indonesia focused on Java and Kalimantan
2. **First ML-based coffee yield prediction for Indonesia using satellite precipitation** — existing studies use statistical methods (Maxent) or focus on climate suitability rather than yield prediction
3. **Identification of critical precipitation windows for Lampung Robusta coffee** — linking seasonal drought indices to productivity through interpretable ML (SHAP), providing actionable insights for farmers and policymakers

---

*Last updated: 2026-03-30*
