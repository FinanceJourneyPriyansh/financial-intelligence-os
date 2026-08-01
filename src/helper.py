"""
Helper Module
=============

Common helper functions used throughout the project.
"""

import logging
from datetime import datetime
from pathlib import Path


def create_directory(directory: Path) -> None:
    """
    Create a directory if it does not already exist.
    """
    directory.mkdir(parents=True, exist_ok=True)


def get_timestamp() -> str:
    """
    Return the current timestamp.

    Example:
        20260801_141530
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_logger(
    logger_name: str = "financial_intelligence_os",
    log_directory: Path = Path("logs"),
    log_level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure and return a logger.
    """

    create_directory(log_directory)

    log_file = log_directory / f"{logger_name}.log"

    logger = logging.getLogger(logger_name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger