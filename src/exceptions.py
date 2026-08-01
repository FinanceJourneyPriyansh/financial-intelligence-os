"""
Financial Intelligence OS
Custom Exception Module

This module defines all project-specific exceptions.
"""


class FinancialIntelligenceError(Exception):
    """
    Base exception class for the Financial Intelligence OS.
    """

    def __init__(self, message: str = "Financial Intelligence OS Error"):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(FinancialIntelligenceError):
    """Raised when configuration is invalid."""


class ConnectorError(FinancialIntelligenceError):
    """Raised when a data connector fails."""


class DataValidationError(FinancialIntelligenceError):
    """Raised when dataset validation fails."""


class ExportError(FinancialIntelligenceError):
    """Raised when exporting data fails."""


class DatabaseError(FinancialIntelligenceError):
    """Raised for database-related errors."""


class APIError(FinancialIntelligenceError):
    """Raised for API-related errors."""


class AuthenticationError(FinancialIntelligenceError):
    """Raised when authentication fails."""