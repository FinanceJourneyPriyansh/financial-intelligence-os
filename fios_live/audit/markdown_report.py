"""
============================================================
Financial Intelligence OS (FIOS)
Markdown Report Generator
============================================================

Module:
    fios_live.audit.markdown_report

Purpose:
    Generates a Markdown audit report from the current
    FIOS runtime state.

Responsibilities:
    - Generate FIOS_System_Audit.md
    - Present project information in Markdown
    - Save report to disk

Author:
    Priyansh Soni

Project:
    Financial Intelligence OS (FIOS)
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fios_live.analyzers.fios_analyzer import FIOSAnalyzer
from fios_live.models.fios_state import FIOSState


class MarkdownReport:
    """
    Generates the primary Markdown audit report.
    """

    REPORT_NAME = "FIOS_System_Audit.md"

    def generate(
        self,
        state: FIOSState,
        output_directory: Path,
    ) -> Path:
        """
        Generate the Markdown audit report.

        Args:
            state:
                Current FIOS runtime state.

            output_directory:
                Directory where the report will be written.

        Returns:
            Path to the generated report.
        """

        analyzer = FIOSAnalyzer()
        platform = analyzer.analyze(state)

        output_directory.mkdir(parents=True, exist_ok=True)

        report_path = output_directory / self.REPORT_NAME

        report = f"""# Financial Intelligence OS (FIOS)

## System Audit Report

---

### Report Information

| Item | Value |
|------|-------|
| Generated | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
| Health Score | {state.health.score:.0f}% |
| Health Status | {state.health.status} |

---

# Executive Summary

Overall Platform Status

**{platform.overall}**

---

# Repository

| Metric | Value |
|---------|------:|
| Folders | {state.project.statistics.total_folders} |
| Files | {state.project.statistics.total_files} |

---

# Python Source

| Metric | Value |
|---------|------:|
| Python Files | {state.project.source.python_files} |
| Packages | {state.project.source.packages} |
| Modules | {state.project.source.modules} |

---

# Documentation

| Metric | Value |
|---------|------:|
| Markdown Files | {state.project.documentation.markdown_files} |
| README Files | {state.project.documentation.readme_files} |

---

# Git

| Metric | Value |
|---------|-------|
| Branch | {state.project.git.branch} |
| Commit | {state.project.git.latest_commit} |
| Working Tree | {"Clean" if state.project.git.clean else "Modified"} |

---

# Platform Status

| Component | Status |
|-----------|--------|
| Foundation | {platform.foundation} |
| Platform Core | {platform.platform_core} |
| Builder | {platform.builder} |
| Runtime | {platform.runtime} |
| FIOS Live | {platform.fios_live} |
| Documentation | {platform.documentation} |
| Tests | {platform.tests} |

---

# Recommendations

- Continue improving subsystem health.
- Keep the repository clean before releases.
- Run FIOS Live regularly to monitor platform status.

---

*Generated automatically by Financial Intelligence OS (FIOS) Live.*
"""

        report_path.write_text(
            report,
            encoding="utf-8",
        )

        return report_path