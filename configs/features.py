"""
Feature definitions and configurations for the ML pipeline.
"""

# CHIRPS-derived features
CHIRPS_FEATURES = [
    "precip_annual",          # Total annual precipitation (mm)
    "precip_wet_season",      # Wet season Nov-Mar (mm)
    "precip_dry_season",      # Dry season Jun-Sep (mm)
    "precip_flowering",       # Flowering phase Jun-Aug (mm)
    "precip_fruiting",        # Fruiting phase Sep-Nov (mm)
    "dry_spell_max",          # Longest consecutive dry days
    "rainy_days",             # Days with >1mm rain per year
    "spi_3",                  # 3-month SPI
    "spi_6",                  # 6-month SPI
    "spi_12",                 # 12-month SPI
    "precip_cv",              # Intra-annual CV of monthly precip
    "precip_lag1yr",          # Previous year's total precip
]

# ERA5-derived features
ERA5_FEATURES = [
    "temp_mean_annual",       # Mean annual temperature (°C)
    "temp_max_dry",           # Max temp during dry season (°C)
    "et0_annual",             # Annual potential evapotranspiration (mm)
    "humidity_mean",          # Mean relative humidity (%)
    "water_deficit",          # ET0 - Precipitation (mm)
]

# MODIS-derived features
MODIS_FEATURES = [
    "ndvi_mean_annual",       # Mean annual NDVI
    "ndvi_min",               # Minimum NDVI (stress indicator)
    "ndvi_anomaly",           # NDVI anomaly from long-term mean
    "evi_mean_growing",       # Mean EVI during growing season
]

# Climate index features
CLIMATE_INDEX_FEATURES = [
    "nino34",                 # ENSO Nino 3.4 index (annual mean)
    "dmi",                    # Indian Ocean Dipole Mode Index
]

# Static features
STATIC_FEATURES = [
    "elevation",              # Mean elevation (m)
    "slope",                  # Mean slope (degrees)
    "area_harvested",         # Harvested area (ha) — non-climate control
]

# Target variable
TARGET = "productivity_kg_per_ha"

# All features combined
ALL_FEATURES = (
    CHIRPS_FEATURES
    + ERA5_FEATURES
    + MODIS_FEATURES
    + CLIMATE_INDEX_FEATURES
    + STATIC_FEATURES
)

# Feature subsets for ablation study
FEATURE_SETS = {
    "chirps_only": CHIRPS_FEATURES,
    "chirps_era5": CHIRPS_FEATURES + ERA5_FEATURES,
    "chirps_era5_modis": CHIRPS_FEATURES + ERA5_FEATURES + MODIS_FEATURES,
    "all_climate": CHIRPS_FEATURES + ERA5_FEATURES + MODIS_FEATURES + CLIMATE_INDEX_FEATURES,
    "full": ALL_FEATURES,
}

# Seasonal month definitions (for Lampung tropical climate)
SEASONS = {
    "wet": [11, 12, 1, 2, 3],
    "dry": [6, 7, 8, 9],
    "transition_1": [4, 5],
    "transition_2": [10],
    "flowering": [6, 7, 8],
    "fruiting": [9, 10, 11],
}
