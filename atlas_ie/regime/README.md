# Regime Detection System

This module handles all regime logic.

---

## Regime Types

- Unknown
- Unstable
- Transitional
- Stable

---

## Two-Stage Classification

1. **Instantaneous Regime**
   - reacts quickly
   - sensitive to variance

2. **Persistent Regime**
   - confirms stability
   - avoids noise-driven flips

---

## Files

- `regime_instantaneous.py`
- `regime_persistence.py`

---

## Why Persistence Matters

Without persistence:
- one spike = false instability
- one dip = false stability

