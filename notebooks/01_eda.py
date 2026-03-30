"""
Exploratory Data Analysis — CHIRPS-ML Coffee Yield Prediction, Lampung
======================================================================

Run as script: python notebooks/01_eda.py
Or convert to notebook: jupytext --to notebook notebooks/01_eda.py

Generates all EDA figures to reports/figures/
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from configs.paths import PROCESSED_DIR, INTERIM_DIR, EXTERNAL_DIR, FIGURES_DIR, ensure_dirs

# Publication defaults
plt.rcParams.update({
    "font.family": "serif", "font.size": 10, "axes.labelsize": 11,
    "axes.titlesize": 12, "figure.dpi": 150, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.facecolor": "white",
})
OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
             "#0072B2", "#D55E00", "#CC79A7", "#000000"]


def load_data():
    """Load analysis dataset."""
    path = PROCESSED_DIR / "analysis_dataset.csv"
    if not path.exists():
        print(f"ERROR: {path} not found. Run preprocessing pipeline first.")
        sys.exit(1)
    df = pd.read_csv(path)
    print(f"Loaded: {len(df)} rows × {len(df.columns)} columns")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df


# =====================================================================
# EDA 1: Target variable distribution & trend
# =====================================================================

def plot_productivity_trend(df):
    """Time series of coffee productivity."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={"height_ratios": [2, 1]})

    # Productivity trend
    ax1.plot(df["year"], df["produktivitas_kg_ha"], "o-", color=OKABE_ITO[4],
             linewidth=2, markersize=8, label="Produktivitas (kg/ha)")
    ax1.axhline(df["produktivitas_kg_ha"].mean(), color="gray", linestyle="--", alpha=0.5,
                label=f'Mean: {df["produktivitas_kg_ha"].mean():.0f} kg/ha')
    ax1.fill_between(df["year"],
                     df["produktivitas_kg_ha"].mean() - df["produktivitas_kg_ha"].std(),
                     df["produktivitas_kg_ha"].mean() + df["produktivitas_kg_ha"].std(),
                     alpha=0.1, color="gray", label="±1 SD")
    ax1.set_ylabel("Produktivitas (kg/ha)")
    ax1.set_title("(a) Produktivitas Kopi Robusta Lampung", fontweight="bold")
    ax1.legend(fontsize=8)
    ax1.grid(True, linestyle=":", alpha=0.4)

    # Production & area
    ax2b = ax2.twinx()
    ax2.bar(df["year"], df["produksi_ton"] / 1000, color=OKABE_ITO[0], alpha=0.7, label="Produksi (ribu ton)")
    ax2b.plot(df["year"], df["luas_panen_ha"] / 1000, "s-", color=OKABE_ITO[5],
              linewidth=1.5, markersize=5, label="Luas panen (ribu ha)")
    ax2.set_xlabel("Tahun")
    ax2.set_ylabel("Produksi (ribu ton)")
    ax2b.set_ylabel("Luas panen (ribu ha)")
    ax2.set_title("(b) Produksi dan Luas Panen", fontweight="bold")
    ax2.legend(loc="upper left", fontsize=8)
    ax2b.legend(loc="upper right", fontsize=8)
    ax2.grid(True, linestyle=":", alpha=0.4)

    plt.tight_layout()
    out = FIGURES_DIR / "eda_productivity_trend.png"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# EDA 2: Precipitation patterns
# =====================================================================

