import pandas as pd

def confidenceScore(
        regimeScore : pd.Series,
)->pd.Series:
    """
    Takes in a Series of Regime Classifications and 

    Returns : a Series of Confidence Scores (0-1)
    """

    confidenceMap = {
        "Unknown" : 0.0,
        "Unstable" : 0.1,
        "Transitional" : 0.4,
        "Stable" : 0.9
    }

    return regimeScore.map(confidenceMap).fillna(0.0)


def forecastingAllowed(
        confidence : pd.Series,
        threshold : float = 0.7,
        window : int = 5
)->pd.Series:
    """
    Based on the confidence level,
    Returns a boolean indicating if forecasting is allowed
    """

    forecast = confidence.rolling(window=window-2, min_periods=window-2).min()
    forecastAllowed = []
    for i in forecast:
        if pd.isna(i):
            forecastAllowed.append(False)
        else:
            forecastAllowed.append(i >= threshold)
    
    

    return pd.Series(forecastAllowed, index=confidence.index)

def confidenceBand(confidence: pd.Series) -> pd.Series:
    bandScore = []
    for con in confidence:
        if con < 0.2:
            bandScore.append("Blocked")
        elif con < 0.5:
            bandScore.append("Caution")
        elif con < 0.7:
            bandScore.append("Keep an Eye")
        else:
            bandScore.append("Permitted")

    return pd.Series(bandScore, index=confidence.index)