"""
Peta spasial distribusi curah hujan rata-rata CHIRPS untuk wilayah Lampung.
Menggunakan interpolasi dari titik-titik stasiun ke grid kontinu.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.interpolate import griddata
from matplotlib.patches import FancyArrowPatch
import os

output_dir = os.path.dirname(os.path.abspath(__file__))

# Load data
df = pd.read_csv(os.path.join(output_dir, "chirps_lampung_monthly_2025_2026.csv"))

# Hitung rata-rata curah hujan per stasiun
avg = df.groupby(["station_id", "station_name", "latitude", "longitude"]).agg(
    mean_precip=("precipitation_mm", "mean")
).reset_index()

# Koordinat stasiun
lons = avg["longitude"].values
lats = avg["latitude"].values
precip = avg["mean_precip"].values

# Buat grid interpolasi
grid_lon = np.linspace(103.3, 106.2, 300)
grid_lat = np.linspace(-6.2, -3.3, 300)
grid_x, grid_y = np.meshgrid(grid_lon, grid_lat)

# Interpolasi menggunakan metode cubic
grid_precip = griddata((lons, lats), precip, (grid_x, grid_y), method="cubic")

# Buat batas kasar wilayah Lampung (simplified polygon)
lampung_lon = [104.0, 104.2, 104.0, 103.9, 104.0, 104.3, 104.5, 104.8,
               105.0, 105.2, 105.5, 105.8, 105.9, 105.8, 105.7, 105.5,
               105.3, 105.0, 104.7, 104.4, 104.1, 104.0]
lampung_lat = [-5.0, -5.2, -5.4, -5.6, -5.8, -5.9, -5.95, -5.9,
               -5.85, -5.8, -5.75, -5.6, -5.3, -5.0, -4.8, -4.6,
               -4.5, -4.4, -4.5, -4.6, -4.8, -5.0]

# ---- PLOT ----
fig, ax = plt.subplots(1, 1, figsize=(10, 12), dpi=150)

# Colormap
cmap = plt.cm.YlGnBu
bounds = np.arange(100, 260, 10)
norm = mcolors.BoundaryNorm(bounds, cmap.N, extend="both")

# Contour fill
cf = ax.contourf(grid_x, grid_y, grid_precip, levels=bounds, cmap=cmap, norm=norm, extend="both")

# Contour lines
cs = ax.contour(grid_x, grid_y, grid_precip, levels=bounds[::2], colors="gray",
                linewidths=0.4, alpha=0.5)
ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")

# Plot batas Lampung (approximate)
ax.plot(lampung_lon, lampung_lat, color="black", linewidth=1.5, linestyle="--", alpha=0.6,
        label="Batas Lampung (aproks.)")

# Plot stasiun
scatter = ax.scatter(lons, lats, c=precip, cmap=cmap, norm=norm,
                     edgecolors="black", linewidths=1.2, s=120, zorder=5)

# Label stasiun
for _, row in avg.iterrows():
    offset_x = 0.05
    offset_y = 0.05
    # Adjust label positions to avoid overlap
    if row["station_name"] == "Menggala":
        offset_x = 0.08
    elif row["station_name"] == "Sukadana":
        offset_x = 0.08
    elif row["station_name"] == "Kotabumi":
        offset_y = 0.08
    elif row["station_name"] == "Pesawaran":
        offset_y = -0.12

    ax.annotate(
        f'{row["station_name"]}\n({row["mean_precip"]:.0f} mm)',
        xy=(row["longitude"], row["latitude"]),
        xytext=(row["longitude"] + offset_x, row["latitude"] + offset_y),
        fontsize=7, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, edgecolor="gray"),
        arrowprops=dict(arrowstyle="-", color="gray", lw=0.5),
        zorder=6,
    )

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation="horizontal", pad=0.06, shrink=0.75, aspect=30)
cbar.set_label("Curah Hujan Rata-rata (mm/bulan)", fontsize=11, fontweight="bold")
cbar.ax.tick_params(labelsize=9)

# Grid & labels
ax.set_xlabel("Bujur (°E)", fontsize=11)
ax.set_ylabel("Lintang (°S)", fontsize=11)
ax.set_title("Distribusi Spasial Curah Hujan Rata-rata\nCHIRPS v2.0 — Lampung, Jan 2025 – Feb 2026",
             fontsize=14, fontweight="bold", pad=15)

ax.set_xlim(103.5, 106.0)
ax.set_ylim(-6.1, -3.4)
ax.set_aspect("equal")
ax.grid(True, linestyle=":", alpha=0.4)
ax.tick_params(labelsize=9)

# North arrow
ax.annotate("N", xy=(105.85, -3.55), fontsize=14, fontweight="bold", ha="center")
ax.annotate("", xy=(105.85, -3.45), xytext=(105.85, -3.65),
            arrowprops=dict(arrowstyle="->", lw=2, color="black"))

# Info text
info_text = (
    "Sumber: CHIRPS v2.0 (sampel)\n"
    "Resolusi: 0.05° (~5 km)\n"
    "Metode: Interpolasi Cubic\n"
    f"Stasiun: {len(avg)} titik"
)
ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=7,
        verticalalignment="bottom", bbox=dict(boxstyle="round", facecolor="lightyellow",
                                              alpha=0.9, edgecolor="gray"))

plt.tight_layout()

# Save
output_path = os.path.join(output_dir, "peta_curah_hujan_lampung.png")
plt.savefig(output_path, bbox_inches="tight", facecolor="white")
print(f"Peta tersimpan: {output_path}")

# Also save seasonal maps
fig2, axes = plt.subplots(1, 3, figsize=(18, 8), dpi=150)

seasons = {
    "Musim Hujan\n(Nov-Mar)": [11, 12, 1, 2, 3],
    "Transisi\n(Apr-Mei, Okt)": [4, 5, 10],
    "Musim Kering\n(Jun-Sep)": [6, 7, 8, 9],
}

for idx, (season_name, months) in enumerate(seasons.items()):
    ax2 = axes[idx]
    season_df = df[df["month"].isin(months)]
    season_avg = season_df.groupby(["station_id", "latitude", "longitude"]).agg(
        mean_precip=("precipitation_mm", "mean")
    ).reset_index()

    s_lons = season_avg["longitude"].values
    s_lats = season_avg["latitude"].values
    s_precip = season_avg["mean_precip"].values

    s_grid = griddata((s_lons, s_lats), s_precip, (grid_x, grid_y), method="cubic")

    # Use same color scale for comparison
    s_bounds = np.arange(40, 360, 20)
    s_norm = mcolors.BoundaryNorm(s_bounds, cmap.N, extend="both")

    cf2 = ax2.contourf(grid_x, grid_y, s_grid, levels=s_bounds, cmap=cmap, norm=s_norm, extend="both")
    ax2.scatter(s_lons, s_lats, c=s_precip, cmap=cmap, norm=s_norm,
                edgecolors="black", linewidths=0.8, s=60, zorder=5)
    ax2.plot(lampung_lon, lampung_lat, color="black", linewidth=1, linestyle="--", alpha=0.5)

    ax2.set_title(f"{season_name}\n(Rata-rata: {s_precip.mean():.0f} mm/bln)", fontsize=11, fontweight="bold")
    ax2.set_xlim(103.5, 106.0)
    ax2.set_ylim(-6.1, -3.4)
    ax2.set_aspect("equal")
    ax2.grid(True, linestyle=":", alpha=0.3)
    ax2.tick_params(labelsize=8)

    plt.colorbar(cf2, ax=ax2, orientation="horizontal", pad=0.08, shrink=0.85, aspect=20,
                 label="mm/bulan")

fig2.suptitle("Distribusi Curah Hujan per Musim — CHIRPS v2.0, Lampung 2025-2026",
              fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()

output_path2 = os.path.join(output_dir, "peta_curah_hujan_musiman.png")
fig2.savefig(output_path2, bbox_inches="tight", facecolor="white")
print(f"Peta musiman tersimpan: {output_path2}")
