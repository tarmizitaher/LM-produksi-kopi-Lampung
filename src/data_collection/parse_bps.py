"""
Parse official BPS CSV files downloaded from lampung.bps.go.id
into clean analysis-ready datasets.
"""

import os
import sys
import csv
import glob

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import RAW_BPS, ensure_dirs

BPS_DIR = "/Users/tarmizitaher/Documents/Dummy test/data/BPS"


def parse_kabupaten_data():
    """Parse per-kabupaten production and area data (2014-2022)."""

    all_produksi = []
    all_luas = []

    # Parse "Produksi Tanaman, YYYY.csv"
    for f in sorted(glob.glob(os.path.join(BPS_DIR, "Produksi Tanaman, *.csv"))):
        year = int(f.split(", ")[1].replace(".csv", ""))
        print(f"  Parsing produksi {year}...")

        df = pd.read_csv(f, header=None, skiprows=4, encoding="utf-8")
        # Column 0 = kabupaten, Column 1 = Kopi Robusta (ton)
        for _, row in df.iterrows():
            kab = str(row[0]).strip()
            if kab in ("", "nan", "Provinsi Lampung"):
                continue
            prod_str = str(row[1]).strip().replace(",", "").replace("-", "0")
            try:
                prod = int(float(prod_str))
            except ValueError:
                prod = 0
            all_produksi.append({
                "year": year,
                "kabupaten": kab,
                "produksi_ton": prod,
            })

    # Parse "Luas Areal Tanaman, YYYY.csv"
    for f in sorted(glob.glob(os.path.join(BPS_DIR, "Luas Areal Tanaman, *.csv"))):
        year = int(f.split(", ")[1].replace(".csv", ""))
        print(f"  Parsing luas {year}...")

        df = pd.read_csv(f, header=None, skiprows=4, encoding="utf-8")
        # Column 0 = kabupaten, Column 1 = Kopi Robusta (ha)
        for _, row in df.iterrows():
            kab = str(row[0]).strip()
            if kab in ("", "nan", "Provinsi Lampung"):
                continue
            luas_str = str(row[1]).strip().replace(",", "").replace("-", "0")
            try:
                luas = int(float(luas_str))
            except ValueError:
                luas = 0
            all_luas.append({
                "year": year,
                "kabupaten": kab,
                "luas_ha": luas,
            })

    # Merge produksi and luas
    df_prod = pd.DataFrame(all_produksi)
    df_luas = pd.DataFrame(all_luas)

    if df_prod.empty or df_luas.empty:
        print("  WARNING: No data parsed")
        return pd.DataFrame()

    merged = df_prod.merge(df_luas, on=["year", "kabupaten"], how="outer")
    merged["produktivitas_kg_ha"] = (
        (merged["produksi_ton"] * 1000 / merged["luas_ha"]).round(1)
        .where(merged["luas_ha"] > 0)
    )
    merged = merged.sort_values(["year", "kabupaten"]).reset_index(drop=True)

    return merged


def parse_provincial_data():
    """Parse provincial-level data (ribu ton / ribu ha) for 2020-2025."""

    records = []

    # Production files
    for f in sorted(glob.glob(os.path.join(BPS_DIR, "Produksi Perkebunan Rakyat*.csv"))):
        year = int(f.rstrip(".csv").split(", ")[-1])
        df = pd.read_csv(f, header=None, skiprows=0)
        for _, row in df.iterrows():
            name = str(row[0]).strip()
            if "Kopi" in name or "Coffee" in name:
                val_str = str(row[1]).strip().replace(",", ".")
                try:
                    prod_ribu_ton = float(val_str)
                    records.append({"year": year, "produksi_ribu_ton": prod_ribu_ton})
                except ValueError:
                    pass

    # Area files
    for f in sorted(glob.glob(os.path.join(BPS_DIR, "Luas Areal Tanaman Perkebunan Rakyat*.csv"))):
        year = int(f.rstrip(".csv").split(", ")[-1])
        df = pd.read_csv(f, header=None, skiprows=0)
        for _, row in df.iterrows():
            name = str(row[0]).strip()
            if "Kopi" in name or "Coffee" in name:
                val_str = str(row[1]).strip().replace(",", ".")
                try:
                    luas_ribu_ha = float(val_str)
                    # Find matching year in records
                    for r in records:
                        if r["year"] == year:
                            r["luas_ribu_ha"] = luas_ribu_ha
                except ValueError:
                    pass

    df = pd.DataFrame(records)
    if not df.empty:
        df["produksi_ton"] = (df["produksi_ribu_ton"] * 1000).astype(int)
        df["luas_ha"] = (df["luas_ribu_ha"] * 1000).astype(int)
        df["produktivitas_kg_ha"] = (df["produksi_ton"] * 1000 / df["luas_ha"]).round(1)

    return df


def main():
    ensure_dirs()

    print("=" * 60)
    print("Parsing BPS Data")
    print("=" * 60)

    # Per-kabupaten (2014-2022)
    print("\n[1] Per-kabupaten data (2014-2022)...")
    kab_df = parse_kabupaten_data()
    if not kab_df.empty:
        out = RAW_BPS / "bps_coffee_per_kabupaten_verified.csv"
        kab_df.to_csv(out, index=False)
        print(f"\n  Saved: {out}")
        print(f"  {len(kab_df)} records, {kab_df['year'].nunique()} years, {kab_df['kabupaten'].nunique()} kabupaten")
        print(f"\n  Provincial totals per year:")
        summary = kab_df.groupby("year").agg(
            total_produksi=("produksi_ton", "sum"),
            total_luas=("luas_ha", "sum"),
        ).reset_index()
        summary["produktivitas"] = (summary["total_produksi"] * 1000 / summary["total_luas"]).round(1)
        print(summary.to_string(index=False))

    # Provincial (2020-2025)
    print("\n[2] Provincial data (2020-2025)...")
    prov_df = parse_provincial_data()
    if not prov_df.empty:
        out = RAW_BPS / "bps_coffee_provincial_verified.csv"
        prov_df.to_csv(out, index=False)
        print(f"\n  Saved: {out}")
        print(prov_df.to_string(index=False))

    print(f"\n{'=' * 60}")
    print("BPS parsing complete!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
