"""
Download MODIS MOD13Q1 (16-day NDVI/EVI, 250m) for Lampung via ORNL DAAC API.

Uses the TESViS REST API: https://modis.ornl.gov/rst/api/v1/
No Earthdata login required for this API (public).
"""

import os
import sys
import csv
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_MODIS, ensure_dirs

BASE_URL = "https://modis.ornl.gov/rst/api/v1"

# Lampung coffee district centroids
POINTS = {
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
}


def get_dates(lat, lon):
    """Get all available MODIS dates for a location."""
    url = f"{BASE_URL}/MOD13Q1/dates?latitude={lat}&longitude={lon}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return data.get("dates", [])


def get_subset(lat, lon, start_date, end_date):
    """Get NDVI/EVI subset for a single date range (max 10 dates)."""
    url = (f"{BASE_URL}/MOD13Q1/subset?"
           f"latitude={lat}&longitude={lon}"
           f"&startDate={start_date}&endDate={end_date}"
           f"&kmAboveBelow=0&kmLeftRight=0")
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def download_all(start_year=2010, end_year=2023):
    """Download MODIS NDVI for all Lampung points, chunked by 8 dates per request."""
    ensure_dirs()

    all_rows = []

    for name, (lat, lon) in POINTS.items():
        print(f"\n  [{name}] ({lat}, {lon})")

        # Get available dates
        dates = get_dates(lat, lon)
        # Filter to study period
        filtered = [d for d in dates
                    if start_year <= int(d["calendar_date"][:4]) <= end_year]
        print(f"    {len(filtered)} dates in {start_year}-{end_year}")

        # Chunk into groups of 8 (API limit is 10)
        for i in range(0, len(filtered), 8):
            chunk = filtered[i:i+8]
            start_d = chunk[0]["modis_date"]
            end_d = chunk[-1]["modis_date"]

            try:
                data = get_subset(lat, lon, start_d, end_d)
                subset = data.get("subset", [])

                for entry in subset:
                    band = entry.get("band", "")
                    if band not in ("250m_16_days_NDVI", "250m_16_days_EVI"):
                        continue

                    cal_date = entry.get("calendar_date", "")
                    values = entry.get("data", [])
                    val = values[0] * 0.0001 if values else None  # scale factor

                    if val is not None and val > -0.2:
                        year = int(cal_date[:4])
                        month = int(cal_date[5:7])
                        band_name = "ndvi" if "NDVI" in band else "evi"

                        all_rows.append({
                            "kabupaten": name,
                            "year": year,
                            "month": month,
                            "date": cal_date,
                            "latitude": lat,
                            "longitude": lon,
                            "band": band_name,
                            "value": round(val, 4),
                        })

                time.sleep(0.5)  # Be nice to the API

            except urllib.error.HTTPError as e:
                print(f"    Error chunk {start_d}-{end_d}: {e.code}")
                time.sleep(2)
            except Exception as e:
                print(f"    Error: {e}")
                time.sleep(2)

        print(f"    Collected {sum(1 for r in all_rows if r['kabupaten'] == name)} records")

    # Save
    if all_rows:
        out_path = RAW_MODIS / "modis_ndvi_evi_lampung.csv"
        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "kabupaten", "year", "month", "date", "latitude", "longitude", "band", "value"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nSaved: {out_path} ({len(all_rows)} records)")

        meta = {
            "source": "NASA ORNL DAAC — MODIS MOD13Q1 v061",
            "api": BASE_URL,
            "download_date": datetime.now().strftime("%Y-%m-%d"),
            "variables": ["NDVI", "EVI"],
            "resolution": "250m, 16-day",
            "points": {k: {"lat": v[0], "lon": v[1]} for k, v in POINTS.items()},
            "temporal_extent": {"start": start_year, "end": end_year},
            "scale_factor": 0.0001,
        }
        with open(RAW_MODIS / "modis_metadata.json", "w") as f:
            json.dump(meta, f, indent=2)

    else:
        print("\nWARNING: No data collected.")

    return len(all_rows)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=2010)
    parser.add_argument("--end", type=int, default=2023)
    args = parser.parse_args()

    print("=" * 60)
    print(f"MODIS MOD13Q1 NDVI/EVI Download — Lampung ({args.start}-{args.end})")
    print("=" * 60)
    download_all(args.start, args.end)
