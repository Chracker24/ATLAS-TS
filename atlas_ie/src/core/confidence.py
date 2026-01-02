import pandas as pd

def confidenceScore(
        regimeScore : pd.Series,
        window : int = 3,
        min_periods : int = 1
)->pd.Series:
    """
    Takes in a Series of Regime Classifications and 

    Returns : a Series of Confidence Scores (0-1)
    """

    confidenceMap = {
        "Unknown" : 0.0,
        "Unstable" : 0.1,
        "Transitional" : 0.5,
        "Stable" : 0.9
    }

    base_confidence = regimeScore.map(confidenceMap).fillna(0.0)

    #Smoothed Confidence Scores
    confidence_smoothed = base_confidence.rolling(window=window, min_periods = min_periods).mean()

    return confidence_smoothed

def forecastingAllowed(
        confidence : pd.Series,
        threshold : float = 0.7,
        window : int = 5
)->pd.Series:
    """
    Based on the confidence level,
    Returns a boolean indicating if forecasting is allowed
    """

    forecastAllowed = []
    for i in confidence:
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