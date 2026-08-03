"""
Financial Intelligence OS
Filesystem Utilities
"""

from pathlib import Path


def ensure_directory(directory: Path) -> None:
    """
    Create a directory if it does not exist.
    """

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


def ensure_directories(*directories: Path) -> None:
    """
    Create multiple directories.
    """

    for directory in directories:
        ensure_directory(directory)


def file_exists(path: Path) -> bool:
    """
    Check whether a file exists.
    """

    return path.exists()