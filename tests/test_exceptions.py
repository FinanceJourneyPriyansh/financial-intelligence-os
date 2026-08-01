"""
Test Custom Exceptions
"""

from src.exceptions import (
    ConfigurationError,
    ConnectorError,
    DataValidationError,
    ExportError,
)

print("=" * 60)
print("CUSTOM EXCEPTION TEST")
print("=" * 60)

try:
    raise ConfigurationError("Invalid configuration.")
except ConfigurationError as error:
    print(f"✓ {error}")

try:
    raise ConnectorError("World Bank API unavailable.")
except ConnectorError as error:
    print(f"✓ {error}")

try:
    raise DataValidationError("Dataset contains missing values.")
except DataValidationError as error:
    print(f"✓ {error}")

try:
    raise ExportError("CSV export failed.")
except ExportError as error:
    print(f"✓ {error}")

print("=" * 60)
print("All custom exceptions are working correctly.")
print("=" * 60)