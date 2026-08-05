"""
FIOS Builder
Release Document Generator Test
"""

import sys

sys.path.insert(0, "01_src")

from platform_core.automation.release import ReleaseDocumentGenerator


def main():

    print("=" * 60)
    print("FIOS Builder Release Document Generator Test")
    print("=" * 60)

    generator = ReleaseDocumentGenerator()

    generator.generate_all()

    print()
    print("=" * 60)
    print("DOCUMENT GENERATION SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()