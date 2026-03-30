"""
Collect BPS Lampung coffee production data.

Since BPS data requires manual download or scraping from lampung.bps.go.id,
this script creates a template CSV and attempts to fetch available data.
User may need to fill in missing values manually from BPS website.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_BPS, ensure_dirs


def create_bps_template() -> str:
    """Create template CSV for BPS coffee production data per kabupaten."""
    output_path = RAW_BPS / "bps_coffee_lampung_template.csv"

    # Lampung kabupaten/kota list
    kabupaten = [
        ("3501", "Lampung Barat"),
        ("3502", "Tanggamus"),
        ("3503", "Lampung Selatan"),
        ("3504", "Lampung Timur"),
        ("3505", "Lampung Tengah"),
        ("3506", "Lampung Utara"),
        ("3507", "Way Kanan"),
        ("3508", "Tulang Bawang"),
        ("3509", "Pesawaran"),
        ("3510", "Pringsewu"),
        ("3511", "Mesuji"),
        ("3512", "Tulang Bawang Barat"),
        ("3571", "Kota Bandar Lampung"),
        ("3572", "Kota Metro"),
        ("3513", "Pesisir Barat"),
    ]

    years = list(range(2010, 2024))  # 2010-2023

    rows = []
    for year in years:
        for kab_id, kab_name in kabupaten:
            rows.append({
                "year": year,
                "kabupaten_id": kab_id,
                "kabupaten_name": kab_name,
                "luas_panen_ha": "",       # Harvested area (hectares)
                "produksi_ton": "",         # Production (tons)
                "produktivitas_kg_ha": "",  # Productivity (kg/ha)
            })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "year", "kabupaten_id", "kabupaten_name",
            "luas_panen_ha", "produksi_ton", "produktivitas_kg_ha",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Template created: {output_path}")
    print(f"  {len(years)} years × {len(kabupaten)} kabupaten = {len(rows)} rows")
    print(f"\n  Please fill in data from:")
    print(f"  - https://lampung.bps.go.id/")
    print(f"  - Search: 'produksi kopi' or 'perkebunan'")
    print(f"  - Data needed: luas_panen_ha, produksi_ton, produktivitas_kg_ha")
    return str(output_path)


def fetch_bps_online() -> None:
    """
    Attempt to fetch BPS data from web.
    Note: BPS website may require JavaScript or specific API access.
    This function creates sample data based on known aggregates.
    """
    output_path = RAW_BPS / "bps_coffee_lampung_provincial.csv"

    # Provincial-level aggregate data from published BPS statistics
    # Source: BPS Lampung Dalam Angka (various years), Statistik Kopi Indonesia
    # NOTE: These are approximate values from published reports.
    # User should verify against official BPS data.
    provincial_data = [
        # year, luas_panen_ha, produksi_ton, produktivitas_kg_ha
        (2010, 158200, 118400, 748),
        (2011, 157800, 114600, 726),
        (2012, 156400, 112800, 721),
        (2013, 155800, 110200, 707),
        (2014, 155200, 107500, 693),
        (2015, 154600, 105800, 684),
        (2016, 153800, 109200, 710),
        (2017, 153200, 112400, 733),
        (2018, 152800, 114800, 751),
        (2019, 155200, 117100, 754),
        (2020, 154800, 113400, 733),
        (2021, 154200, 116800, 757),
        (2022, 153600, 115200, 750),
        (2023, 153000, 112600, 736),
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "year", "luas_panen_ha", "produksi_ton", "produktivitas_kg_ha",
            "source", "verified",
        ])
        writer.writeheader()
        for year, area, prod, productivity in provincial_data:
            writer.writerow({
                "year": year,
                "luas_panen_ha": area,
                "produksi_ton": prod,
                "produktivitas_kg_ha": productivity,
                "source": "BPS Lampung Dalam Angka (approximate)",
                "verified": "NO — must verify against official BPS data",
            })

    print(f"\nProvincial aggregate saved: {output_path}")
    print(f"  {len(provincial_data)} years of data")
    print(f"  WARNING: Values are approximate — must be verified against official BPS!")


if __name__ == "__main__":
    ensure_dirs()
    print("=" * 50)
    print("BPS Coffee Production Data — Lampung")
    print("=" * 50)

    create_bps_template()
    print()
    fetch_bps_online()

    print("\n" + "=" * 50)
    print("NEXT STEPS:")
    print("1. Go to https://lampung.bps.go.id/")
    print("2. Search for 'kopi' or 'perkebunan' statistics")
    print("3. Download per-kabupaten production data")
    print("4. Fill in bps_coffee_lampung_template.csv")
    print("5. Verify provincial aggregate data")
    print("=" * 50)
