"""
============================================================
Financial Intelligence OS (FIOS)
Repository Report
============================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fios_live.brain.models.repository_state import RepositoryState


class RepositoryReport:
    """
    Generates the Repository Brain report.
    """

    REPORT_NAME = "FIOS_Repository_Report.md"

    def generate(
        self,
        state: RepositoryState,
        output_directory: Path,
    ) -> Path:

        output_directory.mkdir(parents=True, exist_ok=True)

        report = output_directory / self.REPORT_NAME

        content = f"""# Financial Intelligence OS (FIOS)

# Repository Brain Report

Generated : {datetime.now():%Y-%m-%d %H:%M:%S}

---

## Repository

| Metric | Value |
|--------|------:|
| Folders | {state.total_folders} |
| Files | {state.total_files} |
| Python Files | {state.python_files} |
| Packages | {state.packages} |
| Modules | {state.modules} |
| Markdown | {state.markdown_files} |
| JSON | {state.json_files} |
| YAML | {state.yaml_files} |
| Tests | {state.tests} |

---

## Scores

| Metric | Score |
|--------|------:|
| Architecture | {state.architecture_score:.1f}% |
| Repository Health | {state.health_score:.1f}% |

---

## Architecture Issues

"""

        if state.architecture_issues:
            for issue in state.architecture_issues:
                content += f"- {issue}\n"
        else:
            content += "- None\n"

        content += "\n---\n\n## Recommendations\n\n"

        for recommendation in state.recommendations:
            content += f"- {recommendation}\n"

        content += """

---

Generated automatically by FIOS Repository Brain.
"""

        report.write_text(content, encoding="utf-8")

        return report