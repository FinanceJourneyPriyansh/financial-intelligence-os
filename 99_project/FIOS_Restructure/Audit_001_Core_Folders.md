# Audit 001 — Core Repository

## Objective

Identify the purpose and future of every top-level folder.

No folder is assumed to be permanent.

---

| Folder | Purpose | Connected | Decision | Notes |
|---------|---------|-----------|----------|-------|
| 00_control_center | | | | |
| 01_src | | | | |
| 02_data | | | | |
| 03_docs | | | | |
| 04_tests | | | | |
| 05_dashboards | | | | |
| 08_reports | | | | |
| 09_logs | | | | |
| 99_project | | | | |
| fios_live | | | | |

---

## Decision Values

- KEEP
- MERGE
- MOVE
- ARCHIVE
- DELETE
- FUTURE

---

## Repository Goal

The final repository should contain only folders that directly support:

- FIOS Core
- FIOS Live
- Builder AI
- Repository Brain
- Dashboard
- Documentation
- Tests
- Reports

Everything else must justify its existence or be merged, archived, or removed.