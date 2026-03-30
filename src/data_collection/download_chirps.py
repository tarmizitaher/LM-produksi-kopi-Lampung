"""
Download CHIRPS v2.0 monthly data and clip to Lampung bounding box.

Downloads global GeoTIFF, clips to Lampung, saves clipped version,
deletes global file to save disk space.
"""

import gzip
import os
import shutil
import sys
import urllib.request
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_CHIRPS, LAMPUNG_BBOX, ensure_dirs

import numpy as np
import rasterio
from rasterio.windows import from_bounds

BASE_URL = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/"
TEMP_DIR = RAW_CHIRPS / "_temp"


def download_and_clip_month(year: int, month: int) -> str:
    """Download one month of CHIRPS, clip to Lampung, save."""
    filename = f"chirps-v2.0.{year}.{month:02d}.tif.gz"
    out_filename = f"chirps_lampung_{year}_{month:02d}.tif"
    out_path = RAW_CHIRPS / out_filename

    # Skip if already exists
    if out_path.exists():
        return str(out_path)

    url = BASE_URL + filename
    gz_path = TEMP_DIR / filename
    tif_path = TEMP_DIR / filename.replace(".gz", "")

    try:
        # Download
        if not gz_path.exists():
            print(f"  Downloading {filename}...", end=" ", flush=True)
            urllib.request.urlretrieve(url, gz_path)
            size_mb = os.path.getsize(gz_path) / (1024 * 1024)
            print(f"({size_mb:.1f} MB)", end=" ", flush=True)
        else:
            print(f"  Using cached {filename}...", end=" ", flush=True)

        # Decompress
        with gzip.open(gz_path, "rb") as f_in:
            with open(tif_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Clip to Lampung
        with rasterio.open(tif_path) as src:
            window = from_bounds(
                LAMPUNG_BBOX["west"], LAMPUNG_BBOX["south"],
                LAMPUNG_BBOX["east"], LAMPUNG_BBOX["north"],
                src.transform,
            )
            data = src.read(1, window=window)
            transform = src.window_transform(window)

            with rasterio.open(
                out_path, "w",
                driver="GTiff",
                height=data.shape[0],
                width=data.shape[1],
                count=1,
                dtype=data.dtype,
                crs="EPSG:4326",
                transform=transform,
                nodata=-9999,
                compress="deflate",
            ) as dst:
                dst.write(data, 1)

        print(f"-> {out_filename} ({data.shape[0]}x{data.shape[1]})")

        # Cleanup temp files
        if tif_path.exists():
            os.remove(tif_path)
        if gz_path.exists():
            os.remove(gz_path)

        return str(out_path)

    except Exception as e:
        print(f"FAILED: {e}")
        # Cleanup on failure
        for p in [gz_path, tif_path]:
            if p.exists():
                os.remove(p)
        return None


def save_metadata(start_year: int, end_year: int, n_files: int) -> None:
    """Save dataset metadata."""
    meta = {
        "source": "CHC UCSB - CHIRPS v2.0",
        "url": BASE_URL,
        "download_date": datetime.now().strftime("%Y-%m-%d"),
        "description": "CHIRPS v2.0 monthly precipitation, clipped to Lampung bbox",
        "spatial_extent": LAMPUNG_BBOX,
        "temporal_extent": {"start": f"{start_year}-01", "end": f"{end_year}-12"},
        "format": "GeoTIFF (deflate compressed)",
        "resolution": "0.05 degrees (~5 km)",
        "units": "mm/month",
        "license": "Public domain",
        "n_files": n_files,
    }
    meta_path = RAW_CHIRPS / "chirps_metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"\nMetadata saved: {meta_path}")


def main(start_year: int = 1981, end_year: int = 2025) -> None:
    ensure_dirs()
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"CHIRPS v2.0 Monthly Download — Lampung")
    print(f"Period: {start_year}-{end_year}")
    print(f"Bbox: {LAMPUNG_BBOX}")
    print("=" * 60)

    total = 0
    failed = 0

    for year in range(start_year, end_year + 1):
        print(f"\n[{year}]")
        for month in range(1, 13):
            result = download_and_clip_month(year, month)
            if result:
                total += 1
            else:
                failed += 1

    # Cleanup temp dir
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    save_metadata(start_year, end_year, total)

    print(f"\n{'=' * 60}")
    print(f"Complete: {total} files downloaded, {failed} failed")
    print(f"Location: {RAW_CHIRPS}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download CHIRPS for Lampung")
    parser.add_argument("--start", type=int, default=1981, help="Start year")
    parser.add_argument("--end", type=int, default=2025, help="End year")
    args = parser.parse_args()
    main(args.start, args.end)
