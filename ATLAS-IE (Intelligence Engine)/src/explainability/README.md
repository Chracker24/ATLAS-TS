# Explainability Engine

This module provides **human-readable explanations** for every engine decision.

---

## Reason Codes

Examples:
- NO_HIS — insufficient history
- UNST — unstable regime
- TR_PH — transitional phase
- TR_PRO — stabilizing trend
- VA_SP — variance spike
- REC — recovered stability
- STBL — stable phase

---

## Outputs

Each timestep includes:
- a list of reason codes
- a summarized explanation string

---

## Why This Matters

ATLAS-IE does not say:
> "Blocked"

It says:
> "Blocked — Unstable regime detected"

This makes decisions auditable and trustworthy.
