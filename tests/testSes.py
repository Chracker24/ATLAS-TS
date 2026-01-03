import pandas as pd
import numpy as np
from atlas_f.models import simple_exponential_smoothing, calculate_prediction_intervals

data = pd.Series([87.5, 87.6, 87.4, 87.7, 87.5, 87.6, 87.8, 87.7, 87.9, 88.0])

for alpha in [0.1, 0.5, 0.9]:
    result = simple_exponential_smoothing(data, alpha = alpha, horizon = 3)
    print(f"\n Alpha = {alpha}")
    print(f"Final Level : {result['level']:.3f}")
    print(f"Forecast: {result['forecast']}")

    #Calculate intervals
    lower, upper = calculate_prediction_intervals(result['forecast'], result['residuals'], confidence=0.9)

    print(f"90% bounds : [{lower[0]:.2f}, {upper[0]:.2f}]")