# FIOS Repository Inventory

## Purpose

This document is the single inventory of every folder and module in FIOS.

---

## Core Repository

- [ ] 00_control_center
- [ ] 01_src
- [ ] 02_data
- [ ] 03_docs
- [ ] 04_tests
- [ ] 05_dashboards
- [ ] 08_reports
- [ ] 09_logs
- [ ] 99_project
- [ ] fios_live

---

## For Every Folder Review

Record:

- Purpose
- Used By
- Depends On
- Keep
- Merge
- Move
- Archive
- Delete

---

## Rules

A folder survives only if it:

- Has a clear purpose.
- Is connected to the architecture.
- Will be used now or in the planned roadmap.

Otherwise:

- Merge
- Archive
- Delete

---

## Success Criteria

After restructuring:

- No duplicate folders
- No duplicate modules
- No orphan files
- Minimal folder depth
- Minimal file count
- Fully connected architecture
- Repository Brain understands every module
- Builder AI can maintain the repository automatically