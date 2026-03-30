"""Download ENSO Nino 3.4 and IOD DMI indices from NOAA."""

import urllib.request
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import EXTERNAL_DIR, ensure_dirs


def download_nino34() -> str:
    """Download monthly Nino 3.4 index from NOAA CPC."""
    url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
    out_path = EXTERNAL_DIR / "nino34_oni.txt"
    print(f"Downloading Nino 3.4 (ONI) from NOAA CPC...")
    urllib.request.urlretrieve(url, out_path)
    print(f"  Saved: {out_path} ({os.path.getsize(out_path)} bytes)")
    return str(out_path)


def download_dmi() -> str:
    """Download monthly DMI (IOD) index from NOAA PSL."""
    url = "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data"
    out_path = EXTERNAL_DIR / "iod_dmi.txt"
    print(f"Downloading IOD DMI from NOAA PSL...")
    urllib.request.urlretrieve(url, out_path)
    print(f"  Saved: {out_path} ({os.path.getsize(out_path)} bytes)")
    return str(out_path)


def parse_nino34_to_csv() -> str:
    """Parse NOAA ONI text file to clean CSV."""
    input_path = EXTERNAL_DIR / "nino34_oni.txt"
    output_path = EXTERNAL_DIR / "nino34_monthly.csv"

    rows = []
    with open(input_path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    season = parts[0]
                    year = int(parts[1])
                    anom = float(parts[3])
                    # Map season (DJF, JFM, ...) to month
                    season_to_month = {
                        "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4,
                        "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8,
                        "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12,
                    }
                    if season in season_to_month:
                        rows.append({
                            "year": year, "month": season_to_month[season],
                            "season": season, "oni": anom,
                        })
                except (ValueError, IndexError):
                    continue

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "month", "season", "oni"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Parsed: {output_path} ({len(rows)} records)")
    return str(output_path)


def parse_dmi_to_csv() -> str:
    """Parse NOAA PSL DMI data to clean CSV."""
    input_path = EXTERNAL_DIR / "iod_dmi.txt"
    output_path = EXTERNAL_DIR / "iod_dmi_monthly.csv"

    rows = []
    with open(input_path) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) == 13:
                try:
                    year = int(parts[0])
                    if 1900 <= year <= 2030:
                        for month_idx in range(12):
                            val = float(parts[month_idx + 1])
                            if val > -90:  # Skip missing values
                                rows.append({
                                    "year": year,
                                    "month": month_idx + 1,
                                    "dmi": val,
                                })
                except (ValueError, IndexError):
                    continue

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "month", "dmi"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Parsed: {output_path} ({len(rows)} records)")
    return str(output_path)


if __name__ == "__main__":
    ensure_dirs()
    print("=" * 50)
    print("Downloading Climate Indices")
    print("=" * 50)

    download_nino34()
    parse_nino34_to_csv()
    print()
    download_dmi()
    parse_dmi_to_csv()

    print("\nDone!")
