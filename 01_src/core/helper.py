"""
Financial Intelligence OS
Helper Module

Purpose
-------
Provide common helper functions used throughout
Financial Intelligence OS.
"""

import logging
from datetime import datetime
from pathlib import Path


def create_directory(directory: Path) -> None:
    """
    Create a directory if it does not already exist.
    """

    directory.mkdir(parents=True, exist_ok=True)


def create_directories(*directories: Path) -> None:
    """
    Create multiple directories.
    """

    for directory in directories:
        create_directory(directory)


def get_timestamp() -> str:
    """
    Return the current timestamp.

    Example:
        20260804_101530
    """

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_logger(
    logger_name: str = "financial_intelligence_os",
    log_directory: Path = Path("logs"),
    log_level: int = logging.INFO,
) -> logging.Logger:
    """
    Create and configure a project logger.
    """

    create_directory(log_directory)

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    log_file = log_directory / f"{logger_name}.log"

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def print_separator(length: int = 70) -> None:
    """
    Print a separator line.
    """

    print("=" * length)


def print_title(title: str) -> None:
    """
    Print a formatted title.
    """

    print_separator()
    print(title)
    print_separator()