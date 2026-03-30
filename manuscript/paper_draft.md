# Climate-Driven Robusta Coffee Yield Prediction in Lampung, Indonesia: A Machine Learning Approach Using CHIRPS Satellite Precipitation Data

**Authors:** [To be determined]

**Target Journal:** International Journal of Climatology / Remote Sensing (MDPI)

**Status:** First Draft — Sections 1–3

---

## Abstract

*[To be written last, after all results are finalized]*

---

## 1. Introduction

Coffee is one of the most economically important agricultural commodities worldwide, with Indonesia ranking as the fourth-largest producer globally. Within Indonesia, Lampung Province serves as the second-largest Robusta coffee producing region, contributing approximately 15% of national coffee output with an annual production exceeding 110,000 tons from roughly 155,000 hectares of plantation area (BPS, 2023). The province's coffee sector supports the livelihoods of hundreds of thousands of smallholder farmers and plays a central role in the regional economy.

Robusta coffee (*Coffea canephora*) is a perennial crop with a biennial bearing cycle, making it particularly sensitive to inter-annual climate variability. Unlike annual crops that complete their reproductive cycle within a single growing season, coffee requires 9–11 months from flowering to fruit maturation, meaning that climate conditions during critical phenological stages can have delayed and compounding effects on yield. In Lampung's tropical monsoon climate, the dry season (June–September) triggers flower bud differentiation, with the onset of rains initiating synchronized flowering — a mechanism that renders coffee productivity highly dependent on the timing, duration, and intensity of seasonal precipitation patterns.

Recent studies have demonstrated that climate change poses a significant threat to coffee production in Indonesia. Sarvina et al. (2023) projected that the area with highly suitable climate for Robusta coffee in Lampung would decrease from 1.63% to 0.56% by 2050 under the RCP 2.6 scenario. Furthermore, El Niño–Southern Oscillation (ENSO) events have been associated with substantial production losses — Indonesian coffee output declined by approximately 20% during the 2023–2024 El Niño episode, with lowland areas in Sumatra experiencing severe heat and drought stress. The Indian Ocean Dipole (IOD) can amplify these effects when co-occurring with El Niño, further reducing rainfall across Lampung's coffee-growing districts.

Despite the clear climate sensitivity of Robusta coffee in Lampung, quantitative tools for predicting yield based on climate data remain underdeveloped. Existing climate-coffee studies in the region have focused primarily on suitability mapping using the Maxent approach (Sarvina et al., 2022, 2023), which assesses where coffee can grow rather than how much it will produce. Statistical analyses of weather impacts on Robusta yield have been conducted in Vietnam (Dinh et al., 2022) and Brazil (Aparecido et al., 2022), but not for Indonesian production systems. A recent study by Aprilia et al. (2025) applied Random Forest to predict coffee production in Lampung using NASA POWER meteorological data, achieving an R² of 0.85. However, this study was limited to a single model without feature importance analysis, drought indices, or climate teleconnection predictors, and employed NASA POWER data at a relatively coarse spatial resolution of 0.5°.

Satellite-based precipitation products offer a promising alternative to sparse gauge networks for climate-agricultural studies in data-limited regions. The Climate Hazards Group InfraRed Precipitation with Stations (CHIRPS) dataset (Funk et al., 2015) provides quasi-global precipitation estimates at 0.05° (~5 km) spatial resolution from 1981 to near-present, combining satellite infrared observations with in-situ station data. CHIRPS has been validated across Indonesia with generally high reliability at the monthly scale (correlation coefficient > 0.7, relative bias < ±25%) (Marzuki et al., 2025), and a specific validation in South Lampung reported a probability of detection of 0.86 during the wet season (Pratama and Agiel, 2022). The high spatial resolution and long temporal record of CHIRPS make it particularly suitable for capturing precipitation variability across Lampung's topographically diverse coffee-growing districts, which range from coastal lowlands to the Bukit Barisan highlands.

Machine learning (ML) approaches have demonstrated considerable potential for crop yield prediction by capturing nonlinear relationships between climate variables and agricultural productivity. Random Forest and XGBoost have consistently emerged as top-performing models for tabular agricultural data, with reported R² values of 0.70–0.93 in coffee yield studies (Aparecido et al., 2022; Kouadio et al., 2021). SHapley Additive exPlanations (SHAP) analysis has become the standard method for interpreting ML predictions, enabling identification of key climate drivers and their directional effects on yield. Importantly, Meroni et al. (2021) demonstrated that ML models can outperform benchmarks for crop yield prediction even with limited sample sizes, provided that appropriate model selection, regularization, and validation strategies are employed.

This study addresses the following research questions:

1. How accurately does CHIRPS v2.0 represent precipitation patterns in Lampung's coffee-growing regions compared to BMKG gauge stations?
2. Which precipitation-derived variables exhibit the strongest influence on inter-annual variability of Robusta coffee productivity in Lampung?
3. Which machine learning approach provides the most accurate and robust prediction of Robusta coffee productivity using satellite-derived climate features?
4. Can the best-performing model serve as a seasonal early warning tool for coffee productivity decline?

This study makes three contributions. First, it provides the first validation of CHIRPS against gauge data specifically for Lampung's coffee-growing districts — prior validations in Indonesia focused on Java and Kalimantan. Second, it presents the first ML-based coffee yield prediction for Indonesia using satellite precipitation, advancing beyond the single-model NASA POWER approach of Aprilia et al. (2025) with higher spatial resolution data, multiple model comparison, drought indices, and SHAP-based interpretability. Third, it identifies critical precipitation windows for Lampung Robusta coffee through interpretable ML, providing actionable insights for farmers and policymakers facing increasing climate variability.

---

## 2. Study Area and Data

### 2.1 Study Area

Lampung Province is located at the southern tip of Sumatra Island, Indonesia, spanning approximately 103.5°E–106.0°E longitude and 3.5°S–6.0°S latitude (Fig. 1). The province covers an area of approximately 34,624 km² and is bordered by the Sunda Strait to the south, the Java Sea to the east, and the provinces of South Sumatra and Bengkulu to the north and west, respectively.

The topography of Lampung is characterized by a pronounced west-to-east gradient, with the Bukit Barisan mountain range occupying the western portion of the province (elevations exceeding 2,000 m above sea level in Pesisir Barat and Lampung Barat districts) and gradually descending to lowland plains and coastal areas in the east. This topographic diversity creates distinct microclimatic zones that influence the spatial distribution of coffee cultivation.

Lampung experiences a tropical monsoon climate (Köppen type Am) with a distinct wet season (November–March) and dry season (June–September), separated by transitional periods in April–May and October. Mean annual precipitation ranges from approximately 2,000 mm in the eastern lowlands to over 3,000 mm in the western highlands. Mean annual temperature ranges from 26–28°C in the lowlands to 20–24°C in the highlands.

Robusta coffee cultivation in Lampung is concentrated in five major producing districts: Lampung Barat (54,106 ha, 34.5% of provincial coffee area), Tanggamus (41,510 ha), Lampung Utara (25,679 ha), Way Kanan (21,655 ha), and Pesisir Barat (6,704 ha). Together, these five districts account for over 95% of the province's coffee plantation area of approximately 156,000 ha (Dinas Perkebunan Lampung, 2020). Coffee is predominantly grown by smallholder farmers at elevations between 200 and 800 m above sea level, with Lampung Barat serving as the primary production center, contributing approximately 50% of provincial coffee output.

### 2.2 Data Sources

#### 2.2.1 CHIRPS Precipitation Data

