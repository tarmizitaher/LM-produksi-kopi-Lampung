# Literature Review: Climate Impacts on Robusta Coffee Production in Indonesia

**Focus:** CHIRPS + Machine Learning for Robusta coffee yield prediction in Lampung, Sumatra

**Date compiled:** 2026-03-30

---

## Summary Table

| # | Authors | Year | Title (short) | Journal | Key Method | Relevance |
|---|---------|------|---------------|---------|------------|-----------|
| 1 | Kath et al. | 2020 | Not so robust: Robusta coffee production is highly sensitive to temperature | Global Change Biology | Hierarchical Bayesian modeling, 798 farms | Critical Robusta temperature thresholds |
| 2 | Sarvina et al. | 2021 | Impacts of climate variability on coffee yield in five Indonesian production centers | Coffee Science | ENSO/IOD composite analysis, production data | Direct ENSO/IOD-yield relationship for Lampung |
| 3 | Sarvina et al. | 2022 | Climatic suitability for Robusta coffee in West Lampung under climate change | IOP Conf. Series: Earth Environ. Sci. | MaxEnt, WorldClim projections | Lampung-specific suitability mapping |
| 4 | Sarvina et al. | 2023 | Projection of Robusta coffee's climate suitability for sustainable Indonesian coffee production | Int. J. Sustainable Dev. & Planning | MaxEnt, 5 provinces, 2050 projections | National Robusta suitability decline including Lampung |
| 5 | Pham (Dinh) et al. | 2022 | Statistical analysis of the weather impact on Robusta coffee yield in Vietnam | Frontiers in Environ. Science | Multiple linear regression, PCA, LOO-CV | Methodological reference; weather-yield for Robusta |
| 6 | Kouadio et al. | 2021 | Probabilistic yield forecasting of Robusta coffee at the farm scale | Agricultural & Forest Meteorology | Bayesian + ML, remote sensing + agroclimatic indices | Closest methodological analog (ML + remote sensing + Robusta) |
| 7 | Aprilia et al. | 2025 | Integration of ML and NASA POWER dataset for predicting coffee production in Lampung | Jurnal Fisika Flux | Random Forest, NASA POWER climate data | Most directly relevant: ML + climate + Lampung coffee |
| 8 | Bunn et al. | 2015 | Winner or loser of climate change? Arabica coffee suitability in Indonesia | Regional Environmental Change | Climate suitability modeling, GCM projections | Foundational Indonesia coffee-climate study |
| 9 | Whibowo et al. | 2024 | Climate suitability analysis of Robusta coffee and its projections in South Sumatera | J. Teknik Pertanian Lampung | SSP scenarios, MIROC6, observation data | Neighboring province, same Robusta context |
| 10 | Thalib et al. (review) | 2024 | Climate change impacts on coffee production in Indonesia: A review | J. Critical Ecology | Systematic literature review | Comprehensive overview of Indonesia coffee-climate research |

---

## Detailed Paper Annotations

### Paper 1: Kath et al. (2020)

**Full title:** Not so robust: Robusta coffee production is highly sensitive to temperature

**Authors:** Kath, J.; Byrareddy, V.M.; Craparo, A.; Nguyen-Huy, T.; Mushtaq, S.; Cao, L.; Bossolasco, L.

**Journal:** Global Change Biology, 26(6), 3677-3688

