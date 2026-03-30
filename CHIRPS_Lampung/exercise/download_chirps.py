"""
Script untuk mengunduh dan memproses data CHIRPS v2.0 asli untuk wilayah Lampung.

Prasyarat:
    pip install rasterio numpy pandas

Penggunaan:
    python download_chirps.py

Catatan:
    - Mengunduh file GeoTIFF global (~14 MB per bulan) lalu mengekstrak wilayah Lampung
    - Memerlukan koneksi internet
    - Total download: ~196 MB (14 bulan x 14 MB)
"""

import os
import gzip
import shutil
import urllib.request
import sys

# Coba import library yang diperlukan
try:
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False
    print("WARNING: rasterio tidak terinstall.")
    print("Install dengan: pip install rasterio numpy")
    print()

# Konfigurasi
BASE_URL = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/"
LAMPUNG_BOUNDS = {
    "west": 103.5,
    "south": -6.0,
    "east": 106.0,
    "north": -3.5,
}
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp_downloads")


def download_file(url, dest):
    """Download file dengan progress indicator."""
    print(f"  Mengunduh: {os.path.basename(dest)}...", end=" ", flush=True)
    try:
        urllib.request.urlretrieve(url, dest)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"OK ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"GAGAL: {e}")
        return False


def extract_lampung(tif_path, year, month):
    """Ekstrak data Lampung dari GeoTIFF global."""
    if not HAS_RASTERIO:
        print("  Tidak bisa ekstrak tanpa rasterio. Lewati.")
        return None

    with rasterio.open(tif_path) as src:
        window = from_bounds(
            LAMPUNG_BOUNDS["west"],
            LAMPUNG_BOUNDS["south"],
            LAMPUNG_BOUNDS["east"],
            LAMPUNG_BOUNDS["north"],
            src.transform,
        )
        data = src.read(1, window=window)
        transform = src.window_transform(window)

    # Simpan sebagai GeoTIFF kecil
    out_path = os.path.join(OUTPUT_DIR, f"chirps_lampung_{year}_{month:02d}.tif")
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
    ) as dst:
        dst.write(data, 1)

    print(f"  Tersimpan: {os.path.basename(out_path)} ({data.shape[0]}x{data.shape[1]} pixels)")
    return out_path


def main():
    print("=" * 60)
    print("Download Data CHIRPS v2.0 - Wilayah Lampung")
    print("=" * 60)
    print(f"Wilayah: {LAMPUNG_BOUNDS}")
    print(f"Output : {OUTPUT_DIR}")
    print()

    if not HAS_RASTERIO:
        print("ERROR: Install rasterio terlebih dahulu:")
        print("  pip install rasterio numpy")
        sys.exit(1)

    os.makedirs(TEMP_DIR, exist_ok=True)

    periods = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 3)]

    for year, month in periods:
        filename = f"chirps-v2.0.{year}.{month:02d}.tif.gz"
        url = BASE_URL + filename
        gz_path = os.path.join(TEMP_DIR, filename)
        tif_path = gz_path.replace(".gz", "")

        print(f"\n[{year}-{month:02d}]")

        # Download
        if not os.path.exists(gz_path):
            if not download_file(url, gz_path):
                continue
        else:
            print(f"  Sudah ada: {filename}")

        # Decompress
        if not os.path.exists(tif_path):
            print("  Dekompresi...", end=" ", flush=True)
            with gzip.open(gz_path, "rb") as f_in:
                with open(tif_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("OK")

        # Extract Lampung
        extract_lampung(tif_path, year, month)

    # Cleanup
    print(f"\nFile temporary di: {TEMP_DIR}")
    response = input("Hapus file temporary? (y/n): ").strip().lower()
    if response == "y":
        shutil.rmtree(TEMP_DIR)
        print("File temporary dihapus.")

    print("\nSelesai!")


if __name__ == "__main__":
    main()
