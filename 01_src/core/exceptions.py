"""
Financial Intelligence OS
Custom Exceptions

Purpose
-------
Define all custom exceptions used throughout
Financial Intelligence OS.
"""


class FinancialIntelligenceError(Exception):
    """
    Base exception for Financial Intelligence OS.
    """

    def __init__(self, message: str = "Financial Intelligence OS Error"):
        super().__init__(message)


class ConfigurationError(FinancialIntelligenceError):
    """
    Raised when application configuration is invalid.
    """


class InitializationError(FinancialIntelligenceError):
    """
    Raised when application initialization fails.
    """


class ValidationError(FinancialIntelligenceError):
    """
    Raised when validation fails.
    """


class DataValidationError(ValidationError):
    """
    Raised when data validation fails.
    """


class ConnectorError(FinancialIntelligenceError):
    """
    Raised when a data connector fails.
    """


class APIError(FinancialIntelligenceError):
    """
    Raised when an external API request fails.
    """


class DatabaseError(FinancialIntelligenceError):
    """
    Raised for database-related errors.
    """


class AuthenticationError(FinancialIntelligenceError):
    """
    Raised when authentication or authorization fails.
    """


class ExportError(FinancialIntelligenceError):
    """
    Raised when exporting data fails.
    """


class GeneratorError(FinancialIntelligenceError):
    """
    Raised when a generator fails.
    """


class AutomationError(FinancialIntelligenceError):
    """
    Raised when an automation task fails.
    """


class MonitoringError(FinancialIntelligenceError):
    """
    Raised when monitoring fails.
    """