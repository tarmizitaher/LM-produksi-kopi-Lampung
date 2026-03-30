"""
Menghitung dan memvisualisasikan anomali curah hujan CHIRPS untuk Lampung.
Anomali = Curah Hujan Aktual - Rata-rata Klimatologis (baseline)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.interpolate import griddata
import os

output_dir = os.path.dirname(os.path.abspath(__file__))

# Load data
df = pd.read_csv(os.path.join(output_dir, "chirps_lampung_monthly_2025_2026.csv"))

# Baseline klimatologis (mm/bulan) — rata-rata jangka panjang CHIRPS untuk Lampung
# Sumber: pola klimatologis tropis Lampung (1981-2010 approx.)
baseline = {
    1: 298, 2: 275, 3: 252, 4: 185, 5: 132,
    6: 88,  7: 72,  8: 58,  9: 85, 10: 148,
    11: 215, 12: 278
}

# Hitung anomali
df["baseline_mm"] = df["month"].map(baseline)
df["anomali_mm"] = df["precipitation_mm"] - df["baseline_mm"]
df["anomali_persen"] = ((df["precipitation_mm"] - df["baseline_mm"]) / df["baseline_mm"]) * 100
df["periode"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

# === Simpan tabel anomali ===
anomali_cols = ["year", "month", "station_id", "station_name", "latitude", "longitude",
                "precipitation_mm", "baseline_mm", "anomali_mm", "anomali_persen"]
df[anomali_cols].to_csv(os.path.join(output_dir, "chirps_lampung_anomali.csv"), index=False)

# === Ringkasan anomali per bulan (rata-rata semua stasiun) ===
summary = df.groupby(["year", "month", "periode"]).agg(
    rerata_aktual=("precipitation_mm", "mean"),
    baseline=("baseline_mm", "first"),
    anomali_mm=("anomali_mm", "mean"),
    anomali_persen=("anomali_persen", "mean"),
    min_anomali=("anomali_mm", "min"),
    max_anomali=("anomali_mm", "max"),
).reset_index().sort_values(["year", "month"])

print("=" * 70)
print("ANOMALI CURAH HUJAN CHIRPS — LAMPUNG 2025-2026")
print("=" * 70)
print(f"{'Periode':<10} {'Aktual':>8} {'Baseline':>10} {'Anomali':>10} {'Anomali%':>10} {'Kategori'}")
print("-" * 70)

def kategorikan(anom_pct):
    if anom_pct > 30:
        return "Sangat Basah"
    elif anom_pct > 15:
        return "Basah"
    elif anom_pct > -15:
        return "Normal"
    elif anom_pct > -30:
        return "Kering"
    else:
        return "Sangat Kering"

for _, row in summary.iterrows():
    kat = kategorikan(row["anomali_persen"])
    print(f'{row["periode"]:<10} {row["rerata_aktual"]:>7.1f} {row["baseline"]:>10.0f} '
          f'{row["anomali_mm"]:>+10.1f} {row["anomali_persen"]:>+9.1f}%  {kat}')

print("-" * 70)

# =====================================================================
# PLOT 1: Time series anomali bulanan (bar chart)
# =====================================================================
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), dpi=150, gridspec_kw={"height_ratios": [1.2, 1]})

periodes = summary["periode"].values
anomali_vals = summary["anomali_mm"].values
anomali_pct = summary["anomali_persen"].values

colors_bar = ["#d73027" if v < -30 else "#fc8d59" if v < -15 else "#91bfdb" if v < 15
              else "#4575b4" if v < 30 else "#313695" for v in anomali_pct]

bars = ax1.bar(range(len(periodes)), anomali_vals, color=colors_bar, edgecolor="black", linewidth=0.5)
ax1.axhline(y=0, color="black", linewidth=1)
ax1.set_xticks(range(len(periodes)))
ax1.set_xticklabels(periodes, rotation=45, ha="right", fontsize=9)
ax1.set_ylabel("Anomali Curah Hujan (mm)", fontsize=11, fontweight="bold")
ax1.set_title("Anomali Curah Hujan Bulanan — CHIRPS v2.0, Lampung 2025-2026",
              fontsize=13, fontweight="bold")
ax1.grid(axis="y", linestyle=":", alpha=0.4)

# Tambahkan label nilai pada bar
for i, (v, p) in enumerate(zip(anomali_vals, anomali_pct)):
    y_pos = v + 2 if v >= 0 else v - 5
    ax1.text(i, y_pos, f"{v:+.0f}", ha="center", va="bottom" if v >= 0 else "top",
             fontsize=7.5, fontweight="bold")

# Legend kategori
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#313695", edgecolor="black", label="Sangat Basah (>+30%)"),
    Patch(facecolor="#4575b4", edgecolor="black", label="Basah (+15% s/d +30%)"),
    Patch(facecolor="#91bfdb", edgecolor="black", label="Normal (-15% s/d +15%)"),
    Patch(facecolor="#fc8d59", edgecolor="black", label="Kering (-30% s/d -15%)"),
    Patch(facecolor="#d73027", edgecolor="black", label="Sangat Kering (<-30%)"),
]
ax1.legend(handles=legend_elements, loc="upper right", fontsize=8, framealpha=0.9)

# =====================================================================
# PLOT 2: Anomali per stasiun (heatmap)
# =====================================================================
pivot = df.pivot_table(index="station_name", columns="periode", values="anomali_mm", aggfunc="mean")
# Sort columns chronologically
pivot = pivot[sorted(pivot.columns)]

cmap_div = plt.cm.RdBu
norm_div = mcolors.TwoSlopeNorm(vmin=-80, vcenter=0, vmax=80)

im = ax2.imshow(pivot.values, cmap=cmap_div, norm=norm_div, aspect="auto")
ax2.set_xticks(range(len(pivot.columns)))
ax2.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=8)
ax2.set_yticks(range(len(pivot.index)))
ax2.set_yticklabels(pivot.index, fontsize=9)
ax2.set_title("Anomali per Stasiun (mm)", fontsize=12, fontweight="bold", pad=10)

# Annotate cells
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        color = "white" if abs(val) > 50 else "black"
        ax2.text(j, i, f"{val:+.0f}", ha="center", va="center", fontsize=6.5,
                 fontweight="bold", color=color)

cbar = plt.colorbar(im, ax=ax2, orientation="vertical", shrink=0.8, pad=0.02)
cbar.set_label("Anomali (mm)", fontsize=9)

plt.tight_layout()
fig1.savefig(os.path.join(output_dir, "anomali_curah_hujan_timeseries.png"), bbox_inches="tight", facecolor="white")
print(f"\nGrafik timeseries tersimpan: anomali_curah_hujan_timeseries.png")

# =====================================================================
# PLOT 3: Peta spasial anomali rata-rata tahunan
# =====================================================================
fig3, axes3 = plt.subplots(1, 2, figsize=(16, 8), dpi=150)

grid_lon = np.linspace(103.3, 106.2, 300)
grid_lat = np.linspace(-6.2, -3.3, 300)
grid_x, grid_y = np.meshgrid(grid_lon, grid_lat)

# Batas Lampung
lampung_lon = [104.0, 104.2, 104.0, 103.9, 104.0, 104.3, 104.5, 104.8,
               105.0, 105.2, 105.5, 105.8, 105.9, 105.8, 105.7, 105.5,
               105.3, 105.0, 104.7, 104.4, 104.1, 104.0]
lampung_lat = [-5.0, -5.2, -5.4, -5.6, -5.8, -5.9, -5.95, -5.9,
               -5.85, -5.8, -5.75, -5.6, -5.3, -5.0, -4.8, -4.6,
               -4.5, -4.4, -4.5, -4.6, -4.8, -5.0]

cmap_div = plt.cm.RdBu
titles = ["Anomali Rata-rata (mm)", "Anomali Rata-rata (%)"]
value_cols = ["anomali_mm", "anomali_persen"]
vmaxs = [60, 30]

for idx, (title, col, vmax) in enumerate(zip(titles, value_cols, vmaxs)):
    ax3 = axes3[idx]

    sta_anom = df.groupby(["station_id", "station_name", "latitude", "longitude"]).agg(
        val=(col, "mean")
    ).reset_index()

    s_lons = sta_anom["longitude"].values
    s_lats = sta_anom["latitude"].values
    s_vals = sta_anom["val"].values

    s_grid = griddata((s_lons, s_lats), s_vals, (grid_x, grid_y), method="cubic")

    norm_s = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    cf = ax3.contourf(grid_x, grid_y, s_grid,
                      levels=np.linspace(-vmax, vmax, 21),
                      cmap=cmap_div, norm=norm_s, extend="both")
    ax3.scatter(s_lons, s_lats, c=s_vals, cmap=cmap_div, norm=norm_s,
                edgecolors="black", linewidths=1, s=80, zorder=5)

    for _, row in sta_anom.iterrows():
        unit = " mm" if col == "anomali_mm" else "%"
        ax3.annotate(f'{row["station_name"]}\n({row["val"]:+.1f}{unit})',
                     xy=(row["longitude"], row["latitude"]),
                     xytext=(row["longitude"] + 0.05, row["latitude"] + 0.05),
                     fontsize=6.5, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="gray"),
                     zorder=6)

    ax3.plot(lampung_lon, lampung_lat, color="black", linewidth=1.2, linestyle="--", alpha=0.5)
    ax3.set_xlim(103.5, 106.0)
    ax3.set_ylim(-6.1, -3.4)
    ax3.set_aspect("equal")
    ax3.grid(True, linestyle=":", alpha=0.3)
    ax3.set_xlabel("Bujur (°E)", fontsize=10)
    ax3.set_ylabel("Lintang (°S)", fontsize=10)
    ax3.set_title(title, fontsize=12, fontweight="bold")

    unit_label = "mm" if col == "anomali_mm" else "%"
    plt.colorbar(cf, ax=ax3, orientation="horizontal", pad=0.08, shrink=0.85,
                 label=f"Anomali ({unit_label})")

fig3.suptitle("Peta Anomali Curah Hujan — CHIRPS v2.0, Lampung 2025-2026\n(terhadap baseline klimatologis 1981-2010)",
              fontsize=14, fontweight="bold", y=1.03)
plt.tight_layout()
fig3.savefig(os.path.join(output_dir, "anomali_curah_hujan_spasial.png"), bbox_inches="tight", facecolor="white")
print(f"Peta spasial anomali tersimpan: anomali_curah_hujan_spasial.png")

print(f"\nFile CSV anomali tersimpan: chirps_lampung_anomali.csv ({len(df)} records)")