Monthly precipitation data were obtained from the Climate Hazards Group InfraRed Precipitation with Stations version 2.0 (CHIRPS v2.0) dataset (Funk et al., 2015). CHIRPS provides quasi-global (50°S–50°N) gridded precipitation estimates at 0.05° (~5 km) spatial resolution and daily to monthly temporal resolution, spanning from 1981 to near-present. The dataset blends satellite-based infrared cold cloud duration estimates with in-situ station observations using a modified inverse distance weighting algorithm. Monthly CHIRPS GeoTIFF files were downloaded from the Climate Hazards Center data server (https://data.chc.ucsb.edu/products/CHIRPS-2.0/) and clipped to the Lampung bounding box (103.5°E–106.0°E, 3.5°S–6.0°S). Data from 1981–2023 were used for SPI baseline computation, with the study period analysis focused on 2010–2023.

#### 2.2.2 Coffee Production Data

Annual Robusta coffee production statistics (harvested area in hectares, production in tons, and productivity in kg/ha) were obtained from the Badan Pusat Statistik (BPS) Lampung Province for the period 2010–2023. Provincial-level aggregate data were supplemented with per-district data from the Dinas Perkebunan (Plantation Office) of Lampung Province. Productivity (kg/ha), computed as production divided by harvested area, was used as the target variable for the prediction models.

#### 2.2.3 Climate Indices

Monthly ENSO indices (Oceanic Niño Index, ONI, based on the Niño 3.4 region sea surface temperature anomaly) were obtained from the NOAA Climate Prediction Center (https://www.cpc.ncep.noaa.gov/). Monthly Indian Ocean Dipole Mode Index (DMI) values were obtained from the NOAA Physical Sciences Laboratory (https://psl.noaa.gov/). Both indices were aggregated to annual means and seasonal averages for use as predictors.

#### 2.2.4 ERA5 Reanalysis Data

*[To be added after data acquisition — monthly temperature, humidity, evapotranspiration from Copernicus Climate Data Store]*

#### 2.2.5 MODIS Vegetation Indices

*[To be added after data acquisition — NDVI and EVI from NASA Earthdata]*

#### 2.2.6 Digital Elevation Model

*[To be added — SRTM 30m or DEMNAS for elevation and slope features]*

### 2.3 Data Summary

Table 1 summarizes all datasets used in this study.

| Dataset | Source | Variables | Spatial Resolution | Temporal Resolution | Period | Access |
|---------|--------|-----------|-------------------|--------------------|---------| ------|
| CHIRPS v2.0 | CHC UCSB | Precipitation (mm) | 0.05° (~5 km) | Monthly | 1981–2023 | Open |
| BPS Coffee Production | BPS Lampung | Area (ha), production (ton), productivity (kg/ha) | Provincial / district | Annual | 2010–2023 | Open |
| ENSO ONI | NOAA CPC | Niño 3.4 SST anomaly (°C) | Global index | Monthly | 1950–2025 | Open |
| IOD DMI | NOAA PSL | Dipole Mode Index (°C) | Global index | Monthly | 1870–2025 | Open |
| ERA5 | Copernicus CDS | Temperature, humidity, ET₀ | 0.25° (~25 km) | Monthly | 2010–2023 | Open |
| MODIS (MOD13A3) | NASA Earthdata | NDVI, EVI | 1 km | Monthly | 2010–2023 | Open |
| DEM | USGS/BIG | Elevation (m) | 30 m | Static | — | Open |

---

## 3. Methodology

### 3.1 Overview

The methodological framework comprises four stages: (1) CHIRPS validation against gauge stations, (2) feature engineering from multi-source climate data, (3) ML model training and comparison, and (4) interpretability analysis and early warning framework development (Fig. 2). All analyses were conducted in Python 3.9 using scikit-learn, XGBoost, and SHAP libraries. A random seed of 42 was used throughout for reproducibility.

### 3.2 CHIRPS Validation

CHIRPS v2.0 monthly precipitation was validated against available BMKG rain gauge stations in Lampung for the period 2010–2023. For each station, the nearest CHIRPS grid cell was extracted and compared at the monthly scale. The following metrics were computed:

- **Pearson correlation coefficient (r)**: measures the linear association between CHIRPS and gauge data
- **Relative bias (%)**: systematic overestimation or underestimation, computed as (CHIRPS − gauge) / gauge × 100
- **Root mean square error (RMSE)**: overall magnitude of errors (mm/month)
- **Probability of Detection (POD)**: proportion of observed rain events correctly detected by CHIRPS
- **False Alarm Ratio (FAR)**: proportion of CHIRPS rain events not observed at the gauge

A rain/no-rain threshold of 1 mm/month was applied for categorical metrics.

### 3.3 Feature Engineering

Monthly CHIRPS data were spatially averaged for each coffee-producing district and temporally aggregated into the following feature groups:

**Precipitation features:**

- Total annual precipitation (mm)
- Seasonal totals: wet season (November–March), dry season (June–September), transition periods (April–May, October)
- Phenologically relevant periods: flowering phase (June–August), fruiting phase (September–November)
- Coefficient of variation (CV) of monthly precipitation within each year
- Number of wet months (precipitation > 100 mm)
- Previous year's annual and dry-season precipitation (lag-1 features)

**Drought indices:**

The Standardized Precipitation Index (SPI) was computed at 3-, 6-, and 12-month accumulation periods following the gamma distribution fitting approach of McKee et al. (1993). The baseline period 1981–2023 was used for parameter estimation. SPI values at the end of key phenological stages were extracted as features.

**Climate teleconnection indices:**

Annual mean and seasonal values of the Oceanic Niño Index (ONI) and Dipole Mode Index (DMI) were included to capture the influence of ENSO and IOD on local precipitation and coffee productivity.

**Additional features** *(pending data acquisition)*:

- ERA5-derived: mean annual temperature, maximum dry-season temperature, potential evapotranspiration (ET₀), mean relative humidity, climatic water deficit (ET₀ − precipitation)
- MODIS-derived: mean annual NDVI, minimum NDVI (stress indicator), NDVI anomaly
- Topographic: mean elevation and slope per district from SRTM DEM
- Non-climate control: harvested area (ha) as a proxy for management intensity

### 3.4 Machine Learning Models

Four regression models were evaluated, selected to span a range of complexities and learning paradigms suitable for small-sample settings (~14 provincial-level observations or ~70 district-level observations):

1. **Multiple Linear Regression (MLR)**: serves as the baseline model, assuming linear relationships between features and productivity.

2. **Random Forest (RF)**: an ensemble bagging method that constructs multiple decision trees on bootstrapped subsets. RF is robust to overfitting with small datasets due to its inherent averaging mechanism. Default configuration: 200 trees, maximum depth of 10, minimum 5 samples per leaf.

3. **Extreme Gradient Boosting (XGBoost)**: a regularized gradient boosting framework that builds trees sequentially, correcting errors of previous trees. XGBoost incorporates L1 and L2 regularization to mitigate overfitting. Default configuration: 200 boosting rounds, maximum depth of 5, learning rate of 0.1, L1 regularization (alpha) of 0.1.

4. **Support Vector Regression (SVR)**: a kernel-based method that finds the optimal hyperplane within an epsilon-insensitive tube. SVR is particularly suited for small sample sizes. A radial basis function (RBF) kernel was used with C = 10 and epsilon = 0.1. Features were standardized to zero mean and unit variance before SVR training.

### 3.5 Validation Strategy

Given the limited sample size and temporal structure of the data, Leave-One-Year-Out (LOYO) cross-validation was employed as the primary validation strategy. In each fold, data from one year were held out for testing while all remaining years were used for training. This approach respects the temporal ordering of the data and provides an unbiased estimate of prediction performance for unseen years.

For hyperparameter tuning, grid search was conducted within the LOYO cross-validation framework, with the mean R² across folds as the selection criterion.

A final hold-out test was reserved for the period 2021–2023 (3 years), with models developed exclusively on 2010–2020 data. This final evaluation was conducted exactly once to avoid data leakage and provide an independent estimate of generalization performance.

### 3.6 Evaluation Metrics

Model performance was assessed using four complementary metrics:

- **Coefficient of determination (R²)**: proportion of variance in productivity explained by the model. Target: R² > 0.70.
- **Root mean square error (RMSE)**: average magnitude of prediction errors in kg/ha.
- **Mean absolute error (MAE)**: average absolute deviation in kg/ha.
- **Mean absolute percentage error (MAPE)**: relative prediction error as a percentage of actual productivity. Target: MAPE < 15%.

### 3.7 Feature Importance and Interpretability

SHapley Additive exPlanations (SHAP) values were computed for the best-performing model to quantify the contribution of each feature to individual predictions. SHAP provides a unified measure of feature importance that is consistent, locally accurate, and based on cooperative game theory. Summary plots, dependence plots, and mean absolute SHAP values were used to identify the most influential climate drivers and their directional effects on coffee productivity.

### 3.8 Ablation Study

To assess the incremental contribution of different data sources, an ablation study was conducted by progressively adding feature groups:

1. CHIRPS precipitation features only
2. CHIRPS + ERA5 temperature/humidity features
3. CHIRPS + ERA5 + MODIS vegetation indices
4. CHIRPS + ERA5 + MODIS + climate teleconnection indices (ENSO, IOD)
5. Full feature set (all of the above + topographic + area harvested)

This analysis quantifies the standalone predictive value of CHIRPS and the marginal contribution of each additional data source.

### 3.9 Early Warning Framework

To evaluate the potential for seasonal forecasting, the best-performing model was retrained using only climate features available up to a specified lead time before the harvest period (typically March–May in Lampung). Lead-time experiments were conducted at 3, 4, 5, and 6 months before harvest, progressively restricting the input features to those available at each lead time. Model skill was assessed in terms of R² and the ability to correctly classify years as above-average or below-average productivity (binary classification accuracy, sensitivity, and specificity).

---

## 4. Results

*[To be written after data analysis is complete]*

### 4.1 CHIRPS Validation
### 4.2 Climate–Yield Relationships
### 4.3 Model Performance
### 4.4 Early Warning Application

---

## 5. Discussion

*[To be written after results]*

---

## 6. Conclusion

*[To be written last]*

---

## Acknowledgments

*[To be added]*

---

## References

*[See docs/references.bib — all entries verified via CrossRef API]*
