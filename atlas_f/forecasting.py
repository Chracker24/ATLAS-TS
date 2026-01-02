import pandas as pd

def naive_forecast(self, series: pd.Series, horizon : int):
    last_value = series.iloc[-1]
    return [last_value] * horizon

def rolling_mean_forecast(series : pd.Series, window : int, horizon : int):
    rolling_mean = series.rolling(window=window).mean().iloc[-1]
    return [rolling_mean] * horizon