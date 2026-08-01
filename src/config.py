"""
Configuration Module
====================

Centralized configuration for the Financial Intelligence OS.

This module defines:
- Project directories
- Application constants
- Environment configuration
"""

from pathlib import Path

# =============================================================================
# PROJECT ROOT
# =============================================================================

# financial-intelligence-os/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =============================================================================
# ROOT DIRECTORIES
# =============================================================================

DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"
DASHBOARDS_DIR = PROJECT_ROOT / "dashboards"

# =============================================================================
# DATA DIRECTORIES
# =============================================================================

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# =============================================================================
# DEFAULT SETTINGS
# =============================================================================

DEFAULT_ENCODING = "utf-8"
DEFAULT_TIMEZONE = "UTC"

# =============================================================================
# CREATE REQUIRED DIRECTORIES
# =============================================================================

REQUIRED_DIRECTORIES = [
    DATA_DIR,
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    LOGS_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    NOTEBOOKS_DIR,
]

for directory in REQUIRED_DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)