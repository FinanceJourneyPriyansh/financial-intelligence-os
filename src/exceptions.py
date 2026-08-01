"""
Custom Exceptions
=================

Centralized exception classes for the Financial Intelligence OS.
"""


class FinancialIntelligenceError(Exception):
    """
    Base exception for the project.
    """

    pass


class ConfigurationError(FinancialIntelligenceError):
    """
    Raised when configuration is invalid.
    """

    pass


class ConnectorError(FinancialIntelligenceError):
    """
    Raised when a data connector fails.
    """

    pass


class DataValidationError(FinancialIntelligenceError):
    """
    Raised when data validation fails.
    """

    pass


class ExportError(FinancialIntelligenceError):
    """
    Raised when exporting data fails.
    """

    pass