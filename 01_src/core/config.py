"""
Financial Intelligence OS
Configuration Module

Purpose
-------
Centralized configuration for the Financial Intelligence OS.

Responsibilities
----------------
- Load environment variables
- Define project paths
- Define application settings
- Create required directories
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# =============================================================================
# LOAD ENVIRONMENT VARIABLES
# =============================================================================

load_dotenv()

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
# APPLICATION SETTINGS
# =============================================================================

APP_NAME = os.getenv("APP_NAME", "Financial Intelligence OS")
APP_VERSION = os.getenv("APP_VERSION", "0.2.0")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

TIMEZONE = os.getenv("TIMEZONE", DEFAULT_TIMEZONE)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# =============================================================================
# REQUIRED DIRECTORIES
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
    DOCS_DIR,
    DASHBOARDS_DIR,
]

# =============================================================================
# CREATE PROJECT DIRECTORIES
# =============================================================================

for directory in REQUIRED_DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)