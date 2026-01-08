# Core Engine Logic

This module contains the orchestration logic for ATLAS-IE.

---

## Responsibilities

- Input validation
- Rolling statistics computation
- Sensitivity configuration
- Confidence calculation
- Forecasting gatekeeping

---

## Key Files

- `engine.py` — main MTSEngine class
- `confidence.py` — confidence scoring & gating
- `validation.py` — input sanity checks

---

## Design Notes

The engine is:
- stateless
- deterministic
- purely data-driven

No domain knowledge is encoded here and therefore the whole engine is **Domain-Agnostic**
