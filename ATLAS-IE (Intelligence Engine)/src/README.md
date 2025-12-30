# Source Architecture

The `src/` directory contains the full implementation of the ATLAS-IE engine.

The architecture is deliberately modular to ensure:
- clarity
- testability
- domain independence

---

## High-Level Modules

- `core/` — orchestration & confidence logic
- `regime/` — regime detection & persistence
- `explainability/` — reasoning & summaries

