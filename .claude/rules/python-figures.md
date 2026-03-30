# Python Figure Generation Rules

## Style System
This project uses a consistent matplotlib style for all figures. Every visualization script MUST follow these rules.

## Required for every figure:

### 1. Base Setup
```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication-quality defaults
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})
```

### 2. Color Palette
Use colorblind-friendly palettes only:
- **Sequential** (precipitation, NDVI): `plt.cm.YlGnBu`, `plt.cm.viridis`
- **Diverging** (anomalies): `plt.cm.RdBu`, `plt.cm.RdYlBu`
- **Categorical** (model comparison): Okabe-Ito palette:
  ```python
  OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#000000"]
  ```
- **Never** use rainbow/jet colormap
- **Never** hardcode random hex colors

### 3. Export Standards
- **Formats**: always save PNG + PDF (PDF for vector in paper, PNG for quick preview)
- **DPI**: 300 for publication, 150 for drafts
- **Sizes** (width in inches):
  - Single column: 3.5 in (~89 mm)
  - 1.5 column: 5.5 in (~140 mm)
  - Full width: 7.5 in (~190 mm)
- **Output directory**: `reports/figures/`

### 4. Naming Convention
- Pattern: `fig{N}_{descriptive_name}.{ext}` (e.g., `fig3_model_comparison.png`)
- Script location: `src/visualization/`

## Map Figures (Spatial Data)
- Always include: north arrow, scale indicator, coordinate labels
- Lampung boundary (approximate) for context
- Source attribution in figure caption or corner text
- Use `ax.set_aspect("equal")` for geographic plots

## Multi-panel Figures
- Use `plt.subplots()` with shared axes where appropriate
- Panel labels: lowercase **(a)**, **(b)**, **(c)** in top-left corner
- Consistent axis ranges across panels for fair comparison

## What NOT to do:
- Do NOT use `plt.show()` in production scripts — only save
- Do NOT use default matplotlib colors without setting palette
- Do NOT save figures outside `reports/figures/`
- Do NOT create figures without axis labels and units
- Do NOT use truncated y-axes without clearly marking the break
