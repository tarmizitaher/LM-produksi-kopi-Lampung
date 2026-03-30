# Data CHIRPS Lampung 2025-2026

## Tentang Dataset
Dataset ini berisi contoh data curah hujan bulanan dari **CHIRPS v2.0** (Climate Hazards Group InfraRed Precipitation with Station data) untuk wilayah **Provinsi Lampung, Indonesia**.

## Cakupan Wilayah
- **Bounding Box:** 103.5°E - 106.0°E, 3.5°S - 6.0°S
- **Resolusi Spasial:** 0.05° x 0.05° (~5 km)
- **Titik Grid:** 10 lokasi representatif di Lampung

## Periode Data
- Januari 2025 - Februari 2026 (14 bulan)

## File yang Tersedia

| File | Deskripsi |
|------|-----------|
| `chirps_lampung_monthly_2025_2026.csv` | Data curah hujan bulanan per titik grid |
| `chirps_lampung_summary.csv` | Ringkasan statistik per bulan |
| `chirps_lampung_stations.csv` | Informasi lokasi titik grid |
| `download_chirps.py` | Script Python untuk mengunduh data CHIRPS asli |

## Satuan
- Curah hujan: **mm/bulan** (milimeter per bulan)

## Sumber Data
- **CHIRPS v2.0**: https://data.chc.ucsb.edu/products/CHIRPS-2.0/
- **Referensi**: Funk et al., 2015. The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.

## Catatan
- Data ini adalah **contoh/sampel** berdasarkan pola klimatologis realistis Lampung
- Untuk data asli, gunakan script `download_chirps.py`
- Lampung memiliki iklim tropis dengan musim hujan (Nov-Mar) dan musim kering (Jun-Sep)
