# Incremental Analysis-Write Workflow

## Rule
Every analysis must be immediately followed by documenting its results. Never batch multiple analyses before writing.

## Cycle
1. **Analyze** — run the Python script, generate figure/table, verify output
2. **Document** — update the corresponding section in the manuscript/report with results and interpretation
3. **Verify** — confirm figures are saved to `reports/figures/`, tables to `reports/tables/`
4. **Log** — record experiment results if ML-related (use `/experiment-log log`)
5. Repeat for next analysis

## Why
Batching analysis creates a backlog of unwritten results that lose context. Writing immediately after analysis ensures:
- Findings are interpreted while the data is fresh
- Figures and narrative stay aligned
- Progress is always visible
- No orphan figures without discussion

## What "document" means
- Save the figure/table to `reports/figures/` or `reports/tables/`
- Write the results paragraph: what the data shows (with specific numbers)
- Write the interpretation: what it means for the research questions
- Note any unexpected findings or limitations
- Cross-reference with other analyses where relevant

## Pipeline Order
Follow this sequence — each phase depends on the previous:
1. Data collection → verify completeness with `/data-check`
2. Preprocessing → validate data quality, check for missing values
3. EDA → document key patterns and distributions
4. CHIRPS validation (vs BMKG) → document accuracy metrics
5. Feature engineering → document feature distributions and correlations
6. Model training → log each experiment with `/experiment-log log`
7. Model evaluation → compare results with `/experiment-log compare`
8. SHAP analysis → document feature importance findings
9. Paper drafting → use `/paper-draft <section>` per section
