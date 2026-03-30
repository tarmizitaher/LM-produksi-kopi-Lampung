"""
Download ERA5 monthly averaged data for Lampung from Copernicus CDS.

Variables: 2m temperature, 2m dewpoint (for humidity), total precipitation,
           potential evaporation, surface solar radiation.

Requires: ~/.cdsapirc with valid API key
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_ERA5, LAMPUNG_BBOX, STUDY_PERIOD, ensure_dirs

import cdsapi


def download_era5_monthly(start_year: int = 2010, end_year: int = 2023) -> None:
    """Download ERA5 monthly averaged single-level data for Lampung."""
    ensure_dirs()

    client = cdsapi.Client()

    years = [str(y) for y in range(start_year, end_year + 1)]
    months = [f"{m:02d}" for m in range(1, 13)]

    # Lampung bbox: North, West, South, East
    area = [
        LAMPUNG_BBOX["north"],  # -3.5
        LAMPUNG_BBOX["west"],   # 103.5
        LAMPUNG_BBOX["south"],  # -6.0
        LAMPUNG_BBOX["east"],   # 106.0
    ]

    # Variables needed for our features
    variables = [
        "2m_temperature",
        "2m_dewpoint_temperature",
        "total_precipitation",
        "potential_evaporation",
        "surface_solar_radiation_downwards",
    ]

    out_path = RAW_ERA5 / f"era5_lampung_{start_year}_{end_year}_monthly.nc"

    if out_path.exists():
        print(f"Already exists: {out_path}")
        return

    print("=" * 60)
    print("Downloading ERA5 Monthly Data — Lampung")
    print(f"Period: {start_year}-{end_year}")
    print(f"Variables: {variables}")
    print(f"Area: {area}")
    print("=" * 60)
    print("\nThis may take several minutes...")

    client.retrieve(
        "reanalysis-era5-single-levels-monthly-means",
        {
            "product_type": "monthly_averaged_reanalysis",
            "variable": variables,
            "year": years,
            "month": months,
            "time": "00:00",
            "area": area,
            "data_format": "netcdf",
        },
        str(out_path),
    )

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\nSaved: {out_path} ({size_mb:.1f} MB)")

    # Save metadata
    meta = {
        "source": "Copernicus Climate Data Store — ERA5",
        "dataset": "reanalysis-era5-single-levels-monthly-means",
        "download_date": datetime.now().strftime("%Y-%m-%d"),
        "variables": variables,
        "spatial_extent": LAMPUNG_BBOX,
        "temporal_extent": {"start": f"{start_year}-01", "end": f"{end_year}-12"},
        "format": "NetCDF",
        "resolution": "0.25 degrees (~25 km)",
        "license": "Copernicus License",
    }
    meta_path = RAW_ERA5 / "era5_metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Metadata: {meta_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download ERA5 for Lampung")
    parser.add_argument("--start", type=int, default=2010)
    parser.add_argument("--end", type=int, default=2023)
    args = parser.parse_args()
    download_era5_monthly(args.start, args.end)
