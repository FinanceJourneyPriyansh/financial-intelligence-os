"""
============================================================
Financial Intelligence OS (FIOS)
Git Scanner
============================================================

Module:
    fios_live.scanners.git_scanner

Purpose:
    Collects Git repository information for the
    FIOS Live platform.

Responsibilities:
    - Current branch
    - Latest commit
    - Working tree status

This scanner never modifies the repository.

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

import subprocess

from fios_live.models.project_state import GitState


class GitScanner:
    """
    Collect Git repository information.
    """

    @staticmethod
    def _run_git_command(*args: str) -> str:
        """
        Execute a Git command and return its output.

        Returns an empty string if the command fails.
        """
        try:
            result = subprocess.run(
                ["git", *args],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
        ):
            return ""

    def scan(self) -> GitState:
        """
        Scan the Git repository.

        Returns:
            Populated GitState.
        """
        state = GitState()

        state.branch = self._run_git_command(
            "branch",
            "--show-current",
        )

        state.latest_commit = self._run_git_command(
            "rev-parse",
            "--short",
            "HEAD",
        )

        status = self._run_git_command(
            "status",
            "--porcelain",
        )

        state.clean = status == ""

        return state