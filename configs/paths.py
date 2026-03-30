"""
Central path configuration for the project.
All data paths are relative to the project root.
"""

from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

# Sub-directories for raw data
RAW_CHIRPS = RAW_DIR / "chirps"
RAW_ERA5 = RAW_DIR / "era5"
RAW_MODIS = RAW_DIR / "modis"
RAW_BPS = RAW_DIR / "bps"
RAW_BMKG = RAW_DIR / "bmkg"

# Output directories
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
MODELS_DIR = ROOT / "models"

# Study area bounds (Lampung Province)
LAMPUNG_BBOX = {
    "west": 103.5,
    "south": -6.0,
    "east": 106.0,
    "north": -3.5,
}

# Study period
STUDY_PERIOD = {
    "start": 2010,
    "end": 2023,
    "train_end": 2020,  # 2010-2020 for training
    "test_start": 2021,  # 2021-2023 for testing
}

# CHIRPS baseline period for SPI calculation
SPI_BASELINE = {
    "start": 1981,
    "end": 2023,
}

# Random seed for reproducibility
RANDOM_STATE = 42


def ensure_dirs() -> None:
    """Create all project directories if they don't exist."""
    for d in [
        RAW_CHIRPS, RAW_ERA5, RAW_MODIS, RAW_BPS, RAW_BMKG,
        INTERIM_DIR, PROCESSED_DIR, EXTERNAL_DIR,
        FIGURES_DIR, TABLES_DIR, MODELS_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)
