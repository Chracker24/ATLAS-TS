import pandas as pd
import numpy as np
from atlas_f.models import simple_exponential_smoothing, calculate_prediction_intervals, double_exponential_smoothing

trending = pd.Series([87.5, 87.7, 87.9, 88.1, 88.3, 88.5])

for alpha in [0.1, 0.5, 0.9]:
    result = double_exponential_smoothing(trending, alpha=alpha, beta=0.3, horizon=3)
    print(f"Level: {result['level']:.2f}")
    print(f"Trend: {result['trend']:.2f}")
    print(f"Forecast: {[f'{x:.2f}' for x in result['forecast']]}")

    #Calculate intervals
    lower, upper = calculate_prediction_intervals(result['forecast'], result['residuals'], confidence=0.9)

    print(f"90% bounds : [{lower[0]:.2f}, {upper[0]:.2f}]")