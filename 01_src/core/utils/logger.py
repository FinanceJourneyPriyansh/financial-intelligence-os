"""
Financial Intelligence OS
Logging Utilities
"""

import logging
from pathlib import Path


def get_logger(
    name: str = "financial_intelligence_os",
    log_directory: Path = Path("logs"),
) -> logging.Logger:
    """
    Create and return a configured logger.
    """

    log_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_directory / f"{name}.log",
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger