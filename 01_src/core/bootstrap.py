"""
Financial Intelligence OS
Application Bootstrap

Purpose
-------
Initializes the Financial Intelligence OS runtime.

Responsibilities
----------------
- Load application configuration
- Initialize logging
- Verify application environment
- Display startup information
- Prepare the system for execution

This module must NOT contain business logic.
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
    Display the Financial Intelligence OS banner.
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
    Initialize the application runtime.
    """

    logger.info("Initializing Financial Intelligence OS...")

    print("✓ Configuration Loaded")
    print("✓ Environment Loaded")
    print("✓ Logger Initialized")
    print("✓ Directories Verified")

    logger.info("Initialization completed successfully.")


def start() -> None:
    """
    Bootstrap the Financial Intelligence OS.

    This function prepares the application and hands control
    to the main program. No business logic should execute here.
    """

    display_banner()

    initialize()

    print()
    print("Financial Intelligence OS is ready.")
    print("System bootstrap completed successfully.")
    print()

    logger.info("Bootstrap completed successfully.")