def plot_precipitation_patterns(df):
    """Annual precipitation and seasonal breakdown."""
    precip_cols = [c for c in df.columns if c.startswith("precip_") and "lag" not in c and "cv" not in c]
    if not precip_cols or "precip_annual" not in df.columns:
        print("Skipping precipitation patterns: no CHIRPS features")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) Annual precipitation trend
    ax = axes[0, 0]
    ax.bar(df["year"], df["precip_annual"], color=OKABE_ITO[1], alpha=0.8)
    ax.axhline(df["precip_annual"].mean(), color="red", linestyle="--", alpha=0.5)
    ax.set_ylabel("Curah hujan (mm/tahun)")
    ax.set_title("(a) Curah Hujan Tahunan", fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.4)

    # (b) Seasonal breakdown
    ax = axes[0, 1]
    season_cols = ["precip_wet", "precip_dry", "precip_flowering", "precip_fruiting"]
    available_seasons = [c for c in season_cols if c in df.columns]
    if available_seasons:
        df_plot = df[["year"] + available_seasons].dropna()
        bottom = np.zeros(len(df_plot))
        for i, col in enumerate(available_seasons):
            ax.bar(df_plot["year"], df_plot[col], bottom=bottom, color=OKABE_ITO[i],
                   alpha=0.8, label=col.replace("precip_", ""))
            bottom += df_plot[col].values
        ax.set_ylabel("Curah hujan (mm)")
        ax.set_title("(b) Curah Hujan per Musim", fontweight="bold")
        ax.legend(fontsize=8)
        ax.grid(True, linestyle=":", alpha=0.4)

    # (c) Precipitation CV
    ax = axes[1, 0]
    if "precip_cv" in df.columns:
        ax.bar(df["year"], df["precip_cv"], color=OKABE_ITO[2], alpha=0.8)
        ax.set_ylabel("Coefficient of Variation")
        ax.set_title("(c) Variabilitas Curah Hujan (CV)", fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.4)

    # (d) Scatter: precip_annual vs productivity
    ax = axes[1, 1]
    if "precip_annual" in df.columns:
        mask = df[["precip_annual", "produktivitas_kg_ha"]].dropna().index
        x = df.loc[mask, "precip_annual"]
        y = df.loc[mask, "produktivitas_kg_ha"]
        ax.scatter(x, y, c=OKABE_ITO[4], edgecolors="black", s=60, linewidths=0.5)
        if len(x) > 2:
            slope, intercept, r, p, se = stats.linregress(x, y)
            ax.plot(x, slope * x + intercept, "r--", alpha=0.5)
            ax.text(0.05, 0.95, f"r={r:.3f}, p={p:.3f}", transform=ax.transAxes,
                    fontsize=9, va="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        for _, row in df.loc[mask].iterrows():
            ax.annotate(str(int(row["year"])), (row["precip_annual"], row["produktivitas_kg_ha"]),
                        fontsize=7, alpha=0.7)
        ax.set_xlabel("Curah hujan tahunan (mm)")
        ax.set_ylabel("Produktivitas (kg/ha)")
        ax.set_title("(d) CH Tahunan vs Produktivitas", fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.4)

    plt.tight_layout()
    out = FIGURES_DIR / "eda_precipitation_patterns.png"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# EDA 3: ENSO/IOD impact
# =====================================================================

def plot_enso_impact(df):
    """ENSO and IOD relationship with productivity."""
    if "nino34_annual" not in df.columns:
        print("Skipping ENSO analysis: no ENSO data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, (col, label) in zip(axes, [("nino34_annual", "ENSO (Nino 3.4)"),
                                        ("dmi_annual", "IOD (DMI)")]):
        if col not in df.columns:
            continue

        mask = df[[col, "produktivitas_kg_ha"]].dropna().index
        x = df.loc[mask, col]
        y = df.loc[mask, "produktivitas_kg_ha"]

        # Color by sign
        colors = [OKABE_ITO[5] if v > 0 else OKABE_ITO[1] for v in x]
        ax.scatter(x, y, c=colors, edgecolors="black", s=80, linewidths=0.5, zorder=5)

        if len(x) > 2:
            slope, intercept, r, p, se = stats.linregress(x, y)
            x_line = np.linspace(x.min(), x.max(), 100)
            ax.plot(x_line, slope * x_line + intercept, "k--", alpha=0.5)
            ax.text(0.05, 0.95, f"r={r:.3f}, p={p:.3f}", transform=ax.transAxes,
                    fontsize=9, va="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

        for _, row in df.loc[mask].iterrows():
            ax.annotate(str(int(row["year"])), (row[col], row["produktivitas_kg_ha"]),
                        fontsize=7, alpha=0.7)

        ax.axvline(0, color="gray", linestyle=":", alpha=0.5)
        ax.set_xlabel(f"{label} Index")
        ax.set_ylabel("Produktivitas (kg/ha)")
        ax.set_title(f"Produktivitas vs {label}", fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.4)

    plt.tight_layout()
    out = FIGURES_DIR / "eda_enso_iod_impact.png"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# EDA 4: Correlation matrix
# =====================================================================

def plot_correlation_matrix(df):
    """Heatmap of feature correlations with target."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    exclude = ["year"]
    cols = [c for c in numeric_cols if c not in exclude]

    if len(cols) < 3:
        print("Skipping correlation matrix: too few numeric columns")
        return

    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.RdBu_r
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

    im = ax.imshow(corr.values, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(cols)))
    ax.set_yticklabels(cols, fontsize=8)

    # Annotate
    for i in range(len(cols)):
        for j in range(len(cols)):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=6, color=color)

    plt.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
    ax.set_title("Correlation Matrix — Features & Target", fontweight="bold")
    plt.tight_layout()

    out = FIGURES_DIR / "eda_correlation_matrix.png"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"Saved: {out}")
    plt.close()

    # Print correlations with target
    target = "produktivitas_kg_ha"
    if target in corr.columns:
        print(f"\nCorrelation with {target}:")
        target_corr = corr[target].drop(target).sort_values(ascending=False)
        for feat, val in target_corr.items():
            marker = "***" if abs(val) > 0.7 else "**" if abs(val) > 0.5 else "*" if abs(val) > 0.3 else ""
            print(f"  {feat:<30} r = {val:+.3f} {marker}")


# =====================================================================
# Main
# =====================================================================

def main():
    ensure_dirs()
    print("=" * 60)
    print("Exploratory Data Analysis")
    print("=" * 60)

    df = load_data()

    print("\n[1/4] Productivity trend...")
    plot_productivity_trend(df)

    print("\n[2/4] Precipitation patterns...")
    plot_precipitation_patterns(df)

    print("\n[3/4] ENSO/IOD impact...")
    plot_enso_impact(df)

    print("\n[4/4] Correlation matrix...")
    plot_correlation_matrix(df)

    print(f"\n{'=' * 60}")
    print(f"EDA complete! Figures saved to: {FIGURES_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
