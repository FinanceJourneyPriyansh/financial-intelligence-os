# Financial Intelligence OS (FIOS)

# FIOS Live Architecture

Version: 2.0

Status: Canonical Architecture

---

# Purpose

FIOS Live is the operating layer of the Financial Intelligence OS.

It provides the continuously running runtime connection between the
FIOS Kernel, Repository Brain, Monitoring Platform, Builder Integration
Platform, Automation, and Web Dashboard.

FIOS Live does not duplicate repository scanners, project-state models,
audit engines, dashboard engines, or business logic.

The repository is analyzed through one canonical Repository Brain.

The Kernel owns runtime coordination.

The Web layer consumes Kernel state.

---

# Canonical Architecture

```text
                         FIOS
                          │
                          ▼
                    fios.py
                          │
                          ▼
                    FIOS Kernel
                          │
                          ▼
                   ServiceManager
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
   Repository Brain   Monitoring      Builder Integration
          │           Platform            Platform
          │                                │
          │                                ▼
          │                            Automation
          │
          ├── Repository Mapper
          ├── Architecture Analyzer
          ├── Dependency Analyzer
          ├── Code Analyzer
          ├── Documentation Analyzer
          ├── Repository Health
          └── Builder AI
          │
          ▼
   Repository Runtime State
          │
          ├───────────────┐
          │               │
          ▼               ▼
   Repository Report   Kernel State
                          │
                          ▼
                     FIOS Web Layer
                          │
                          ▼
                    Live Dashboard