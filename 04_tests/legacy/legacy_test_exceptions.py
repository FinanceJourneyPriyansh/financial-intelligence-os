"""
Test Custom Exceptions
"""

from src.exceptions import (
    ConfigurationError,
    ConnectorError,
    DataValidationError,
    ExportError,
    DatabaseError,
    APIError,
    AuthenticationError,
)

print("=" * 70)
print("CUSTOM EXCEPTION TEST")
print("=" * 70)

tests = [
    ConfigurationError("Invalid configuration."),
    ConnectorError("World Bank connection failed."),
    DataValidationError("Dataset contains missing values."),
    ExportError("Export operation failed."),
    DatabaseError("Database connection failed."),
    APIError("API returned status code 500."),
    AuthenticationError("Authentication failed."),
]

for error in tests:
    try:
        raise error
    except Exception as e:
        print(f"✓ {type(e).__name__:<25} : {e}")

print("=" * 70)
print("All custom exceptions are working successfully.")
print("=" * 70)