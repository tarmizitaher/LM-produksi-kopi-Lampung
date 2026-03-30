"""
Download SRTM 30m DEM tiles for Lampung and extract elevation per kabupaten.

Uses NASA Earthdata for SRTM GL1 (30m) tiles.
Requires ~/.netrc with Earthdata credentials.
"""

import os
import sys
import json
import zipfile
import urllib.request
import urllib.error
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_BMKG, LAMPUNG_BBOX, ensure_dirs

DEM_DIR = RAW_BMKG.parent / "dem"

# SRTM tiles for Lampung bbox
TILES = [
    "S04E103", "S04E104", "S04E105",
    "S05E103", "S05E104", "S05E105",
    "S06E103", "S06E104", "S06E105",
]

KABUPATEN_COORDS = {
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


def download_srtm_tile(tile_name: str) -> str:
    """Download one SRTM tile from NASA Earthdata."""
    DEM_DIR.mkdir(parents=True, exist_ok=True)

    hgt_file = DEM_DIR / f"{tile_name}.hgt"
    if hgt_file.exists():
        print(f"  {tile_name}: already exists")
        return str(hgt_file)

    zip_file = DEM_DIR / f"{tile_name}.SRTMGL1.hgt.zip"
    url = f"https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/{tile_name}.SRTMGL1.hgt.zip"

    print(f"  Downloading {tile_name}...", end=" ", flush=True)
    try:
        urllib.request.urlretrieve(url, zip_file)
        # Unzip
        with zipfile.ZipFile(zip_file, "r") as z:
            z.extractall(DEM_DIR)
        os.remove(zip_file)
        size_kb = os.path.getsize(hgt_file) / 1024
        print(f"OK ({size_kb:.0f} KB)")
        return str(hgt_file)
    except urllib.error.HTTPError as e:
        print(f"FAILED: {e.code} {e.reason}")
        if zip_file.exists():
            os.remove(zip_file)
        return ""
    except Exception as e:
        print(f"FAILED: {e}")
        return ""


def read_srtm_hgt(filepath: str) -> tuple:
    """Read SRTM .hgt file and return (data, lat_range, lon_range)."""
    basename = os.path.basename(filepath).replace(".hgt", "")
    # Parse lat/lon from filename (e.g., S05E104)
    lat_sign = -1 if basename[0] == "S" else 1
    lat = lat_sign * int(basename[1:3])
    lon_sign = -1 if basename[3] == "W" else 1
    lon = lon_sign * int(basename[4:7])

    # SRTM GL1: 3601 x 3601 pixels per tile
    size = 3601
    data = np.fromfile(filepath, dtype=">i2").reshape((size, size))
    data = data.astype(np.float32)
    data[data == -32768] = np.nan  # nodata

    return data, lat, lon


def extract_elevation_per_kabupaten() -> dict:
    """Extract mean elevation for each kabupaten centroid (5km radius average)."""
    results = {}

    for kab_name, (klat, klon) in KABUPATEN_COORDS.items():
        # Determine which tile this point falls in
        tile_lat = -int(np.ceil(abs(klat)))
        tile_lon = int(np.floor(klon))
        tile_name = f"S{abs(tile_lat):02d}E{tile_lon:03d}"

        hgt_path = DEM_DIR / f"{tile_name}.hgt"
        if not hgt_path.exists():
            print(f"  {kab_name}: tile {tile_name} not found")
            results[kab_name] = {"elevation": np.nan, "slope": np.nan}
            continue

        data, base_lat, base_lon = read_srtm_hgt(str(hgt_path))

        # Convert lat/lon to pixel coordinates
        # SRTM: top-left is (base_lat+1, base_lon), resolution 1/3600 degree
        row = int((base_lat + 1 - klat) * 3600)
        col = int((klon - base_lon) * 3600)

        # Extract ~5km radius (approx 50 pixels at equator)
        r = 50
        r1, r2 = max(0, row - r), min(3600, row + r)
        c1, c2 = max(0, col - r), min(3600, col + r)
        patch = data[r1:r2, c1:c2]

        elev = float(np.nanmean(patch))
        # Compute slope from gradients
        dy, dx = np.gradient(patch, 30, 30)  # 30m pixel size
        slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
        mean_slope = float(np.nanmean(np.degrees(slope_rad)))

        results[kab_name] = {
            "elevation": round(elev, 1),
            "slope": round(mean_slope, 2),
        }
        print(f"  {kab_name}: elev={elev:.0f}m, slope={mean_slope:.1f}°")

    return results


def main():
    ensure_dirs()
    DEM_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SRTM DEM Download & Extraction — Lampung")
    print("=" * 60)

    # Download tiles
    print("\n[1] Downloading SRTM tiles...")
    for tile in TILES:
        download_srtm_tile(tile)

    # Extract elevations
    print("\n[2] Extracting elevation per kabupaten...")
    elevations = extract_elevation_per_kabupaten()

    # Save as CSV
    import csv
    out_path = DEM_DIR / "kabupaten_elevation.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["kabupaten", "elevation_m", "slope_deg"])
        writer.writeheader()
        for kab, vals in elevations.items():
            writer.writerow({
                "kabupaten": kab,
                "elevation_m": vals["elevation"],
                "slope_deg": vals["slope"],
            })
    print(f"\nSaved: {out_path}")

    # Metadata
    meta = {
        "source": "NASA SRTM GL1 (30m)",
        "download_date": datetime.now().strftime("%Y-%m-%d"),
        "tiles": TILES,
        "resolution": "30m (1 arc-second)",
        "extraction_method": "Mean within ~5km radius of kabupaten centroid",
    }
    with open(DEM_DIR / "dem_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("\nDone!")


if __name__ == "__main__":
    main()