**DOI:** [10.1111/gcb.15097](https://doi.org/10.1111/gcb.15097)

**Methodology:**
- 10 years of yield data from 798 farms across Southeast Asia (primarily Vietnam)
- High-resolution precipitation and temperature data
- Hierarchical Bayesian modeling to isolate temperature and rainfall effects

**Main findings:**
- Robusta optimal mean temperature is ~20.5 degrees C -- markedly lower (1.5-9 degrees C) than previous estimates of >22 degrees C
- Every 1 degree C increase above optimal min/max thresholds of 16.2/24.1 degrees C reduces yield by ~14% (350-460 kg/ha)
- Current climate suitability assessments for Robusta likely overestimate its viable production range
- Robusta is far more climate-sensitive than the industry previously assumed

**Relevance:** Provides the critical temperature thresholds needed for feature engineering in our ML models. Suggests temperature variables (especially minimum temperature during growing season) should be high-priority predictors alongside CHIRPS precipitation.

---

### Paper 2: Sarvina et al. (2021)

**Full title:** The impacts of climate variability on coffee yield in five Indonesian coffee production centers

**Authors:** Sarvina, Y.; June, T.; Sutjahjo, S.H.; Nurmalina, R.; Surmaini, E.

**Journal:** Coffee Science, 16, e161917

**DOI:** [10.25186/.v16i.1917](https://doi.org/10.25186/.v16i.1917)

**Methodology:**
- Annual coffee production data from Indonesia's five major production centers (including Lampung)
- ENSO (Nino 3.4 SST anomaly) and IOD (DMI) indices
- Composite analysis of yield anomalies during El Nino, La Nina, positive IOD, and negative IOD years

**Main findings:**
- La Nina has the most significant impact on coffee production decline (6-22% depending on region)
- El Nino also causes yield decline, but the mechanism differs (drought stress during dry season)
- ENSO/IOD impact on rainfall is most dominant during the dry season (June-September)
- Different production centers show different vulnerability levels to ENSO vs. IOD

**Relevance:** Directly validates the inclusion of ENSO/IOD indices as predictors in our model. The finding that impacts are strongest during dry season aligns with our focus on CHIRPS dry-season precipitation features. Lampung is one of the five study sites.

---

### Paper 3: Sarvina et al. (2022)

**Full title:** Climatic suitability for Robusta coffee in West Lampung under climate change

**Authors:** Sarvina, Y.; et al.

**Journal:** IOP Conference Series: Earth and Environmental Science, 950(1), 012019

**DOI:** [10.1088/1755-1315/950/1/012019](https://doi.org/10.1088/1755-1315/950/1/012019)

**Methodology:**
- Maximum Entropy (MaxEnt) species distribution modeling
- Coffee location data from Indonesia's agricultural commodity maps
- Climate projections from WorldClim under RCP 2.6 and RCP 8.5

**Main findings:**
- Highly suitable area for Robusta in West Lampung projected to decrease ~23.28% under RCP 2.6 by 2050
- Temperature in the driest quarter and diurnal temperature range are the most significant variables
- Current suitable areas are shifting toward higher altitudes
- West Lampung is confirmed as one of Indonesia's major Robusta production areas

**Relevance:** Directly covers our study area. Identifies which climate variables matter most for Lampung Robusta -- temperature during dry season and diurnal range. These should be considered as additional features beyond CHIRPS precipitation.

---

### Paper 4: Sarvina et al. (2023)

**Full title:** Projection of Robusta coffee's climate suitability for sustainable Indonesian coffee production

**Authors:** Sarvina, Y.; June, T.; Sutjahjo, S.H.; Nurmalina, R.; Surmaini, E.

**Journal:** International Journal of Sustainable Development and Planning, 18(4), 1069-1078

**DOI:** [10.18280/ijsdp.180409](https://doi.org/10.18280/ijsdp.180409)

**Methodology:**
- MaxEnt approach applied to 5 provinces: Aceh, North Sumatra, South Sumatra, Bengkulu, Lampung
- WorldClim climate data + coffee occurrence data
- Projections to 2050

**Main findings:**
- Suitable and highly suitable areas for Robusta decrease in all provinces except Bengkulu
- Lampung shows decrement in both highly suitable and suitable classes by 2050
- Aceh, North Sumatra, South Sumatra, and Lampung all need adaptation strategies
- Bengkulu is an exception where highly suitable areas expand

**Relevance:** Provides the broader spatial context for our Lampung study. Demonstrates the urgency of understanding climate-yield relationships in Lampung as suitability declines. Motivates our predictive modeling work.

---

### Paper 5: Pham/Dinh et al. (2022)

**Full title:** Statistical analysis of the weather impact on Robusta coffee yield in Vietnam

**Authors:** Dinh, T.L.A.; Aires, F.; Rahn, E.

**Journal:** Frontiers in Environmental Science, 10, 820916

**DOI:** [10.3389/fenvs.2022.820916](https://doi.org/10.3389/fenvs.2022.820916)

**Methodology:**
- Robusta yield time series 2000-2018, Central Highlands Vietnam
- Multiple linear regression with PCA and leave-one-out cross-validation
- Monthly weather variables as predictors
- Temporal analysis of weather sensitivity windows

**Main findings:**
- Robusta most sensitive to two key moments: (1) prolonged rainy season of previous year (favoring vegetative growth), and (2) low rainfall during bean formation (decreases yield)
- Rainfall distribution between months more influential than total annual rainfall
- Yield anomaly can be forecast 3-6 months before harvest depending on location
- High temperatures + dry conditions favorable during flowering; opposite during growing

**Relevance:** Methodological reference for our regression approach. Key insight: seasonal timing of rainfall matters more than annual totals -- supports our plan to engineer monthly/seasonal CHIRPS features rather than annual aggregates. The 3-6 month forecast lead time is achievable with our approach.

---

### Paper 6: Kouadio et al. (2021)

**Full title:** Probabilistic yield forecasting of Robusta coffee at the farm scale using agroclimatic and remote sensing derived indices

**Authors:** Kouadio, L.; Byrareddy, V.M.; Sawadogo, A.; Newlands, N.K.

**Journal:** Agricultural and Forest Meteorology, 306, 108449

**DOI:** [10.1016/j.agrformet.2021.108449](https://doi.org/10.1016/j.agrformet.2021.108449)

**Methodology:**
- 10-year data (2008-2017) from 558 farmers across 4 Vietnamese provinces
- Integration of farm data, agroclimatic indices, and remotely sensed indices
- Bayesian and machine learning methods
- Probabilistic (not deterministic) forecast framework

**Main findings:**
- Coffee yields predicted with reasonable accuracy using combined agroclimatic + remote sensing indices
- In-season model skill depends on data availability and predictor selection
- Probabilistic approach captures yield uncertainty better than point estimates
- Remote sensing indices add predictive value beyond climate station data alone

**Relevance:** Closest methodological analog to our study. Demonstrates that ML + remote sensing data can effectively predict Robusta coffee yield. However, this was done in Vietnam, not Indonesia -- our study fills the geographic gap. Their use of remote sensing-derived indices parallels our CHIRPS-based approach.

---

### Paper 7: Aprilia et al. (2025)

**Full title:** Integration of machine learning and NASA POWER dataset for predicting coffee production in Lampung

**Authors:** Aprilia et al.

**Journal:** Jurnal Fisika Flux: Jurnal Ilmiah Fisika FMIPA Universitas Lambung Mangkurat, 22(1)

**DOI:** [10.20527/flux.v22i1.20980](https://doi.org/10.20527/flux.v22i1.20980)

**Methodology:**
- NASA POWER dataset (solar radiation, temperature, humidity, pressure, soil wetness, wind speed)
- Random Forest algorithm
- Coffee production data from Lampung

**Main findings:**
- Random Forest achieved R-squared = 85.03%, RMSE = 8.8%, MSE = 5.4%
- RF outperformed linear regression in predictive performance
- Multiple climate variables from NASA POWER contribute to prediction

**Relevance:** **Most directly relevant paper** -- same study area (Lampung), same general approach (ML + climate data for coffee prediction). Key difference: they used NASA POWER reanalysis data while we use CHIRPS satellite precipitation. Our study adds: (1) CHIRPS as primary precipitation input (higher spatial resolution), (2) ENSO/IOD indices, (3) drought indices (SPI/SPEI), (4) multiple ML algorithms with comparison. This paper validates the feasibility of our approach while we extend it.

---

### Paper 8: Bunn et al. (2015)

**Full title:** Winner or loser of climate change? A modeling study of current and future climatic suitability of Arabica coffee in Indonesia

**Authors:** Bunn, C.; Laderach, P.; Ovalle Rivera, O.; Kirschke, D.

**Journal:** Regional Environmental Change, 15, 1473-1482

**DOI:** [10.1007/s10113-014-0713-x](https://doi.org/10.1007/s10113-014-0713-x)

**Methodology:**
- Climate suitability model calibrated on Indonesia's Arabica production zones
- Global Circulation Model projections
- Spatial analysis of suitability shifts

**Main findings:**
- 67% of current Arabica area in Indonesia will no longer be suitable by 2050
- 28% new suitable area emerges (higher altitudes)
- Net loss is substantial for Indonesian coffee sector
- Adaptation through altitude migration is limited

**Relevance:** While focused on Arabica, this foundational study established the framework for understanding climate change impacts on Indonesian coffee. Motivates parallel research on Robusta (our study). The general finding that climate change threatens Indonesian coffee production supports the urgency of our yield prediction work.

---

### Paper 9: Whibowo et al. (2024)

**Full title:** Climate suitability analysis of Robusta coffee and its projections in South Sumatera Province

**Authors:** Whibowo; Arifianto; Ferdiansyah

**Journal:** Jurnal Teknik Pertanian Lampung, 13(2)

**DOI:** Not retrieved; available at [jurnal.fp.unila.ac.id](https://jurnal.fp.unila.ac.id/index.php/JTP/article/view/7918)

**Methodology:**
- 48 rain post observation points in Robusta farming areas
- SSP 2-4.5 and SSP 5-8.5 scenarios with MIROC6 model
- Three projection periods: 2021-2030, 2031-2040, 2041-2050
- Suitability based on temperature, rainfall, dry months, altitude, soil texture, slope

**Main findings:**
- Baseline: 35% very suitable, 65% fairly suitable
- Under SSP2-4.5: 91% very suitable, 9% fairly suitable (all periods) -- actually improves
- South Sumatra appears more resilient than Lampung to climate change for Robusta
- Contrasts with Lampung findings where suitability declines

**Relevance:** Covers the province immediately north of Lampung with the same Robusta coffee system. The contrasting result (South Sumatra stable vs. Lampung declining) highlights the importance of province-level analysis, which our kabupaten-level ML approach captures.

---

### Paper 10: Thalib et al. (2024)

**Full title:** Climate change impacts on coffee production in Indonesia: A review

**Authors:** Thalib et al.

**Journal:** Journal of Critical Ecology (JCRECO), 1(1), 1-7

**DOI:** Available at [journal-iasssf.com](https://journal-iasssf.com/index.php/JCRECO/article/view/645)

**Methodology:**
- Systematic literature review of climate-coffee studies in Indonesia
- Synthesis of adaptation strategies

**Main findings:**
- Indonesia is world's 4th largest coffee exporter; 1.7 million farmers, 75% grow Robusta
- Temperature increases degrade Robusta production; suitable areas shifting to higher altitudes
- Adaptation strategies include shade plantation, soil moisturization control, and modified cultivation calendars aligned with climate predictions
- Overall suitable area is declining under multiple climate scenarios

**Relevance:** Provides the broad overview context for our literature review. Confirms the research motivation and identifies adaptation strategy gaps that predictive models (like ours) could address.

---

## Synthesis

### Key Climate Variables Affecting Robusta Coffee (Critical Thresholds)

| Variable | Optimal Range | Critical Threshold | Effect | Source |
|----------|--------------|-------------------|--------|--------|
| Mean temperature | ~20.5 C | >20.5 C | -14% yield per 1 C increase | Kath et al. 2020 |
| Min temperature (growing season) | <=16.2 C | >16.2 C | -14% yield per 1 C above | Kath et al. 2020 |
| Max temperature (growing season) | <=24.1 C | >24.1 C | -350-460 kg/ha per 1 C above | Kath et al. 2020 |
| Annual rainfall | 1,200-2,000 mm | <1,200 mm (drought stress) | -6.5% yield avg; -22% gross margin | Multiple |
| Rainfall distribution | Even across growing months | Prolonged dry spell during bean formation | Significant yield decline | Pham et al. 2022 |
| Temperature (driest quarter) | Key variable for Lampung | Increasing trend | Suitability decline | Sarvina et al. 2022 |
| Diurnal temperature range | Moderate | Increasing range | Suitability decline | Sarvina et al. 2022 |
| Dry months | 1-3 months needed for flowering | >3 months or 0 months | Extended/irregular flowering | Multiple |

### Phenological Calendar for Robusta Coffee in Indonesia (Lampung)

| Month | Phase | Climate Sensitivity | Notes |
|-------|-------|-------------------|-------|
| Sep-Oct | Flowering initiation | Needs 1+ dry month beforehand; rain triggers flowering | Flowering occurs 2-3 weeks after first significant rains following dry season |
| Oct-Nov | Flowering / fruit set | Temperature and moisture critical | High temp + dry = favorable for flowering |
| Nov-Mar | Berry development / growing | Lower temp + high rainfall favorable | Opposite conditions to flowering |
| Mar-May | Bean filling / maturation | Adequate moisture needed for bean size | Rainfall deficit here reduces yield |
| May-Aug | Harvest (main) | Dry conditions preferred for quality | Excess moisture causes mold/defects |
| Jul-Nov | Export window | -- | Post-harvest processing |

**Key insight for our model:** The critical climate windows are (1) dry season Jun-Aug of previous year (flowering trigger), (2) wet season Nov-Mar (berry development), and (3) Mar-May (bean filling). CHIRPS monthly features should be engineered around these windows.

### Known ENSO/IOD Effects on Indonesian Coffee

| Climate Mode | Effect on Lampung | Mechanism | Yield Impact |
|-------------|-------------------|-----------|-------------|
| **El Nino** | Reduced rainfall, extended dry season | Weakened Walker circulation, suppressed convection over Maritime Continent | Yield decline via drought stress; severity depends on timing relative to phenology |
| **La Nina** | Excess rainfall, flooding risk | Enhanced convection, prolonged wet season | 6-22% yield decline; excessive moisture during flowering disrupts fruit set; harvest quality declines |
| **Positive IOD (+IOD)** | Reduced rainfall over Sumatra | SST gradient in Indian Ocean shifts convection eastward away from Sumatra | Compounded drought when co-occurring with El Nino |
| **Negative IOD (-IOD)** | Enhanced rainfall over Sumatra | Opposite SST gradient brings moisture | Can partially offset El Nino effects; may worsen La Nina impacts |
| **El Nino + pIOD** | Most severe drought | Combined suppression of rainfall | Worst-case scenario for Lampung coffee |

**Key insight:** ENSO and IOD effects are strongest during the dry season (Jun-Sep), which overlaps with the critical pre-flowering period. Both indices should be included as lagged features in our ML models.

### Research Gaps Identified

1. **ML + satellite precipitation data for coffee in Indonesia:** Aprilia et al. (2025) used ML + NASA POWER for Lampung coffee, but **no study has used CHIRPS satellite precipitation data specifically for Indonesian coffee yield prediction**. Our study fills this gap.

2. **Drought indices (SPI/SPEI) for coffee-growing regions in Indonesia:** SPI/SPEI have been applied to general agriculture in Indonesia (e.g., South Sulawesi), but **no published study applies SPI/SPEI specifically to coffee-growing regions in Lampung or Sumatra**. This is a clear gap our study addresses.

3. **Sub-provincial (kabupaten-level) analysis:** Most studies operate at the provincial level. Our kabupaten-level approach (13 kabupaten in Lampung) provides finer spatial resolution.

4. **Combined ENSO/IOD + precipitation + ML framework:** While Sarvina et al. (2021) examined ENSO/IOD effects and Aprilia et al. (2025) used ML, **no study combines ENSO/IOD indices with satellite precipitation data in an ML framework for Indonesian coffee**. Our study integrates these.

5. **CHIRPS validation for coffee regions:** CHIRPS has been validated for West Sumatra cropping patterns but not specifically for Lampung coffee zones.

6. **Temporal forecasting lead time:** Pham et al. (2022) showed 3-6 month forecast potential in Vietnam; this has not been tested for Indonesian Robusta.

7. **Robusta vs. Arabica yield sensitivity comparison using data-driven methods:** Most Indonesian studies focus on suitability mapping (MaxEnt), not data-driven yield prediction.

### How Our Study Positions Itself

Our study (CHIRPS + ML for Robusta coffee yield prediction in Lampung) addresses multiple gaps simultaneously:

- **Data source novelty:** First use of CHIRPS for coffee yield prediction in Indonesia
- **Methodological advance:** Combines satellite precipitation, drought indices (SPI/SPEI from CHIRPS), and ENSO/IOD indices in one ML framework
- **Spatial resolution:** Kabupaten-level analysis (13 units) vs. provincial-level in prior work
- **Practical value:** Yield prediction model vs. suitability mapping -- directly useful for farmers and agricultural planning
- **Comparison potential:** Can benchmark against Aprilia et al.'s NASA POWER approach and Kouadio et al.'s Vietnam Robusta work

---

## Sources

- [Kath et al. 2020 - Global Change Biology](https://onlinelibrary.wiley.com/doi/abs/10.1111/gcb.15097)
- [Sarvina et al. 2021 - Coffee Science](https://coffeescience.ufla.br/index.php/Coffeescience/article/view/1917)
- [Sarvina et al. 2022 - IOP Conf. Series](https://www.researchgate.net/publication/357882215_Climatic_Suitability_for_Robusta_Coffee_in_West_Lampung_Under_Climate_Change)
- [Sarvina et al. 2023 - IJSDP](https://iieta.org/journals/ijsdp/paper/10.18280/ijsdp.180409)
- [Pham/Dinh et al. 2022 - Frontiers in Environ. Science](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2022.820916/full)
- [Kouadio et al. 2021 - Agricultural & Forest Meteorology](https://www.sciencedirect.com/science/article/abs/pii/S0168192321001325)
- [Aprilia et al. 2025 - Jurnal Fisika Flux](https://ppjp.ulm.ac.id/journal/index.php/f/article/view/20980)
- [Bunn et al. 2015 - Regional Environmental Change](https://link.springer.com/article/10.1007/s10113-014-0713-x)
- [Whibowo et al. 2024 - J. Teknik Pertanian Lampung](https://jurnal.fp.unila.ac.id/index.php/JTP/article/view/7918)
- [Thalib et al. 2024 - J. Critical Ecology](https://journal-iasssf.com/index.php/JCRECO/article/view/645)
- [SPI/SPEI drought in South Sulawesi](https://pmc.ncbi.nlm.nih.gov/articles/PMC11903953/)
- [CHIRPS for West Sumatra cropping patterns](https://www.jaast.org/index.php/jaast/article/view/524)
- [Indonesian Coffee Harvest Calendar 2026](https://www.indonesia-coffee.com/en/articles/indonesian-coffee-harvest-calendar-2026-sourcing-guide-xeU2V8)
- [Robusta lifecycle and phenology](https://greg.app/robusta-coffee-lifecycle/)
- [Early flowering changes Robusta yield responses](https://www.sciencedirect.com/science/article/abs/pii/S0048969722059356)

---

*All papers were identified via web search on 2026-03-30. DOIs and details verified against publisher pages where available.*
