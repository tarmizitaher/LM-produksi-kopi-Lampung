"""
Model configurations and hyperparameter search spaces.
"""

RANDOM_STATE = 42

# Model configurations with default hyperparameters
MODEL_CONFIGS = {
    "linear_regression": {
        "class": "sklearn.linear_model.LinearRegression",
        "params": {},
        "description": "Baseline linear model",
    },
    "random_forest": {
        "class": "sklearn.ensemble.RandomForestRegressor",
        "params": {
            "n_estimators": 200,
            "max_depth": 10,
            "min_samples_leaf": 5,
            "random_state": RANDOM_STATE,
        },
        "search_space": {
            "n_estimators": [100, 200, 500],
            "max_depth": [5, 10, 15, None],
            "min_samples_leaf": [3, 5, 10],
            "min_samples_split": [2, 5, 10],
        },
        "description": "Ensemble bagging — robust for small datasets",
    },
    "xgboost": {
        "class": "xgboost.XGBRegressor",
        "params": {
            "n_estimators": 200,
            "max_depth": 5,
            "learning_rate": 0.1,
            "reg_alpha": 0.1,
            "reg_lambda": 1.0,
            "random_state": RANDOM_STATE,
        },
        "search_space": {
            "n_estimators": [100, 200, 500],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.05, 0.1],
            "reg_alpha": [0, 0.1, 1.0],
            "reg_lambda": [0.5, 1.0, 2.0],
        },
        "description": "Gradient boosting — state of the art for tabular data",
    },
    "svr": {
        "class": "sklearn.svm.SVR",
        "params": {
            "kernel": "rbf",
            "C": 10.0,
            "epsilon": 0.1,
        },
        "search_space": {
            "C": [0.1, 1.0, 10.0, 100.0],
            "epsilon": [0.01, 0.1, 0.5],
            "kernel": ["rbf", "linear"],
            "gamma": ["scale", "auto"],
        },
        "description": "Kernel-based — good for small sample sizes",
    },
}

# Evaluation metrics
METRICS = ["r2", "rmse", "mae", "mape"]

# Cross-validation strategy
CV_CONFIG = {
    "method": "LeaveOneGroupOut",  # Leave-One-Year-Out
    "group_column": "year",
    "n_splits": None,  # Determined by number of years
}
