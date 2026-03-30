"""
Model evaluation, comparison, and SHAP analysis.

Usage:
    python -m src.evaluation.compare
    python -m src.evaluation.compare --shap random_forest
"""

import os
import sys
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import MODELS_DIR, TABLES_DIR, FIGURES_DIR, PROCESSED_DIR, ensure_dirs

# Publication-quality defaults
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
             "#0072B2", "#D55E00", "#CC79A7", "#000000"]


# =====================================================================
# Model comparison visualization
# =====================================================================

def plot_model_comparison(feature_set: str = "full") -> None:
    """Bar chart comparing model performance metrics."""
    comp_path = TABLES_DIR / f"model_comparison_{feature_set}.csv"
    if not comp_path.exists():
        print(f"No comparison file found: {comp_path}")
        return

    df = pd.read_csv(comp_path)

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    metrics = [("r2", "R²", True), ("rmse", "RMSE (kg/ha)", False),
               ("mae", "MAE (kg/ha)", False), ("mape", "MAPE (%)", False)]

    for ax, (col, label, higher_better) in zip(axes, metrics):
        colors = [OKABE_ITO[i] for i in range(len(df))]
        bars = ax.barh(df["model"], df[col], color=colors, edgecolor="black", linewidth=0.5)
        ax.set_xlabel(label)
        ax.invert_yaxis()

        # Annotate
        for bar, val in zip(bars, df[col]):
            ax.text(bar.get_width() + 0.01 * df[col].max(), bar.get_y() + bar.get_height() / 2,
                    f"{val:.2f}", va="center", fontsize=8)

        # Highlight best
        best_idx = df[col].idxmax() if higher_better else df[col].idxmin()
        bars[best_idx].set_edgecolor("red")
        bars[best_idx].set_linewidth(2)

    fig.suptitle(f"Model Comparison — LOGO CV ({feature_set})", fontweight="bold", y=1.02)
    plt.tight_layout()

    out = FIGURES_DIR / f"model_comparison_{feature_set}.png"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# Predicted vs Actual plot
# =====================================================================

def plot_predicted_vs_actual(feature_set: str = "full") -> None:
    """Scatter plot of predicted vs actual for all models."""
    comp_path = TABLES_DIR / f"model_comparison_{feature_set}.csv"
    if not comp_path.exists():
        return

    comp = pd.read_csv(comp_path)
    n_models = len(comp)
    fig, axes = plt.subplots(1, n_models, figsize=(4 * n_models, 4))
    if n_models == 1:
        axes = [axes]

    for ax, (_, row) in zip(axes, comp.iterrows()):
        pred_path = TABLES_DIR / f"predictions_{row['model']}_{feature_set}.csv"
        if not pred_path.exists():
            continue

        preds = pd.read_csv(pred_path)

        ax.scatter(preds["y_true"], preds["y_pred"], c=OKABE_ITO[0],
                   edgecolors="black", linewidths=0.5, s=50, alpha=0.8)

        # 1:1 line
        lims = [min(preds["y_true"].min(), preds["y_pred"].min()) - 10,
                max(preds["y_true"].max(), preds["y_pred"].max()) + 10]
        ax.plot(lims, lims, "k--", alpha=0.5, linewidth=1)
        ax.set_xlim(lims)
        ax.set_ylim(lims)

        ax.set_xlabel("Actual (kg/ha)")
        ax.set_ylabel("Predicted (kg/ha)")
        ax.set_title(f"{row['model']}\nR²={row['r2']:.3f}")
        ax.set_aspect("equal")

        # Annotate years
        for _, p in preds.iterrows():
            ax.annotate(str(int(p["year"])), (p["y_true"], p["y_pred"]),
                        fontsize=6, alpha=0.7, ha="center", va="bottom")

    fig.suptitle("Predicted vs Actual Productivity", fontweight="bold", y=1.02)
    plt.tight_layout()

    out = FIGURES_DIR / f"predicted_vs_actual_{feature_set}.png"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# SHAP Analysis
# =====================================================================

