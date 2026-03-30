"""
Train and evaluate ML models for coffee yield prediction.

Usage:
    python -m src.modeling.train
    python -m src.modeling.train --model random_forest
    python -m src.modeling.train --tune

Supports:
    - Leave-One-Year-Out cross-validation
    - Multiple models (LR, RF, XGBoost, SVR)
    - Hyperparameter tuning via GridSearchCV
    - Ablation study across feature subsets
    - Final hold-out test evaluation (one-time only)
"""

import os
import sys
import json
import warnings
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from configs.paths import PROCESSED_DIR, MODELS_DIR, TABLES_DIR, STUDY_PERIOD, RANDOM_STATE, ensure_dirs
from configs.models import MODEL_CONFIGS, METRICS
from configs.features import TARGET, FEATURE_SETS

warnings.filterwarnings("ignore")


# =====================================================================
# Metrics
# =====================================================================

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute all evaluation metrics."""
    mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
    y_t, y_p = y_true[mask], y_pred[mask]

    if len(y_t) < 2:
        return {m: np.nan for m in METRICS}

    r2 = r2_score(y_t, y_p)
    rmse = np.sqrt(mean_squared_error(y_t, y_p))
    mae = mean_absolute_error(y_t, y_p)
    mape = np.mean(np.abs((y_t - y_p) / y_t)) * 100 if np.all(y_t != 0) else np.nan

    return {"r2": round(r2, 4), "rmse": round(rmse, 2), "mae": round(mae, 2), "mape": round(mape, 2)}


# =====================================================================
# Model factory
# =====================================================================

def create_model(model_name: str):
    """Instantiate a model from config."""
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_CONFIGS.keys())}")

    cfg = MODEL_CONFIGS[model_name]

    if model_name == "linear_regression":
        return LinearRegression(**cfg["params"])
    elif model_name == "random_forest":
        return RandomForestRegressor(**cfg["params"])
    elif model_name == "xgboost":
        try:
            from xgboost import XGBRegressor
            return XGBRegressor(**cfg["params"])
        except ImportError:
            print("  WARNING: xgboost not installed. Skipping.")
            return None
    elif model_name == "svr":
        return SVR(**cfg["params"])
    else:
        raise ValueError(f"No factory for model: {model_name}")


# =====================================================================
# Data loading
# =====================================================================

def load_data(feature_set: str = "full") -> Tuple[pd.DataFrame, List[str], str]:
    """
    Load analysis dataset and return features + target.

    Returns:
        (dataframe, feature_columns, target_column)
    """
    path = PROCESSED_DIR / "analysis_dataset.csv"
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}. Run preprocessing pipeline first.")

    df = pd.read_csv(path)

    # Map config feature names to actual column names
    target_col = "produktivitas_kg_ha"

    # Get available numeric features from the dataset
    exclude = ["year", target_col, "produksi_ton", "luas_panen_ha", "source", "verified", "kabupaten"]
    available = [c for c in df.select_dtypes(include=[np.number]).columns if c not in exclude]

    if feature_set == "full":
        feature_cols = available
    else:
        requested = FEATURE_SETS.get(feature_set, FEATURE_SETS["full"])
        feature_cols = [c for c in available if c in requested]
        if not feature_cols:
            feature_cols = available

    # Drop features with >50% NaN, then drop rows with NaN
    keep_cols = ["year"] + feature_cols + [target_col]
    temp = df[keep_cols].copy()
    nan_pct = temp[feature_cols].isna().mean()
    drop_features = nan_pct[nan_pct > 0.5].index.tolist()
    if drop_features:
        print(f"  Dropping high-NaN features: {drop_features}")
        feature_cols = [c for c in feature_cols if c not in drop_features]
    subset = df[["year"] + feature_cols + [target_col]].dropna()

    print(f"  Dataset: {len(subset)} samples, {len(feature_cols)} features")
    print(f"  Features: {feature_cols}")
    print(f"  Target: {target_col}")
    print(f"  Year range: {subset['year'].min()}-{subset['year'].max()}")

    return subset, feature_cols, target_col


# =====================================================================
# Cross-validation
# =====================================================================

def leave_one_year_out_cv(
    model,
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
    scale: bool = False,
    model_name: str = "linear_regression",
) -> Dict:
    """
    Leave-One-Year-Out cross-validation.

    Returns dict with metrics and per-fold predictions.
    """
    logo = LeaveOneGroupOut()
    groups = df["year"].values
    X = df[feature_cols].values
    y = df[target_col].values

    y_true_all = []
    y_pred_all = []
    year_all = []
    fold_metrics = []

    for train_idx, test_idx in logo.split(X, y, groups):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        if scale:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        model_clone = create_model(model_name)
        if model_clone is None:
            continue

        model_clone.fit(X_train, y_train)
        y_pred = model_clone.predict(X_test)

        y_true_all.extend(y_test)
        y_pred_all.extend(y_pred)
        year_all.extend(groups[test_idx])

        fold_m = compute_metrics(np.array(y_test), np.array(y_pred))
        fold_m["year"] = int(groups[test_idx][0])
        fold_metrics.append(fold_m)

    overall = compute_metrics(np.array(y_true_all), np.array(y_pred_all))

    return {
        "overall_metrics": overall,
        "fold_metrics": fold_metrics,
        "predictions": pd.DataFrame({
            "year": year_all,
            "y_true": y_true_all,
            "y_pred": y_pred_all,
        }),
    }


# =====================================================================
# Hyperparameter tuning
# =====================================================================

def tune_model(
    model_name: str,
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
) -> Dict:
    """Grid search with LOGO CV for hyperparameter tuning."""
    cfg = MODEL_CONFIGS[model_name]
    if "search_space" not in cfg:
        print(f"  No search space defined for {model_name}. Using defaults.")
        return {}

    model = create_model(model_name)
    if model is None:
        return {}

    logo = LeaveOneGroupOut()
    groups = df["year"].values
    X = df[feature_cols].values
    y = df[target_col].values

    if model_name == "svr":
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    grid = GridSearchCV(
        model, cfg["search_space"],
        cv=logo, scoring="r2",
        n_jobs=-1, verbose=0,
    )
    grid.fit(X, y, groups=groups)

    print(f"  Best params: {grid.best_params_}")
    print(f"  Best CV R²: {grid.best_score_:.4f}")

    return {
        "best_params": grid.best_params_,
        "best_score": round(grid.best_score_, 4),
        "cv_results": pd.DataFrame(grid.cv_results_)[["params", "mean_test_score", "std_test_score"]].to_dict("records"),
    }


# =====================================================================
# Train all models
# =====================================================================

def train_all(
    feature_set: str = "full",
    tune: bool = False,
) -> pd.DataFrame:
    """Train all configured models and compare."""
    ensure_dirs()

    print("=" * 60)
    print("Model Training Pipeline")
    print(f"Feature set: {feature_set}")
    print(f"Tuning: {tune}")
    print("=" * 60)

    df, feature_cols, target_col = load_data(feature_set)

    results = []
    all_predictions = {}

    for model_name, cfg in MODEL_CONFIGS.items():
        print(f"\n{'─' * 40}")
        print(f"Training: {model_name} ({cfg['description']})")
        print(f"{'─' * 40}")

        model = create_model(model_name)
        if model is None:
            continue

        scale = model_name == "svr"

        # Tune if requested
        if tune and "search_space" in cfg:
            print("  Tuning hyperparameters...")
            tune_result = tune_model(model_name, df, feature_cols, target_col)
            if tune_result.get("best_params"):
                model.set_params(**tune_result["best_params"])

        # Cross-validation
        print("  Running Leave-One-Year-Out CV...")
        cv_result = leave_one_year_out_cv(model, df, feature_cols, target_col, scale=scale, model_name=model_name)

        metrics = cv_result["overall_metrics"]
        print(f"  Results: R²={metrics['r2']}, RMSE={metrics['rmse']}, MAE={metrics['mae']}, MAPE={metrics['mape']}%")

        results.append({
            "model": model_name,
            "feature_set": feature_set,
            "n_features": len(feature_cols),
            "n_samples": len(df),
            **metrics,
            "timestamp": datetime.now().isoformat(),
        })

        all_predictions[model_name] = cv_result["predictions"]

        # Train final model on all data and save
        X_all = df[feature_cols].values
        y_all = df[target_col].values
        if scale:
            scaler = StandardScaler()
            X_all = scaler.fit_transform(X_all)

        model.fit(X_all, y_all)
        model_path = MODELS_DIR / f"{model_name}_{feature_set}_{datetime.now().strftime('%Y%m%d')}.joblib"
        joblib.dump({"model": model, "features": feature_cols, "scaler": scaler if scale else None}, model_path)
        print(f"  Saved: {model_path.name}")

    # Comparison table
    comparison = pd.DataFrame(results)
    comparison = comparison.sort_values("r2", ascending=False)

    print(f"\n{'=' * 60}")
    print("MODEL COMPARISON")
    print(f"{'=' * 60}")
    print(comparison[["model", "r2", "rmse", "mae", "mape"]].to_string(index=False))

    # Save results
    comp_path = TABLES_DIR / f"model_comparison_{feature_set}.csv"
    comparison.to_csv(comp_path, index=False)
    print(f"\nSaved: {comp_path}")

    # Save predictions
    for model_name, preds in all_predictions.items():
        pred_path = TABLES_DIR / f"predictions_{model_name}_{feature_set}.csv"
        preds.to_csv(pred_path, index=False)

    # Append to experiment log
    log_path = TABLES_DIR / "experiment_log.csv"
    if log_path.exists():
        existing = pd.read_csv(log_path)
        comparison = pd.concat([existing, comparison], ignore_index=True)
    comparison.to_csv(log_path, index=False)

    return comparison


# =====================================================================
# Ablation study
# =====================================================================

def ablation_study() -> pd.DataFrame:
    """Run models across different feature subsets to measure contribution."""
    print("\n" + "=" * 60)
    print("ABLATION STUDY")
    print("=" * 60)

    all_results = []

    # Only run ablation with available feature sets
    for set_name in FEATURE_SETS:
        print(f"\n>>> Feature set: {set_name}")
        try:
            df, feature_cols, target_col = load_data(set_name)
            if len(feature_cols) == 0 or len(df) < 5:
                print(f"  Skipped: insufficient features or data")
                continue

            for model_name in ["random_forest", "xgboost"]:
                model = create_model(model_name)
                if model is None:
                    continue

                scale = model_name == "svr"
                cv_result = leave_one_year_out_cv(model, df, feature_cols, target_col, scale=scale)

                all_results.append({
                    "feature_set": set_name,
                    "model": model_name,
                    "n_features": len(feature_cols),
                    **cv_result["overall_metrics"],
                })
        except Exception as e:
            print(f"  Error: {e}")

    if all_results:
        ablation_df = pd.DataFrame(all_results)
        abl_path = TABLES_DIR / "ablation_study.csv"
        ablation_df.to_csv(abl_path, index=False)
        print(f"\n{'=' * 60}")
        print("ABLATION RESULTS")
        print(f"{'=' * 60}")
        print(ablation_df.to_string(index=False))
        print(f"\nSaved: {abl_path}")
        return ablation_df

    return pd.DataFrame()


# =====================================================================
# Final test set evaluation (ONE TIME ONLY)
# =====================================================================

def final_test_evaluation(model_name: str, feature_set: str = "full") -> Dict:
    """
    Evaluate best model on hold-out test set (2021-2023).
    WARNING: This should be run exactly ONCE after all development is complete.
    """
    print("\n" + "!" * 60)
    print("FINAL TEST SET EVALUATION")
    print("WARNING: This uses the held-out test set. Run only once!")
    print("!" * 60)

    df, feature_cols, target_col = load_data(feature_set)

    train_df = df[df["year"] <= STUDY_PERIOD["train_end"]]
    test_df = df[df["year"] >= STUDY_PERIOD["test_start"]]

    if len(test_df) == 0:
        print("  ERROR: No test data available")
        return {}

    X_train = train_df[feature_cols].values
    y_train = train_df[target_col].values
    X_test = test_df[feature_cols].values
    y_test = test_df[target_col].values

    model = create_model(model_name)
    scale = model_name == "svr"

    if scale:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = compute_metrics(y_test, y_pred)

    print(f"\n  Model: {model_name}")
    print(f"  Train: {len(train_df)} samples ({train_df['year'].min()}-{train_df['year'].max()})")
    print(f"  Test:  {len(test_df)} samples ({test_df['year'].min()}-{test_df['year'].max()})")
    print(f"  R²={metrics['r2']}, RMSE={metrics['rmse']}, MAE={metrics['mae']}, MAPE={metrics['mape']}%")

    result = {
        "model": model_name,
        "metrics": metrics,
        "predictions": pd.DataFrame({
            "year": test_df["year"].values,
            "y_true": y_test,
            "y_pred": y_pred,
        }),
    }

    # Save
    test_path = TABLES_DIR / "final_test_results.csv"
    pd.DataFrame([{"model": model_name, **metrics}]).to_csv(test_path, index=False)
    print(f"\n  Saved: {test_path}")

    return result


# =====================================================================
# Main
# =====================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Train ML models for coffee yield prediction")
    parser.add_argument("--model", type=str, default=None, help="Train specific model only")
    parser.add_argument("--feature-set", type=str, default="full", help="Feature set to use")
    parser.add_argument("--tune", action="store_true", help="Run hyperparameter tuning")
    parser.add_argument("--ablation", action="store_true", help="Run ablation study")
    parser.add_argument("--final-test", type=str, default=None, help="Run final test with specified model")
    args = parser.parse_args()

    if args.ablation:
        ablation_study()
    elif args.final_test:
        final_test_evaluation(args.final_test, args.feature_set)
    else:
        train_all(feature_set=args.feature_set, tune=args.tune)


if __name__ == "__main__":
    main()
