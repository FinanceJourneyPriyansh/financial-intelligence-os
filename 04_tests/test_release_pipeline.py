"""
Financial Intelligence OS (FIOS)
Builder Automation Platform

Release Pipeline Integration Test
"""

import sys

sys.path.insert(0, "01_src")

from platform_core.automation.release import ReleasePipeline


def main():

    print("=" * 60)
    print("FIOS Builder Release Pipeline Test")
    print("=" * 60)

    pipeline = ReleasePipeline()

    pipeline.register_default_stages()

    result = pipeline.execute()

    print()

    print("Completed Stages")
    print("-" * 60)

    for stage in result.completed:
        print(f"PASS  {stage}")

    if result.failed:

        print()
        print("Failed Stages")
        print("-" * 60)

        for stage in result.failed:
            print(f"FAIL  {stage}")

    print()
    print("=" * 60)

    if not result.failed:
        print("RELEASE PIPELINE PASSED")
    else:
        print("RELEASE PIPELINE FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()