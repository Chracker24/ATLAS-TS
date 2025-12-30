# ATLAS-IE  
**Multi-Domain Time Series Intelligence Engine**

ATLAS-IE is a **stateless, rolling-statistics intelligence engine** designed to evaluate whether a time series is suitable for forecasting.

It decides **if prediction is allowed**.

---

## What ATLAS-IE Does

For any numeric time series, ATLAS-IE:

1. Computes rolling statistics
2. Detects variance-based regimes
3. Confirms regime persistence
4. Assigns confidence scores
5. Produces human-readable confidence bands
6. Explains every decision with explicit reasons

---

## Regime States

- **Unknown** — insufficient history
- **Unstable** — high or chaotic variance
- **Transitional** — stabilizing or degrading
- **Stable** — low, persistent variance

---

## Confidence Bands

| Band        | Meaning |
|-------------|--------|
| BLOCKED     | Forecasting forbidden |
| CAUTION     | Forecasting unreliable |
| KEEP AN EYE | Monitor before forecasting |
| PERMITTED   | Forecasting allowed |

---

## Sensitivity Profiles

ATLAS-IE supports three sensitivity modes:

- **strict** — conservative, low tolerance
- **normal** — balanced (default)
- **loose** — exploratory, permissive

Each mode controls variance thresholds and confirmation depth.

---

## Output

The engine returns a fully enriched DataFrame including:
- rolling statistics
- regime classification
- confidence score
- forecasting permission
- explanations and summaries

This output is designed for:
- humans
- visualizations
- downstream forecasting engines

---

## Why This Exists

Most forecasting systems fail because they:
- assume stationarity
- ignore regime changes
- provide no justification

ATLAS-IE exists to prevent those failures.
