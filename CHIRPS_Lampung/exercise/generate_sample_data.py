"""
Generate realistic CHIRPS sample data for Lampung region.
Based on tropical rainfall patterns: wet season (Nov-Mar), dry season (Jun-Sep).
"""

import csv
import random
import os

random.seed(42)

# Lampung stations
stations = [
    ("LP01", "Bandar Lampung", -5.45, 105.26),
    ("LP02", "Metro", -5.11, 105.31),
    ("LP03", "Pringsewu", -5.36, 104.97),
    ("LP04", "Kotabumi", -4.83, 104.88),
    ("LP05", "Liwa", -5.02, 104.06),
    ("LP06", "Kalianda", -5.72, 105.62),
    ("LP07", "Menggala", -4.54, 105.24),
    ("LP08", "Sukadana", -4.75, 105.50),
    ("LP09", "Tanggamus", -5.42, 104.63),
    ("LP10", "Pesawaran", -5.52, 105.08),
]

# Typical monthly rainfall (mm) for Lampung - climatological average
# Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
base_rainfall = [298, 275, 252, 185, 132, 88, 72, 58, 85, 148, 215, 278]

output_dir = os.path.dirname(os.path.abspath(__file__))

# Generate monthly data
rows = []
for year in [2025, 2026]:
    months = range(1, 13) if year == 2025 else range(1, 3)  # 2026 only Jan-Feb
    for month in months:
        base = base_rainfall[month - 1]
        for sid, name, lat, lon in stations:
            # Add realistic variation: ±20% spatial, ±15% temporal
            spatial_factor = 1.0 + random.uniform(-0.20, 0.20)
            temporal_factor = 1.0 + random.uniform(-0.15, 0.15)
            # Highland stations (Liwa) get more rain
            altitude_factor = 1.15 if sid == "LP05" else 1.0
            # Coastal stations slightly more
            coastal_factor = 1.05 if sid == "LP06" else 1.0

            rainfall = base * spatial_factor * temporal_factor * altitude_factor * coastal_factor
            rainfall = round(max(0, rainfall), 1)

            rows.append({
                "year": year,
                "month": month,
                "station_id": sid,
                "station_name": name,
                "latitude": lat,
                "longitude": lon,
                "precipitation_mm": rainfall,
            })

# Write monthly detail
with open(os.path.join(output_dir, "chirps_lampung_monthly_2025_2026.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["year", "month", "station_id", "station_name",
                                           "latitude", "longitude", "precipitation_mm"])
    writer.writeheader()
    writer.writerows(rows)

# Generate summary
summary = {}
for r in rows:
    key = (r["year"], r["month"])
    if key not in summary:
        summary[key] = []
    summary[key].append(r["precipitation_mm"])

with open(os.path.join(output_dir, "chirps_lampung_summary.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["year", "month", "mean_precipitation_mm",
                                           "min_precipitation_mm", "max_precipitation_mm",
                                           "std_precipitation_mm", "num_stations"])
    writer.writeheader()
    for (year, month), vals in sorted(summary.items()):
        n = len(vals)
        mean_val = sum(vals) / n
        min_val = min(vals)
        max_val = max(vals)
        std_val = (sum((x - mean_val) ** 2 for x in vals) / n) ** 0.5
        writer.writerow({
            "year": year,
            "month": month,
            "mean_precipitation_mm": round(mean_val, 1),
            "min_precipitation_mm": round(min_val, 1),
            "max_precipitation_mm": round(max_val, 1),
            "std_precipitation_mm": round(std_val, 1),
            "num_stations": n,
        })

print("Sample CHIRPS data generated successfully!")
print(f"  - chirps_lampung_monthly_2025_2026.csv ({len(rows)} records)")
print(f"  - chirps_lampung_summary.csv ({len(summary)} months)")
