"""
Test Configuration Module
"""

from src.config import (
    PROJECT_ROOT,
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
)

print("=" * 70)
print("FINANCIAL INTELLIGENCE OS - CONFIGURATION TEST")
print("=" * 70)

print(f"Project Root     : {PROJECT_ROOT}")
print(f"Data Directory   : {DATA_DIR}")
print(f"Raw Data         : {RAW_DATA_DIR}")
print(f"Interim Data     : {INTERIM_DATA_DIR}")
print(f"Processed Data   : {PROCESSED_DATA_DIR}")
print(f"External Data    : {EXTERNAL_DATA_DIR}")
print(f"Logs             : {LOGS_DIR}")
print(f"Models           : {MODELS_DIR}")
print(f"Reports          : {REPORTS_DIR}")
print(f"Notebooks        : {NOTEBOOKS_DIR}")
print(f"Docs             : {DOCS_DIR}")
print(f"Dashboards       : {DASHBOARDS_DIR}")

print("=" * 70)
print("Configuration loaded successfully.")
print("=" * 70)