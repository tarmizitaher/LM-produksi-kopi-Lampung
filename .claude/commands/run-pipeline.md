# Run Data Pipeline

Execute the data processing and modeling pipeline.

## Instructions
Based on the argument, run the appropriate pipeline stage:

### Stages
- `preprocess` — Run preprocessing pipeline: clean raw data, clip to Lampung, compute features
- `eda` — Run exploratory data analysis notebooks and generate summary statistics
- `train` — Train ML models with current processed data
- `evaluate` — Run evaluation metrics, SHAP analysis, generate comparison tables
- `figures` — Generate all publication-quality figures
- `all` — Run full pipeline end-to-end

### Rules
- Always check that input data exists before running a stage
- Print clear progress messages
- Save all outputs to appropriate directories (data/processed, reports/figures, etc.)
- Log any errors with helpful context
- After completion, summarize what was produced

Run stage: $ARGUMENTS
