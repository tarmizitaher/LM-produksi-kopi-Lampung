"""
Preprocessing pipeline: merge all data sources into analysis-ready dataset.

Usage:
    python -m src.preprocessing.pipeline

Input:
    - data/raw/chirps/        CHIRPS monthly GeoTIFFs (clipped to Lampung)
    - data/raw/bps/           BPS coffee production CSV
    - data/external/          ENSO Nino 3.4 + IOD DMI indices
    (future: ERA5, MODIS, DEM)

Output:
    - data/processed/analysis_dataset.csv
"""

import os
import sys
import glob
import json

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import (
    ROOT, RAW_CHIRPS, RAW_BPS, RAW_ERA5, RAW_MODIS, RAW_BMKG,
    EXTERNAL_DIR, INTERIM_DIR, PROCESSED_DIR, LAMPUNG_BBOX,
    STUDY_PERIOD, SPI_BASELINE, RANDOM_STATE, ensure_dirs,
)
from configs.features import SEASONS


# =====================================================================
# Step 1: Extract CHIRPS time series per kabupaten
# =====================================================================

def extract_chirps_kabupaten(kabupaten_coords: dict[str, tuple]) -> pd.DataFrame:
    """
    Extract monthly CHIRPS precipitation for each kabupaten centroid.

    Args:
        kabupaten_coords: dict of {name: (lat, lon)}

    Returns:
        DataFrame with columns: year, month, kabupaten, precipitation_mm
    """
    try:
        import rasterio
    except ImportError:
        print("WARNING: rasterio not installed. Skipping CHIRPS extraction.")
        return pd.DataFrame()

    tif_files = sorted(glob.glob(str(RAW_CHIRPS / "chirps_lampung_*.tif")))
    if not tif_files:
        print("WARNING: No CHIRPS files found in", RAW_CHIRPS)
        return pd.DataFrame()

    rows = []
    for tif_path in tif_files:
        basename = os.path.basename(tif_path)
        # Parse year and month from filename: chirps_lampung_YYYY_MM.tif
        parts = basename.replace(".tif", "").split("_")
        year, month = int(parts[2]), int(parts[3])

        with rasterio.open(tif_path) as src:
            for kab_name, (lat, lon) in kabupaten_coords.items():
                try:
                    row_idx, col_idx = src.index(lon, lat)
                    value = src.read(1)[row_idx, col_idx]
                    if value < 0:  # nodata
                        value = np.nan
                    rows.append({
                        "year": year, "month": month,
                        "kabupaten": kab_name,
                        "precipitation_mm": round(float(value), 2),
                    })
                except (IndexError, ValueError):
                    rows.append({
                        "year": year, "month": month,
                        "kabupaten": kab_name,
                        "precipitation_mm": np.nan,
                    })

    df = pd.DataFrame(rows)
    print(f"  CHIRPS extracted: {len(df)} records ({len(tif_files)} months × {len(kabupaten_coords)} kabupaten)")
    return df


# =====================================================================
# Step 2: Compute CHIRPS features (seasonal, SPI, etc.)
# =====================================================================

