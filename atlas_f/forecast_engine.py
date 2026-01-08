"""
Docstring for ATLAS-F (Forecasting).forecast_engine

This module contain the main engin for the ATLAS-F (forecasting) system.

It ingests 
1. time-series data in a pandas DataFrame
2. Regime final from persistance Regime Classification in ATLAS-IE (Intelligence Engine)
3. Confidence scores from ATLAS-IE
4. Domain information and
5. Forecasting Allowed - parameter to tell the forecasting engin whether it is valid to produce forecasts for the given input data.


Forecast Modes:

1. Conditional Forecast : Forecast how wherever the regime has classified as "Keep an Eye" or "Permitted" for Forecasting in Forecasting_Allowed to understand how the data could've moved
2. Transitional Forecast : Forecast how the data would move next after the time-series data has ended as input
3. What if Analysis : User defined scenarios and spaces where the user can use the engine to forecast in a specfic time.
"""

import pandas as pd
import numpy as np
from .horizon import select_horizon, get_model_params, explain_horizon
from .forecasting import rolling_mean_forecast, naive_forecast
from .models import simple_exponential_smoothing, double_exponential_smoothing, calculate_prediction_intervals
from .explain import _assess_quality, _explain_model_choice, _calculate_errors


class ATLASForecastEngine:
    def __init__(self, domain:str | None = None, window : int = 3, confidence : float  = 0.9):
        self.domain = domain
        self.window = window
        self.confidence = confidence

    def forecast (self, atlas_ie_output : pd.DataFrame, anchor_index : int | None = None, scenario_regime : str | None = None, mode : str = "live") -> dict:
        """
        Generate forecasts based on Intelligence Engine output

        Parameters:
        - atlas_ie_output : Dataframe by ATLAS-IE
        - anchor_index : index to get forecast from
        - regime : the regime data classified
        - mode : type of forecasting
         - live : forecasts what is going to happen next
         - backtest : forecasts the possible scenarios at a certain point of time
         - scenario : forecasts what wouldve happen under a different regime 

        Returns:
        - Structured forecast output (dict)
        """
        
        if mode == "live": 
            anchor_index = len(atlas_ie_output) - 1
        elif mode == "backtest":
            if anchor_index is None:
                raise ValueError("Backtest mode requires Anchor Index")
            if anchor_index < 0 or anchor_index >= len(atlas_ie_output):
                raise IndexError(f"Anchor Index {anchor_index} out of bounds")
        elif mode == "scenario":
            if scenario_regime is None:
                raise ValueError("Scenario mode needs a Regime")
            anchor_index = len(atlas_ie_output) - 1
        else:
            raise ValueError(f"Unknown Mode '{mode}'. Use 'live', 'backtest' or 'scenario'")
        
        data_slice = atlas_ie_output.iloc[:anchor_index + 1].copy()
        required_cols = ["Regime", "Confidence", "Forecasting_Allowed"]
        missing = [c for c in required_cols if c not in data_slice.columns]
        if missing:
            raise ValueError(f"Missing required columns : {missing}")

        regime = scenario_regime if scenario_regime else data_slice["Regime"].iloc[-1]
        confidence = data_slice["Confidence"].iloc[-1]
        forecasting_allowed = data_slice["Forecasting_Allowed"].iloc[-1]
        signal_col = data_slice.select_dtypes(include="number").columns[0]
        series = data_slice[signal_col]
        block_reasons = []

        if not forecasting_allowed:
            block_reasons.append("ATLAS-IE blocked forecasting")

        if regime in ["Unstable","Unknown"]:
            block_reasons.append(f"{regime} regime detected")

        if confidence < 0.5:
            block_reasons.append(f"Low Confidence ({confidence:.1%})")

        if self.domain == 'f1' and series.iloc[-1] > 95:
            block_reasons.append(f"Anomalous lap time ({series.iloc[-1]:.1f}s)")

        if block_reasons:
            return self._blocked_response(
                regime = regime, 
                confidence = confidence,
                anchor_index=anchor_index,
                reasons=block_reasons,
                mode = mode
            )

        horizon = select_horizon(regime, self.domain) 

        if horizon == 0:
            return self._blocked_response(
                regime = regime, 
                confidence = confidence,
                anchor_index=anchor_index,
                reasons=[f"Zero Horizon for {regime} regime"], 
                mode = mode
            )

        params = get_model_params(regime, self.domain) 
        alpha = params["alpha"]
        beta = params["beta"]

        if regime == "Stable": 
            result = simple_exponential_smoothing(series, alpha = alpha, horizon = horizon)
            model_used = "Simple Exponential Smoothing"

        else:
            result = double_exponential_smoothing(series, alpha=alpha, beta=beta, horizon=horizon)
            model_used = "Double Exponential Smoothing (Holt's method)"


        lower_bounds, upper_bounds = calculate_prediction_intervals(
            result['forecast'],
            result['residuals'],
            confidence=self.confidence
        )

        response = {
            "status" : "PERMITTED",
            "mode" : mode, 
            "anchor_index" : anchor_index,
            "regime" : regime,
            "confidence" : float(confidence),
            "domain" : self.domain,

            "horizon" : horizon,
            "forecast_values" : [float(f) for f in result['forecast']],
            "lower_bounds" : [float(l) for l in lower_bounds],
            "upper_bounds" : [float(u) for u in upper_bounds],

            "model": model_used,
            "parameters" : {
                "alpha" : alpha,
                "beta" : beta if 'trend' in result else None
            },
            'level' : float(result['level']),
            'trend' : float(result.get('trend', 0.0)),

            "why_this_horizon" : explain_horizon(regime, self.domain),
            "why_this_model"  : _explain_model_choice(regime),
            "forecast_quality" : _assess_quality(result['residuals'], confidence)
        }

        # backtest section
        if mode == "backtest":
            actual_end = min(anchor_index + horizon + 1, len(atlas_ie_output))
            if actual_end > anchor_index + 1:
                actual_values = atlas_ie_output[signal_col].iloc[anchor_index+1:actual_end].tolist()
                response["actual_values"] = actual_values
                response["forecast_error"] = _calculate_errors(
                    result['forecast'][:len(actual_values)],
                    actual_values
                )

        return response

    def _blocked_response(
            self,
            regime : str,
            confidence: float,
            anchor_index: int,
            reasons:list,
            mode: str
    ) -> dict:
        #Generate reponse for blocked forecasting

        return {
            'status' : 'BLOCKED',
            'mode' : mode,
            'anchor_index' : anchor_index,
            'regime' : regime,
            'confidence' : float(confidence),
            'domain' : self.domain,
            'horizon' : 0,
            'forecast_values' : None,
            'reasons' : reasons,
            'message' : 'Forecasting Blocked: ' + ';'.join(reasons) 
        }
    
