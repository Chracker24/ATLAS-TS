"""
Forecasting models for ATLAS-Forecasting

Starting with Simply Exponential Smoothing (SES)
"""

import pandas as pd
import numpy as np


def simple_exponential_smoothing(
        series : pd.Series,
        alpha : float = 0.3,
        horizon : int = 3
) -> dict:
    """
    Simple Exponential Smoothing
    Args :
    series : Time Series data
    alpha : smoothing parameter 
     - High : responsive to recent changes
     - Low : Stable, smooths out noise
    Horizon : Number of steps to forecast ahead


    Returns: 
    a dict with :
     - "forecast" : List of predicted values
     - "level" : Final Smoothed Level
     - "fitted" : Fitted values for historical data
    """
    values = series.values
    n = len(values)

    level = values[0]
    fitted = [level]

    for i in range (1, n):
        level = alpha * values[i] + (1 - alpha) * level
        fitted.append(level)

    forecast = [level] * horizon

    residuals= values [1:] - np.array(fitted[:-1])


    return {
        'forecast' : forecast,
        'level' : level,
        'fitted' : fitted,
        'residuals' : residuals
    }


def calculate_prediction_intervals(
forecast : list,
residuals : pd.Series,
confidence: float = 0.9
) -> tuple:
    """
    Calculate the lower and upper prediction bounds

    Args:
        forecast : Point forecasts
        residuals : Historical forecast errors
        confidence : Confidence level

    Returns :
        (lower_bounds, upper_bounds)
    """


    std_error = np.std(residuals)

    if confidence==0.9:
        z = 1.645
    elif confidence == 0.95:
        z = 1.96
    else:
        z = 1.645

    horizon = len(forecast)
    lower_bound = []
    upper_bound = []

    for h in range(horizon):
        margin = z * std_error * np.sqrt(h + 1)

        lower_bound.append(forecast[h] - margin)
        upper_bound.append(forecast[h] + margin)

    return lower_bound, upper_bound


def double_exponential_smoothing(
    series : pd.Series,
    alpha : float = 0.3,
    beta : float = 0.1,
    horizon : int = 5        
) -> dict :
    """  
    Double Exponential Smoohting (Holt's Method)
    Captures both level and trend for better forecasting


    Args:
        series : Time Series data
        alpha : level Smoothing 
        beta : trend Smoothing
        Horizon : Forecast steps


    Returns :
        dict : containing same as simple exponential smoothing but with trend added
    """

    values = series.values
    n=len(values)
    level = values[0]
    trend = values[1] - values[0]
    fitted = [level]


    for i in range(1, n):
        prev_level = level

        level = alpha * values[i] + (1 - alpha) * (level+trend)

        trend = beta + (level - prev_level) + (1-beta) * trend

        fitted.append(level)

    forecast = []
    for h in range(1, horizon+1):
        forecast.append(level + h * trend)

    residuals = values[1:] - np.array(fitted[:-1])

    return {
        'forecast' : forecast,
        'level' : level,
        'trend' : trend,
        'fitted' : fitted,
        'residuals' : residuals
    }
