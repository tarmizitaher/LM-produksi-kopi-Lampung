# Literature Review: CHIRPS Validation in Indonesia & Southeast Asia

*Sprint 0.1 — Last updated: 2026-03-30*

---

## Summary Table

| # | First Author | Year | Region | Journal | Key Finding | DOI/URL |
|---|-------------|------|--------|---------|-------------|---------|
| 1 | Pratama & Agiel | 2022 | **Lampung Selatan** | J. Science & Applicative Tech. | CHIRPS best at monthly scale (POD=0.86 wet season, 6% bias) | [ResearchGate](https://www.researchgate.net/publication/359873488) |
| 2 | Sahid et al. | 2024 | **Bandar Lampung** | JGISE (UGM) | CHIRPS viable for low-cost flood modeling in Way Garuntang | [UGM](https://jurnal.ugm.ac.id/jgise/article/view/94307) |
| 3 | Marzuki et al. | 2025 | **All Indonesia** | Int. J. Climatology (Q1) | 43yr CHIRPS validated vs 67 gauges: CC>0.7, RB<±25% | [Wiley](https://rmets.onlinelibrary.wiley.com/doi/10.1002/joc.70107) |
| 4 | — | 2024 | Siwaluh Basin, Java | Eng. Proc. (MDPI) | 20yr validation: NSE, RSR, KR metrics | [MDPI](https://www.mdpi.com/2673-4591/84/1/94) |
| 5 | — | 2024 | **North Sumatra** | — | CHIRPS accuracy for onset wet/dry season detection | [ResearchGate](https://www.researchgate.net/publication/381854174) |
| 6 | — | 2024 | Ciliwung, Jakarta | Int. J. Livable Space | 30yr CHIRPS correction factor for Ciliwung watershed | [Trisakti](https://e-journal.trisakti.ac.id/index.php/livas/article/view/19919) |
| 7 | — | 2023 | Kalimantan Barat | J. Rekayasa Pertanian | Daily validation: r=0.25, bias=9.92%, RMSE=19.82mm | [UNRAM](https://jrpb.unram.ac.id/index.php/jrpb/article/view/442) |
| 8 | — | 2024 | **Kalimantan** | — | CHIRPS best at monthly scale (RMSE=81mm/mo); GSMaP best daily | [ResearchGate](https://www.researchgate.net/publication/380818049) |
| 9 | — | 2021 | Papua Barat | J. Teknik Pertanian Lampung | CHIRPS vs AWS: RMSE=8.59mm, ME=2.75mm (moderate accuracy) | [Unila](https://jurnal.fp.unila.ac.id/index.php/JTP/article/view/4731) |
| 10 | — | 2025 | Jakarta | J. Water & Land Dev. | CHIRPS vs ground for hybrid ML flood prediction | [UI Scholar](https://scholar.ui.ac.id/en/publications/hybrid-machine-learning-for-flood-prediction-comparing-chirps-sat) |
| 11 | Ismanto et al. | 2024 | All Indonesia | J. Meteorologi & Geofisika (BMKG) | Himawari-8 vs CHIRPS vs GSMaP rain detection | [BMKG](https://jmg.bmkg.go.id/jmg/index.php/jmg/article/view/863) |
| 12 | — | 2024 | West Sumatra | JAAST | CHIRPS spatio-temporal analysis for cropping patterns | [JAAST](https://www.jaast.org/index.php/jaast/article/view/524) |
| 13 | — | 2021 | Brantas, Java | Hydrology (MDPI) | CHIRPS & PERSIANN similar: 8-13% NRSME daily | [MDPI](https://www.mdpi.com/2306-5338/8/4/154) |
| 14 | — | 2019 | Mekong Basin, SEA | Remote Sensing (MDPI) | CHIRPS r=0.83 for high-precip stations (>2500mm/yr) | [MDPI](https://www.mdpi.com/2072-4292/11/22/2709) |
| 15 | — | 2025 | Southeast Asia | PLOS One | Daily CHIRPS RMSE=15.03mm/day, best among products | [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319477) |

---

## Detailed Annotations

### 1. Pratama & Agiel (2022) — Lampung Selatan [KEY PAPER]
**Title:** Evaluasi Satellite Precipitation Product (GSMaP, CHIRPS, dan IMERG) di Kabupaten Lampung Selatan
**Journal:** Journal of Science and Applicative Technology
**Period:** 2018-2020
**Method:** Compared GSMaP, CHIRPS, IMERG against AWS data at monthly, 10-daily, and daily scales
**Key Findings:**
- CHIRPS POD = 0.86 (wet season), 0.85 (transition I) — best rain detection
- Monthly scale: CHIRPS shows excellent linearity, slightly overestimated (6% bias)
- Daily scale: IMERG shows better linearity than GSMaP and CHIRPS
- **This is the only validation study specifically in Lampung** — directly supports our work
**Relevance:** Establishes baseline CHIRPS accuracy in our exact study area. We can extend this to coffee-growing districts.

### 2. Sahid et al. (2024) — Bandar Lampung [KEY PAPER]
**Title:** Low-cost alternative flood modeling using CHIRPS data in the Way Garuntang Catchment, Bandar Lampung
**Journal:** JGISE (UGM)
**Method:** Used CHIRPS as rainfall input for HEC-RAS flood modeling
**Key Findings:**
- CHIRPS data accuracy is sufficient as alternative to station data for flood modeling
- Demonstrates practical application of CHIRPS in Lampung
**Relevance:** Validates CHIRPS usability for applied research in Lampung.

### 3. Marzuki et al. (2025) — All Indonesia [KEY PAPER]
**Title:** Long-term spatial-temporal variability, trends and extreme rainfall events over Indonesia based on 43 years of CHIRPS data
**Journal:** International Journal of Climatology (Q1, IF ~4.0)
**Period:** 1981-2023
**Method:** Mann-Kendall trend test, Theil-Sen slope, validated vs 67 BMKG gauges
**Key Findings:**
- CHIRPS v2.0 reliability: CC > 0.7, relative bias < ±25% across Indonesia
- Sumatra has lowest interannual variability (CV < 15%)
- Comprehensive 43-year analysis — the benchmark for CHIRPS in Indonesia
**Relevance:** Provides national-scale validation that supports using CHIRPS in Lampung. Published in our target journal.

### 4. Siwaluh Basin Study (2024) — Central Java
**Title:** Evaluation and Reliability of CHIRPS Satellite Rainfall Products Against Station Rainfall Data in the Siwaluh Basin
**Journal:** Engineering Proceedings (MDPI)
**Period:** 2004-2023 (20 years)
**Method:** NSE, RSR, KR metrics
**Relevance:** Methodology reference for our validation approach.

### 5. North Sumatra Study (2024)
**Title:** Accuracy of CHIRPS rainfall data and its utilization in determining the onset of wet and dry seasons in North Sumatra
**Method:** Contingency Table method, 4 BMKG stations
**Relevance:** Shows CHIRPS can detect seasonal onset in Sumatra — relevant for our seasonal feature engineering.

### 6. Kalimantan Barat Study (2023)
**Title:** Validasi Curah Hujan Harian CHIRPS di Provinsi Kalimantan Barat
**Key Findings:** Pearson r = 0.25 (weak daily), bias = 9.92%, RMSE = 19.82mm
**Relevance:** Shows CHIRPS daily data has limitations — supports our choice of monthly aggregation.

### 7. Kalimantan Comparison (2024)
**Title:** Comparison Accuracy of CHIRPS, GSMaP V7, and GSMaP V8 in Kalimantan
**Key Findings:** CHIRPS best at monthly (RMSE=81mm/mo), GSMaP V8 best daily (RMSE=14.31mm/day)
**Relevance:** Confirms CHIRPS strength at monthly scale — aligns with our monthly feature approach.

### 8. Lower Mekong Basin (2019) — Regional SEA
**Title:** Evaluation of Satellite-Based Rainfall Estimates in the Lower Mekong River Basin
**Journal:** Remote Sensing (MDPI, Q1)
**Key Findings:** CHIRPS r=0.83 for high-precip areas (>2500mm/yr); better performance in wetter regions
**Relevance:** Lampung receives 2000-3000mm/yr — falls in CHIRPS's strong performance range.

---

## Synthesis

### Typical CHIRPS Accuracy in Indonesia
| Scale | Correlation (r) | Bias | RMSE | Best For |
|-------|-----------------|------|------|----------|
| Monthly | 0.7-0.9 | 5-15% | 50-100 mm/mo | Trend analysis, seasonal features |
| 10-daily | 0.5-0.8 | 10-20% | — | Crop phenology |
| Daily | 0.2-0.6 | 10-30% | 8-19 mm/day | Less reliable; prefer monthly |

### Common Validation Metrics Used
- Pearson correlation coefficient (r / CC)
- RMSE / NRMSE
- Bias / Relative Bias (%)
- Nash-Sutcliffe Efficiency (NSE)
- POD (Probability of Detection), FAR (False Alarm Ratio), CSI (Critical Success Index)

### Known CHIRPS Limitations in Indonesia
- Slight overestimation in wet season (~6% in Lampung)
- Weak daily correlation (r ~ 0.25 in some regions) — monthly is much better
- Orographic effects: may underestimate in mountainous areas (relevant for Lampung Barat)
- Coastal effects: less reliable near complex coastlines

### Research Gap Our Study Fills
1. **Only one CHIRPS validation study exists for Lampung** (Pratama & Agiel 2022) — and it's limited to Lampung Selatan, 2018-2020
2. **No validation specifically for coffee-growing districts** (Lampung Barat, Tanggamus) which are mountainous
3. **No study links CHIRPS validation to agricultural application** in Lampung
4. Our study will provide: longer period (2010-2023), more stations, and direct application to yield prediction

---

*Note: Full author names and DOIs to be verified via CrossRef API before inclusion in paper (per reference rules).*
