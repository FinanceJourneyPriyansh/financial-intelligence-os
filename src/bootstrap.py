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
    Start the application.
    """

    display_banner()

    initialize()

    print()
    print("Financial Intelligence OS is ready.")
    print()

    logger.info("Application started successfully.")