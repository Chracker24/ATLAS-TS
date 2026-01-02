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
from .horizon import select_horizon
from .forecasting import rolling_mean_forecast, naive_forecast

class ATLASForecastEngine:
    def __init__(self, domain:str | None = None, window : int = 3):
        self.domain = domain
        self.window = window

    def forecast (self, atlas_ie_output : pd.DataFrame, anchor_index : int | None = None) -> dict:
        """
        Generate forecasts based on Intelligence Engine output

        Parameters:
        - atlas_ie_output : Dataframe by ATLAS-IE

        Returns:
        - Structured forecast output (dict)
        """

        if anchor_index is None:
            anchor_index = len(atlas_ie_output) - 1
        
        if anchor_index < 0 or anchor_index >= len(atlas_ie_output):
            raise IndexError("Anchor Index is out of bounds")
        
        atlas_ie_output = atlas_ie_output.iloc[:anchor_index + 1]
        # Forecasting permission given
        if "Forecasting_Allowed" not in atlas_ie_output.columns:
            raise ValueError("Input Dataframe must contain missing 'Forecasting_Allowed' column")

        if not atlas_ie_output["Forecasting_Allowed"].iloc[-1]:
            return {
                "forecast" : None,
                "horizon" : None,
                "uncertainty" : None,
                "regime" : atlas_ie_output["Regime_Final"].iloc[-1],
                "confidence" : atlas_ie_output["Confidence"].iloc[-1],
                "forecast_type" : None,
                "message" : "Forecasting blocked by Intelligence Engine"
            }

        #If nothing
        signal_col = atlas_ie_output.select_dtypes(include="number").columns[0]
        series = atlas_ie_output[signal_col]

        horizon = select_horizon(atlas_ie_output["Regime_Final"].iloc[-1])

        forecast = rolling_mean_forecast(series, window=self.window, horizon= horizon)
        return {
            "forecast" : forecast,
            "horizon" : horizon,
            "uncertainty" : None,
            "regime" : atlas_ie_output["Regime_Final"].iloc[-1],
            "confidence" : atlas_ie_output["Confidence"].iloc[-1],
            "forecast_type" : "baseline_mean",
            "message" : f"Baseline forecast from index {anchor_index}"
        }