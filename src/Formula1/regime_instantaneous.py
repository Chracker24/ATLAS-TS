import pandas as pd

def classify_regimes(
    rolling_variance: pd.Series,
    window: int,
    alpha: float = 1.2,
    beta: float = 2.0
) -> pd.Series:
    """
    Classify regimes based on rolling variance.

    Returns:
    - Too Early
    - Stable
    - Transitional
    - Unstable
    """

    baseline = rolling_variance.rolling(
        window=window,
        min_periods=window
    ).median()

    regimes = pd.Series("Too Early", index=rolling_variance.index)

    regimes[rolling_variance <= baseline * alpha] = "Stable"
    regimes[
        (rolling_variance > baseline * alpha) &
        (rolling_variance <= baseline * beta)
    ] = "Transitional"
    regimes[rolling_variance > baseline * beta] = "Unstable"

    return regimes

