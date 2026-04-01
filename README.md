# ATLAS 🚀  
### Adaptive Time Series Intelligence & Forecasting System

ATLAS is a **multi-domain time-series decision intelligence framework** designed to **understand data before predicting it**.

> **Forecasting should never come before understanding.**

ATLAS separates *judgement* from *prediction* to ensure forecasts are **trustworthy, explainable, and context-aware**.

---

## 🧠 System Architecture

ATLAS is built around two sibling engines:

### 🔍 ATLAS-IE — Intelligence Engine
Evaluates the **behavioural state** of a time series before forecasting:
- Detects regimes (Unknown, Unstable, Transitional, Stable)
- Assigns confidence based on persistence
- Explicitly **permits or blocks forecasting**
- Produces explainable reason codes and summaries

ATLAS-IE is the **final authority** on data trustworthiness.

---

### 📊 ATLAS-F — Forecasting Engine *(in progress)*
Consumes ATLAS-IE outputs and:
- Forecasts **only when permitted**
- Adapts horizon and strategy to regime state
- Handles uncertainty and what-if scenarios
- Degrades or halts forecasts when stability collapses

ATLAS-F **never overrides intelligence decisions**.

---
### 🧾Data Sources
- Canonical datasets (see [Canonical Datasets](https://github.com/Chracker24/ATLAS-TS/tree/main/01_Data_Handling/Data/Canonical))
- Data collected via the **FastF1 API** for the F1 Domain
- Custom test scripts and scenarios

## 🌍 Domain-Agnostic by Design
ATLAS makes **no domain assumptions**.  
All logic is driven by the *relative behaviour* of the series itself.

Example domains:
- 🏎️ Motorsports telemetry  ✅
- 📈 Financial markets  
- 🏥 Epidemic/Pandemic Monitoring
---
## Structure of Project
```
ATLAS/
├── .gitignore
├── README.md
├── requirements.txt
├── __init__.py
├── 01_Data_Handling/
│   ├── Data/
│   │   ├── README.md
│   │   ├── Archive/
│   │   │   ├── season_2020.csv
│   │   │   ├── season_2021.csv
│   │   │   ├── season_2024.csv
│   │   │   └── season_2025.csv
│   │   └── Canonical/
│   │       └── lewisHamilton_AbuDhabi_2021.csv
│   ├── Notebooks/
│   │   ├── Canonical_Notebook/
│   │   │   └── AbuDhabi2021.ipynb
│   │   └── Data_Collection/
│   │       ├── cache/
│   │       │   └── 2021/
│   │       └── Formula1/
│   │           ├── 2021_Races.ipynb
│   │           └── 2020/
│   │               └── 2020_Races.ipynb
│   └── Scripts/
│       ├── cache/
│       │   ├── 2024/
│       │   └── 2025/
│       └── Ground Effect Era (Formula 1)/
│           ├── 2024_Races.py
│           └── 2025_Races.py
├── atlas_f/
│   ├── __init__.py
│   ├── explain.py
│   ├── forecast_engine.py
│   ├── forecasting.py
│   ├── horizon.py
│   ├── models.py
│   └── README.md
├── atlas_ie/
│   ├── __init__.py
│   ├── README.md
│   ├── core/
│   │   ├── __init__.py
│   │   ├── confidence.py
│   │   ├── engine.py
│   │   ├── index.py
│   │   ├── README.md
│   │   └── validation.py
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── explainability.py
│   │   └── README.md
│   └── regime/
│       ├── __init__.py
│       ├── README.md
│       ├── regime_instantaneous.py
│       └── regime_persistance.py
├── tests/
    ├── __init__.py
    ├── README.md
    ├── testDes.py
    ├── testEngine.py
    ├── testFinal.py
    ├── testForecast.py
    ├── testForecastBacktest.py
    ├── testForecastLive.py
    ├── testForecastScenario.py
    └── testSes.py
```
## 🚦 Quickstart Examples

```python
import pandas as pd
from atlas_ie.core.engine import ATLASIntelligenceEngine as IE
from atlas_f.forecast_engine import ATLASForecastEngine as FE

df = pd.read_csv("01_Data_Handling/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
ie_engine = IE(domain="f1")
ie_output = ie_engine.run(df)
f_engine = FE(domain="f1")
result = f_engine.forecast(ie_output, mode="live")
print(result)
```

## Running tests
Run any test script using:
``` python -m tests.test<suffix>```

For Example:
```
python -m tests.testForecastLive
python -m tests.testFinal
python -m tests.testEngine
```

## 🎯 Project Focus
ATLAS demonstrates:
- System-level ML engineering
- Explicit authority boundaries
- Explainability over blind prediction
- Governance-first forecasting design

**ATLAS decides *when* forecasting makes sense — before forecasting ever begins.**

