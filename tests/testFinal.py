"""
Test ATLAS-F on F1 data with all 3 modes.
"""

import pandas as pd
from atlas_ie.src.core.engine import ATLASIntelligenceEngine as IE
from atlas_f.forecast_engine import ATLASForecastEngine as FE


# === LOAD DATA ===
df_raw = pd.read_csv("atlas_ie/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
df = df_raw[["LapTime"]]

# Run IE
ie_engine = IE(domain="f1")
ie_output = ie_engine.run(df)

# Create F engine
f_engine = FE(domain="f1")


# === TEST 1: LIVE FORECAST ===
print("=" * 60)
print("TEST 1: LIVE FORECAST (from latest data)")
print("=" * 60)

result_live = f_engine.forecast(ie_output, mode="live")

print(f"Status: {result_live['status']}")
print(f"Regime: {result_live['regime']}")
print(f"Confidence: {result_live['confidence']:.1%}")
print(f"Horizon: {result_live.get('horizon', 0)} laps")

if result_live['status'] == "PERMITTED":
    print(f"\nModel: {result_live['model']}")
    print(f"Parameters: α={result_live['parameters']['alpha']:.2f}, β={result_live['parameters'].get('beta', 'N/A')}")
    print(f"\nForecast: {[f'{x:.2f}' for x in result_live['forecast_values']]}")
    print(f"90% Bounds: {[f'{x:.2f}' for x in result_live['lower_bounds']]} to {[f'{x:.2f}' for x in result_live['upper_bounds']]}")
    print(f"\nWhy this horizon: {result_live['why_this_horizon']}")
    print(f"Why this model: {result_live['why_this_model']}")
    print(f"Quality: {result_live['forecast_quality']}")
else:
    print(f"\nReaons: {result_live['message']}")


# === TEST 2: BACKTEST (Lap 83 - Middle of Stable Period) ===
print("\n\n" + "=" * 60)
print("TEST 2: BACKTEST (from lap 83 - stable period)")
print("=" * 60)
engine = FE(domain="f1")
result_backtest = engine.forecast(ie_output, mode="backtest", anchor_index=111)

print(f"Status: {result_backtest['status']}")
print(f"Forecasting from lap: {result_backtest['anchor_index']}")
print(f"Regime: {result_backtest['regime']}")
if result_backtest['reasons']:
    print(f"Reasons: {result_backtest['message']}")

if result_backtest['status'] == "PERMITTED":
    print(f"\nForecast: {[f'{x:.2f}' for x in result_backtest['forecast_values'][:5]]}")
    print(f"Actual:   {[f'{x:.2f}' for x in result_backtest.get('actual_values', [])[:5]]}")
    
    if 'forecast_error' in result_backtest:
        print(f"\nForecast Errors:")
        print(f"  MAE:  {result_backtest['forecast_error']['MAE']:.3f}")
        print(f"  RMSE: {result_backtest['forecast_error']['RMSE']:.3f}")
        print(f"  MAPE: {result_backtest['forecast_error']['MAPE']:.2f}%")


# === TEST 3: SCENARIO (What if Unstable at lap 80?) ===
print("\n\n" + "=" * 60)
print("TEST 3: SCENARIO (What if lap 80 was Unstable?)")
print("=" * 60)

# Slice to lap 80
ie_slice = ie_output.iloc[:81].copy()

result_scenario = f_engine.forecast(ie_slice, mode="scenario", scenario_regime="Unstable")

print(f"Status: {result_scenario['status']}")
print(f"Overridden regime: {result_scenario['regime']}")

if result_scenario['status'] == "BLOCKED":
    print(f"Reasons: {result_scenario['message']}")
else:
    print(f"Forecast: {result_scenario['forecast_values']}")


print("\n" + "=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)