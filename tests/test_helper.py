from src.helper import (
    create_directory,
    get_timestamp,
    setup_logger,
)

from pathlib import Path

print("=" * 60)
print("HELPER MODULE TEST")
print("=" * 60)

print("Timestamp:")
print(get_timestamp())

print()

print("Creating test directory...")

create_directory(Path("logs/test"))

print("Done!")

logger = setup_logger()

logger.info("Helper module test successful.")

print()

print("Log file created successfully.")
print("=" * 60)