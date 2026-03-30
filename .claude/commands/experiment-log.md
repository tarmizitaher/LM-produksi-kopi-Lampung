# Experiment Logger

Log and track ML experiment results.

## Instructions
1. If argument is `log` — Record a new experiment:
   - Read the latest model training output
   - Extract: model name, hyperparameters, features used, metrics (R², RMSE, MAE, MAPE)
   - Append to `reports/experiment_log.csv`
   - Print summary comparison with previous experiments

2. If argument is `compare` — Compare all logged experiments:
   - Read `reports/experiment_log.csv`
   - Generate a ranked comparison table
   - Highlight the best model per metric
   - Suggest next experiment to try

3. If argument is `summary` — Generate a summary report:
   - Best model overall
   - Most important features (from SHAP)
   - Key findings so far
   - Remaining experiments to run

Action: $ARGUMENTS
