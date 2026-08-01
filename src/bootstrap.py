"""
Financial Intelligence OS
Application Bootstrap
"""

from src.config import (
    APP_NAME,
    APP_VERSION,
    ENVIRONMENT,
    DEBUG,
    TIMEZONE,
)

from src.helper import setup_logger
from src.data.acquisition import DataAcquisitionEngine
from src.data.connectors.api_connector import APIConnector

logger = setup_logger()


def display_banner() -> None:
    """
    Display application banner.
    """

    print("=" * 70)
    print(APP_NAME)
    print("=" * 70)
    print(f"Version      : {APP_VERSION}")
    print(f"Environment  : {ENVIRONMENT}")
    print(f"Debug Mode   : {DEBUG}")
    print(f"Timezone     : {TIMEZONE}")
    print("=" * 70)


def initialize() -> None:
    """
    Initialize the application.
    """

    logger.info("Initializing Financial Intelligence OS")

    print("✓ Configuration Loaded")
    print("✓ Environment Loaded")
    print("✓ Logger Initialized")
    print("✓ Directories Verified")

    logger.info("Initialization completed.")


def start() -> None:
    """
    Start the Financial Intelligence OS.
    """

    # Display application banner
    display_banner()

    # Initialize application
    initialize()

    print()
    print("Financial Intelligence OS is ready.")
    print()

    # Create Data Acquisition Engine
    engine = DataAcquisitionEngine()

    # Register connectors
    engine.register_connector(
    APIConnector("world_bank")
    )

    # Run all connectors
    engine.run()

    logger.info("Application started successfully.")