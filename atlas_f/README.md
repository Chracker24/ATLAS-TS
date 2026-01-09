# ATLAS-F: Forecasting Module for Formula 1

## Overview
ATLAS-F is a forecasting engine designed to work with domain-agnostic data tested initially with Formula 1 race data. It leverages intelligence outputs from the ATLAS-IE (Intelligence Engine) to generate live, backtest, and scenario-based forecasts for race performance, strategy, and outcomes. ATLAS-F is modular, extensible, and built for integration with canonical datasets and analytical pipelines.

## How ATLAS-F Works
- **Input:** ATLAS-F requires processed data and intelligence outputs from ATLAS-IE. ATLAS-IE analyzes raw data, detects regimes, and computes confidence metrics, which are essential for accurate forecasting.
- **Processing:** ATLAS-F uses statistical models to forecast future race states, evaluate model quality, and provide confidence intervals and explanations for its predictions.
- **Output:** The engine returns detailed forecast results, including predicted values, bounds, model parameters, and interpretability insights.

## File Structure & Roles

### Main Files
- **`__init__.py`**: Initializes the module and exposes key classes/functions.
- **`explain.py`**: Contains functions for explaining model choices, forecast horizons, and quality assessments. Used to generate human-readable rationales for forecasts.
- **`forecast_engine.py`**: Implements the core `ATLASForecastEngine` class. Handles all forecasting logic, modes (live, backtest, scenario), and integration with ATLAS-IE outputs.
- **`forecasting.py`**: Provides lower-level forecasting algorithms and utilities used by the engine.
- **`horizon.py`**: Manages horizon selection logic, determining how far ahead forecasts should be made based on race regime and confidence.
- **`models.py`**: Defines statistical models used for forecasting, including parameter estimation and error metrics.

### How the Pieces Fit Together
1. **Data Preparation**: Race data is loaded and processed (typically via pandas DataFrames).
2. **Intelligence Engine (ATLAS-IE)**: The data is passed to ATLAS-IE, which analyzes the data, detects regimes (Stable, Transitional, Unstable), and computes confidence scores.
3. **Forecast Engine (ATLAS-F)**: The output from ATLAS-IE is fed into ATLAS-F, which selects appropriate models and forecasting horizons, runs predictions, and explains its choices.
4. **Results & Interpretation**: ATLAS-F returns a dictionary with forecast values, bounds, model details, and interpretability information. These results can be printed, visualized, or used for further analysis.

## Example Usage
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

## Forecast Modes
- **Live**: Forecasts from the latest available data point.
- **Backtest**: Forecasts from a specified historical anchor point, comparing predictions to actual outcomes.
- **Scenario**: Forecasts under hypothetical regime changes (e.g., "What if lap 15 was Unstable?" in the Formula 1 domain).

## Testing
- **Live**: [tests.testForecastLive](https://github.com/Chracker24/ATLAS-TS/blob/main/tests/testForecastLive.py)
- **BackTest**: [tests.testForecastBacktest](https://github.com/Chracker24/ATLAS-TS/blob/main/tests/testForecastBacktest.py)
- **Scenario**: [tests.testForecastScenario](https://github.com/Chracker24/ATLAS-TS/blob/main/tests/testForecastScenario.py)
- **Final All modes together**: [tests.testFinal](https://github.com/Chracker24/ATLAS-TS/blob/main/tests/testFinal.py)

## Integration with ATLAS-IE
ATLAS-F is tightly coupled with ATLAS-IE. It relies on ATLAS-IE for:
- Regime detection (race phase classification)
- Confidence scoring
- Preprocessing and feature extraction

This separation of concerns ensures that forecasting is always based on the most relevant and context-aware intelligence.

## Extending ATLAS-F
- Add new models in `models.py`
- Enhance horizon logic in `horizon.py`
- Improve interpretability in `explain.py`
- Integrate with new data sources or intelligence modules

## Summary
ATLAS-F is a robust, explainable forecasting engine for analytics. It is designed for modularity, interpretability, and seamless integration with the ATLAS-IE intelligence pipeline. Use it to generate actionable forecasts, test strategies, and explore race scenarios with confidence.