def compute_chirps_features(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly CHIRPS to annual features per kabupaten."""
    if monthly_df.empty:
        return pd.DataFrame()

    features = []

    for (kab, year), grp in monthly_df.groupby(["kabupaten", "year"]):
        if len(grp) < 12:
            continue  # Skip incomplete years

        month_precip = grp.set_index("month")["precipitation_mm"]

        feat = {"kabupaten": kab, "year": year}

        # Annual total
        feat["precip_annual"] = month_precip.sum()

        # Seasonal totals
        for season_name, months in SEASONS.items():
            vals = month_precip.reindex(months).dropna()
            feat[f"precip_{season_name}"] = vals.sum()

        # Variability
        feat["precip_cv"] = month_precip.std() / month_precip.mean() if month_precip.mean() > 0 else np.nan

        # Rainy days proxy: months with > 100mm
        feat["wet_months"] = (month_precip > 100).sum()

        features.append(feat)

    df = pd.DataFrame(features)
    print(f"  CHIRPS features: {len(df)} records")
    return df


def compute_spi(monthly_df: pd.DataFrame, scale: int = 3) -> pd.DataFrame:
    """
    Compute Standardized Precipitation Index (SPI) at given scale.
    Uses gamma distribution fitting on the full CHIRPS record.
    """
    if monthly_df.empty:
        return pd.DataFrame()

    from scipy.stats import gamma as gamma_dist

    results = []

    for kab, kab_df in monthly_df.groupby("kabupaten"):
        kab_df = kab_df.sort_values(["year", "month"])

        # Rolling sum for the given scale
        kab_df = kab_df.copy()
        kab_df["rolling_precip"] = kab_df["precipitation_mm"].rolling(scale, min_periods=scale).sum()

        for month in range(1, 13):
            month_data = kab_df[kab_df["month"] == month]["rolling_precip"].dropna()
            if len(month_data) < 10:
                continue

            # Fit gamma distribution
            positive = month_data[month_data > 0]
            if len(positive) < 5:
                continue

            try:
                shape, loc, scale_param = gamma_dist.fit(positive, floc=0)
                # Probability of zero
                q = 1 - len(positive) / len(month_data)

                for idx, row in kab_df[kab_df["month"] == month].iterrows():
                    if pd.isna(row["rolling_precip"]):
                        continue
                    if row["rolling_precip"] <= 0:
                        prob = q
                    else:
                        prob = q + (1 - q) * gamma_dist.cdf(row["rolling_precip"], shape, loc=0, scale=scale_param)

                    # Convert to standard normal
                    from scipy.stats import norm
                    spi_val = norm.ppf(max(0.001, min(prob, 0.999)))

                    results.append({
                        "year": row["year"], "month": row["month"],
                        "kabupaten": kab,
                        f"spi_{scale}": round(spi_val, 3),
                    })
            except Exception:
                continue

    df = pd.DataFrame(results)
    print(f"  SPI-{scale}: {len(df)} records")
    return df


# =====================================================================
# Step 3: Load climate indices
# =====================================================================

def load_climate_indices() -> pd.DataFrame:
    """Load and merge ENSO and IOD monthly indices."""
    nino_path = EXTERNAL_DIR / "nino34_monthly.csv"
    dmi_path = EXTERNAL_DIR / "iod_dmi_monthly.csv"

    dfs = []

    if nino_path.exists():
        nino = pd.read_csv(nino_path)
        nino_annual = nino.groupby("year").agg(
            nino34_annual=("oni", "mean"),
            nino34_djf=("oni", lambda x: x.iloc[0] if len(x) >= 1 else np.nan),  # DJF
        ).reset_index()
        dfs.append(nino_annual)
        print(f"  ENSO loaded: {len(nino_annual)} years")

    if dmi_path.exists():
        dmi = pd.read_csv(dmi_path)
        dmi_annual = dmi.groupby("year").agg(
            dmi_annual=("dmi", "mean"),
            dmi_jjas=("dmi", lambda x: x[(x.index >= 5) & (x.index <= 8)].mean()
                      if len(x) >= 9 else x.mean()),
        ).reset_index()
        dfs.append(dmi_annual)
        print(f"  IOD loaded: {len(dmi_annual)} years")

    if dfs:
        merged = dfs[0]
        for df in dfs[1:]:
            merged = merged.merge(df, on="year", how="outer")
        return merged

    return pd.DataFrame()


# =====================================================================
# Step 4: Load BPS target variable
# =====================================================================

def load_bps_data() -> pd.DataFrame:
    """Load BPS coffee production data. Prefer per-kabupaten verified data."""
    kab_verified = RAW_BPS / "bps_coffee_per_kabupaten_verified.csv"
    prov_path = RAW_BPS / "bps_coffee_lampung_provincial.csv"

    if kab_verified.exists():
        df = pd.read_csv(kab_verified)
        df = df.rename(columns={"luas_ha": "luas_panen_ha"})
        print(f"  BPS per-kabupaten loaded: {len(df)} records ({df['year'].nunique()} years × {df['kabupaten'].nunique()} kabupaten)")
        return df

    if prov_path.exists():
        df = pd.read_csv(prov_path)
        df = df[["year", "luas_panen_ha", "produksi_ton", "produktivitas_kg_ha"]]
        print(f"  BPS provincial loaded: {len(df)} years")
        return df

    print("  WARNING: No BPS data found")
    return pd.DataFrame()


# =====================================================================
# Step 4b: Load ERA5 features
# =====================================================================

def load_era5_features(kabupaten_coords: dict) -> pd.DataFrame:
    """Extract ERA5 features per kabupaten."""
    era5_dir = RAW_ERA5
    nc_files = list(era5_dir.glob("data_stream-*.nc"))
    if not nc_files:
        print("  WARNING: No ERA5 files found")
        return pd.DataFrame()

    try:
        import netCDF4
    except ImportError:
        print("  WARNING: netCDF4 not installed")
        return pd.DataFrame()

    rows = []

    # Load temperature and dewpoint
    t_file = era5_dir / "data_stream-moda_stepType-avgua.nc"
    p_file = era5_dir / "data_stream-moda_stepType-avgad.nc"

    if not t_file.exists() or not p_file.exists():
        print("  WARNING: ERA5 NC files not found")
        return pd.DataFrame()

    ds_t = netCDF4.Dataset(str(t_file))
    ds_p = netCDF4.Dataset(str(p_file))

    times = netCDF4.num2date(ds_t.variables["valid_time"][:],
                             ds_t.variables["valid_time"].units)
    lats = ds_t.variables["latitude"][:]
    lons = ds_t.variables["longitude"][:]

    t2m = ds_t.variables["t2m"][:]  # Kelvin
    d2m = ds_t.variables["d2m"][:]  # Kelvin
    tp = ds_p.variables["tp"][:]    # m (total precip)
    pev = ds_p.variables["pev"][:]  # m (potential evaporation, negative)
    ssrd = ds_p.variables["ssrd"][:]  # J/m2

    for kab_name, (klat, klon) in kabupaten_coords.items():
        # Find nearest grid cell
        lat_idx = np.argmin(np.abs(lats - klat))
        lon_idx = np.argmin(np.abs(lons - klon))

        for t_idx, time_val in enumerate(times):
            year = time_val.year if hasattr(time_val, 'year') else int(str(time_val)[:4])
            month = time_val.month if hasattr(time_val, 'month') else int(str(time_val)[5:7])

            temp_k = float(t2m[t_idx, lat_idx, lon_idx])
            dewp_k = float(d2m[t_idx, lat_idx, lon_idx])
            precip_m = float(tp[t_idx, lat_idx, lon_idx])
            evap_m = float(pev[t_idx, lat_idx, lon_idx])
            solar = float(ssrd[t_idx, lat_idx, lon_idx])

            rows.append({
                "kabupaten": kab_name,
                "year": year,
                "month": month,
                "temp_c": round(temp_k - 273.15, 2),
                "dewpoint_c": round(dewp_k - 273.15, 2),
                "era5_precip_mm": round(precip_m * 1000, 2),
                "pot_evap_mm": round(abs(evap_m) * 1000, 2),
                "solar_rad_mj": round(solar / 1e6, 2),
            })

    ds_t.close()
    ds_p.close()

    df = pd.DataFrame(rows)

    # Compute relative humidity from temp and dewpoint (Magnus formula)
    df["rh_pct"] = (100 * np.exp(17.625 * df["dewpoint_c"] / (243.04 + df["dewpoint_c"]))
                    / np.exp(17.625 * df["temp_c"] / (243.04 + df["temp_c"]))).round(1)

    print(f"  ERA5 extracted: {len(df)} records ({df['year'].nunique()} years × {df['kabupaten'].nunique()} kabupaten)")
    return df


def compute_era5_annual(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly ERA5 to annual features per kabupaten."""
    if monthly_df.empty:
        return pd.DataFrame()

    from configs.features import SEASONS

    features = []
    for (kab, year), grp in monthly_df.groupby(["kabupaten", "year"]):
        if len(grp) < 12:
            continue
        m = grp.set_index("month")
        feat = {"kabupaten": kab, "year": year}
        feat["temp_mean_annual"] = m["temp_c"].mean().round(2)
        # Max temp in dry season
        dry_months = SEASONS.get("dry", [6, 7, 8, 9])
        dry = m.loc[m.index.isin(dry_months)]
        feat["temp_max_dry"] = dry["temp_c"].max().round(2) if len(dry) > 0 else np.nan
        feat["et0_annual"] = m["pot_evap_mm"].sum().round(1)
        feat["humidity_mean"] = m["rh_pct"].mean().round(1)
        feat["solar_rad_annual"] = m["solar_rad_mj"].sum().round(1)
        features.append(feat)

    df = pd.DataFrame(features)
    print(f"  ERA5 features: {len(df)} records")
    return df


# =====================================================================
# Step 5: Merge everything
# =====================================================================

def merge_dataset(
    chirps_features: pd.DataFrame,
    climate_indices: pd.DataFrame,
    bps_data: pd.DataFrame,
    era5_features: pd.DataFrame = None,
) -> pd.DataFrame:
    """Merge all features with target variable."""
    if bps_data.empty:
        print("  ERROR: No BPS data to merge")
        return pd.DataFrame()

    df = bps_data.copy()
    has_kabupaten = "kabupaten" in df.columns

    # Merge keys
    merge_keys = ["year", "kabupaten"] if has_kabupaten else ["year"]

    # Merge climate indices (year-level, same for all kabupaten)
    if not climate_indices.empty:
        df = df.merge(climate_indices, on="year", how="left")

    # Merge CHIRPS features
    if not chirps_features.empty:
        if has_kabupaten:
            df = df.merge(chirps_features, on=merge_keys, how="left")
        else:
            chirps_annual = chirps_features.groupby("year").mean(numeric_only=True).reset_index()
            df = df.merge(chirps_annual, on="year", how="left")

    # Merge ERA5 features
    if era5_features is not None and not era5_features.empty:
        if has_kabupaten:
            df = df.merge(era5_features, on=merge_keys, how="left")
        else:
            era5_annual = era5_features.groupby("year").mean(numeric_only=True).reset_index()
            df = df.merge(era5_annual, on="year", how="left")

    # Add lag features per kabupaten
    if has_kabupaten:
        lag_cols = ["precip_annual", "precip_dry", "precip_wet"]
        for col in lag_cols:
            if col in df.columns:
                df[f"{col}_lag1"] = df.groupby("kabupaten")[col].shift(1)
    else:
        for col in ["precip_annual", "precip_dry", "precip_wet"]:
            if col in df.columns:
                df[f"{col}_lag1"] = df[col].shift(1)

    # Compute water deficit if possible
    if "et0_annual" in df.columns and "precip_annual" in df.columns:
        df["water_deficit"] = (df["et0_annual"] - df["precip_annual"]).round(1)

    # Filter to study period
    df = df[
        (df["year"] >= STUDY_PERIOD["start"]) &
        (df["year"] <= STUDY_PERIOD["end"])
    ].reset_index(drop=True)

    print(f"  Merged dataset: {len(df)} rows × {len(df.columns)} columns")
    return df


# =====================================================================
# Main Pipeline
# =====================================================================

def main():
    ensure_dirs()

    print("=" * 60)
    print("Preprocessing Pipeline")
    print("=" * 60)

    # Kabupaten centroids (approximate)
    kabupaten_coords = {
        "Lampung Barat": (-5.02, 104.06),
        "Tanggamus": (-5.42, 104.63),
        "Lampung Utara": (-4.83, 104.88),
        "Way Kanan": (-4.65, 104.50),
        "Pesisir Barat": (-5.20, 103.95),
        "Lampung Selatan": (-5.72, 105.62),
        "Lampung Timur": (-4.75, 105.50),
        "Lampung Tengah": (-4.90, 105.20),
        "Pringsewu": (-5.36, 104.97),
        "Pesawaran": (-5.52, 105.08),
        "Bandar Lampung": (-5.45, 105.26),
        "Metro": (-5.11, 105.31),
        "Mesuji": (-4.10, 105.40),
        "Tulang Bawang": (-4.30, 105.45),
        "Tulang Bawang Barat": (-4.45, 105.10),
    }

    # Step 1: Extract CHIRPS
    print("\n[Step 1] Extracting CHIRPS time series...")
    chirps_monthly = extract_chirps_kabupaten(kabupaten_coords)
    if not chirps_monthly.empty:
        chirps_monthly.to_csv(INTERIM_DIR / "chirps_monthly_kabupaten.csv", index=False)

    # Step 2: Compute features
    print("\n[Step 2] Computing CHIRPS features...")
    chirps_features = compute_chirps_features(chirps_monthly)
    if not chirps_features.empty:
        chirps_features.to_csv(INTERIM_DIR / "chirps_features.csv", index=False)

    # Step 2b: Compute SPI (if enough data)
    print("\n[Step 2b] Computing SPI...")
    if not chirps_monthly.empty and len(chirps_monthly["year"].unique()) >= 20:
        for scale in [3, 6, 12]:
            spi = compute_spi(chirps_monthly, scale=scale)
            if not spi.empty:
                spi.to_csv(INTERIM_DIR / f"spi_{scale}_monthly.csv", index=False)
    else:
        print("  Skipped: need 20+ years of CHIRPS for SPI baseline")

    # Step 3: Climate indices
    print("\n[Step 3] Loading climate indices...")
    climate_indices = load_climate_indices()

    # Step 2c: Aggregate SPI to annual features per kabupaten
    print("\n[Step 2c] Computing annual SPI features...")
    spi_features = pd.DataFrame()
    for scale in [3, 6, 12]:
        spi_path = INTERIM_DIR / f"spi_{scale}_monthly.csv"
        if spi_path.exists():
            spi_monthly = pd.read_csv(spi_path)
            # For each kabupaten-year, get SPI at end of key months
            # Jun (6) = start flowering, Sep (9) = end flowering, Dec (12) = end year
            for month_target, suffix in [(6, "jun"), (9, "sep"), (12, "dec")]:
                month_spi = spi_monthly[spi_monthly["month"] == month_target][["year", "kabupaten", f"spi_{scale}"]]
                month_spi = month_spi.rename(columns={f"spi_{scale}": f"spi{scale}_{suffix}"})
                if spi_features.empty:
                    spi_features = month_spi
                else:
                    spi_features = spi_features.merge(month_spi, on=["year", "kabupaten"], how="outer")
    if not spi_features.empty:
        spi_features.to_csv(INTERIM_DIR / "spi_annual_features.csv", index=False)
        print(f"  SPI features: {len(spi_features)} records, {len(spi_features.columns)-2} features")
    else:
        print("  No SPI features computed")

    # Step 2d: MODIS NDVI/EVI features
    print("\n[Step 2d] Computing MODIS features...")
    modis_path = RAW_MODIS / "modis_ndvi_evi_lampung.csv"
    modis_features = pd.DataFrame()
    if modis_path.exists():
        modis_raw = pd.read_csv(modis_path)
        # Pivot to get ndvi and evi as separate columns per observation
        ndvi_data = modis_raw[modis_raw["band"] == "ndvi"].copy()
        evi_data = modis_raw[modis_raw["band"] == "evi"].copy()

        # Aggregate to monthly mean per kabupaten
        ndvi_monthly = ndvi_data.groupby(["kabupaten", "year", "month"]).agg(ndvi=("value", "mean")).reset_index()
        evi_monthly = evi_data.groupby(["kabupaten", "year", "month"]).agg(evi=("value", "mean")).reset_index()

        # Aggregate to annual features per kabupaten
        modis_rows = []
        for (kab, year), grp in ndvi_monthly.groupby(["kabupaten", "year"]):
            feat = {"kabupaten": kab, "year": year}
            feat["ndvi_mean_annual"] = round(grp["ndvi"].mean(), 4)
            feat["ndvi_min"] = round(grp["ndvi"].min(), 4)
            feat["ndvi_max"] = round(grp["ndvi"].max(), 4)
            feat["ndvi_std"] = round(grp["ndvi"].std(), 4)
            # NDVI anomaly = mean - long-term mean for this kabupaten
            long_term = ndvi_monthly[ndvi_monthly["kabupaten"] == kab]["ndvi"].mean()
            feat["ndvi_anomaly"] = round(grp["ndvi"].mean() - long_term, 4)

            # EVI
            evi_grp = evi_monthly[(evi_monthly["kabupaten"] == kab) & (evi_monthly["year"] == year)]
            if not evi_grp.empty:
                feat["evi_mean_annual"] = round(evi_grp["evi"].mean(), 4)
                feat["evi_min"] = round(evi_grp["evi"].min(), 4)

            modis_rows.append(feat)

        modis_features = pd.DataFrame(modis_rows)
        modis_features.to_csv(INTERIM_DIR / "modis_features.csv", index=False)
        print(f"  MODIS features: {len(modis_features)} records, {len(modis_features.columns)-2} features")
    else:
        print("  WARNING: No MODIS data found")

    # Step 4: BPS data
    print("\n[Step 4] Loading BPS data...")
    bps_data = load_bps_data()

    # Step 4b: ERA5
    print("\n[Step 4b] Loading ERA5 data...")
    era5_monthly = load_era5_features(kabupaten_coords)
    era5_features = pd.DataFrame()
    if not era5_monthly.empty:
        era5_monthly.to_csv(INTERIM_DIR / "era5_monthly_kabupaten.csv", index=False)
        era5_features = compute_era5_annual(era5_monthly)
        if not era5_features.empty:
            era5_features.to_csv(INTERIM_DIR / "era5_features.csv", index=False)

    # Step 4c: DEM elevation
    print("\n[Step 4c] Loading DEM elevation...")
    dem_path = ROOT / "data" / "raw" / "dem" / "kabupaten_elevation.csv"
    elev_df = pd.DataFrame()
    if dem_path.exists():
        elev_df = pd.read_csv(dem_path)
        print(f"  Elevation loaded: {len(elev_df)} kabupaten")
    else:
        print("  WARNING: No elevation data found")

    # Step 5: Merge
    print("\n[Step 5] Merging dataset...")
    dataset = merge_dataset(chirps_features, climate_indices, bps_data, era5_features)

    # Add MODIS features
    if not dataset.empty and not modis_features.empty and "kabupaten" in dataset.columns:
        dataset = dataset.merge(modis_features, on=["year", "kabupaten"], how="left")
        ndvi_cols = [c for c in dataset.columns if "ndvi" in c or "evi" in c]
        print(f"  + MODIS added: {len(ndvi_cols)} features, {dataset['ndvi_mean_annual'].notna().sum()} matches")

    # Add SPI features
    if not dataset.empty and not spi_features.empty and "kabupaten" in dataset.columns:
        dataset = dataset.merge(spi_features, on=["year", "kabupaten"], how="left")
        spi_cols = [c for c in dataset.columns if c.startswith("spi")]
        print(f"  + SPI added: {len(spi_cols)} features")

    # Add elevation (static feature)
    if not dataset.empty and not elev_df.empty and "kabupaten" in dataset.columns:
        # Drop any existing elevation columns before merge
        for col in elev_df.columns:
            if col != "kabupaten" and col in dataset.columns:
                dataset = dataset.drop(columns=[col])
        dataset = dataset.merge(elev_df, on="kabupaten", how="left")
        print(f"  + Elevation added: {dataset['elevation_m'].notna().sum()} matches")

    if not dataset.empty:
        out_path = PROCESSED_DIR / "analysis_dataset.csv"
        dataset.to_csv(out_path, index=False)
        print(f"\n  Saved: {out_path}")
        print(f"\n  Columns: {list(dataset.columns)}")
        print(f"\n  Preview:")
        print(dataset.head().to_string())

    print(f"\n{'=' * 60}")
    print("Pipeline complete!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