def shap_analysis(model_name: str, feature_set: str = "full") -> None:
    """Run SHAP analysis on the specified model."""
    try:
        import shap
    except ImportError:
        print("ERROR: shap not installed. Run: pip install shap")
        return

    # Find saved model
    model_files = sorted(MODELS_DIR.glob(f"{model_name}_{feature_set}_*.joblib"))
    if not model_files:
        print(f"No saved model found for {model_name}_{feature_set}")
        return

    saved = joblib.load(model_files[-1])  # latest
    model = saved["model"]
    feature_cols = saved["features"]
    scaler = saved.get("scaler")

    # Load data
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")
    available = [c for c in feature_cols if c in df.columns]
    df_clean = df[["year"] + available + ["produktivitas_kg_ha"]].dropna()
    X = df_clean[available].values

    if scaler:
        X = scaler.transform(X)

    print(f"Running SHAP on {model_name} with {len(available)} features, {len(X)} samples...")

    # Compute SHAP values
    if model_name in ["random_forest", "xgboost"]:
        explainer = shap.TreeExplainer(model)
    else:
        explainer = shap.KernelExplainer(model.predict, X)

    shap_values = explainer.shap_values(X)

    # --- SHAP Summary Plot ---
    fig, ax = plt.subplots(figsize=(8, 6))
    shap.summary_plot(shap_values, X, feature_names=available, show=False)
    plt.title(f"SHAP Feature Importance — {model_name}", fontweight="bold")
    plt.tight_layout()
    out = FIGURES_DIR / f"shap_summary_{model_name}.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()

    # --- SHAP Bar Plot (mean |SHAP|) ---
    fig, ax = plt.subplots(figsize=(8, 5))
    shap.summary_plot(shap_values, X, feature_names=available, plot_type="bar", show=False)
    plt.title(f"Mean |SHAP| — {model_name}", fontweight="bold")
    plt.tight_layout()
    out = FIGURES_DIR / f"shap_bar_{model_name}.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()

    # --- Top features table ---
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": available,
        "mean_abs_shap": mean_abs_shap,
    }).sort_values("mean_abs_shap", ascending=False)

    importance_path = TABLES_DIR / f"shap_importance_{model_name}.csv"
    importance_df.to_csv(importance_path, index=False)
    print(f"Saved: {importance_path}")

    print("\nTop 10 features by SHAP importance:")
    print(importance_df.head(10).to_string(index=False))


# =====================================================================
# Ablation visualization
# =====================================================================

def plot_ablation() -> None:
    """Plot ablation study results."""
    abl_path = TABLES_DIR / "ablation_study.csv"
    if not abl_path.exists():
        print("No ablation study results found.")
        return

    df = pd.read_csv(abl_path)

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, model in enumerate(df["model"].unique()):
        model_df = df[df["model"] == model].sort_values("n_features")
        ax.plot(model_df["feature_set"], model_df["r2"], "o-",
                color=OKABE_ITO[i], label=model, linewidth=2, markersize=8)

    ax.set_xlabel("Feature Set")
    ax.set_ylabel("R² (LOGO CV)")
    ax.set_title("Ablation Study: Feature Set Impact on Model Performance", fontweight="bold")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.4)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    out = FIGURES_DIR / "ablation_study.png"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()


# =====================================================================
# Main
# =====================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Model evaluation and SHAP analysis")
    parser.add_argument("--feature-set", type=str, default="full")
    parser.add_argument("--shap", type=str, default=None, help="Run SHAP on specified model")
    parser.add_argument("--ablation", action="store_true", help="Plot ablation results")
    args = parser.parse_args()

    ensure_dirs()

    if args.shap:
        shap_analysis(args.shap, args.feature_set)
    elif args.ablation:
        plot_ablation()
    else:
        plot_model_comparison(args.feature_set)
        plot_predicted_vs_actual(args.feature_set)
        print("\nAll comparison plots generated.")
        print("For SHAP analysis, run: python -m src.evaluation.compare --shap <model_name>")


if __name__ == "__main__":
    main()
