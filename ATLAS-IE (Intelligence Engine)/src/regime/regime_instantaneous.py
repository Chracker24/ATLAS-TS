import pandas as pd


def classify_regimes(
    rolling_variance: pd.Series,
    window: int,
    alpha: float = 1.2,
    beta: float = 2.0,
    baseline_method: str = "median",
    smooth_baseline: bool = False,
    smoothing_alpha: float = 0.3
) -> pd.Series:
    """
    Classify regimes based on rolling variance.

    Regimes:
    - Unknown
    - Stable
    - Transitional
    - Unstable
    """

    #Baseline
    baseline_window = rolling_variance.rolling(
        window=window,
        min_periods=window
    )

    # Baseline Methods
    if baseline_method == "median":
        baseline = baseline_window.median()
    elif baseline_method == "mean":
        baseline = baseline_window.mean()
    elif baseline_method == "q25":
        baseline = baseline_window.quantile(0.25)
    elif baseline_method == "q75":
        baseline = baseline_window.quantile(0.75)
    else:
        raise ValueError(f"Unknown baseline_method: {baseline_method}")

    # Optional Smoothing
    if smooth_baseline:
        baseline = baseline.ewm(alpha=smoothing_alpha, adjust=False).mean()

    # Instantaneous Regime Classifcation
    regimes = pd.Series("Unknown", index=rolling_variance.index)

    regimes[rolling_variance <= baseline * alpha] = "Stable"

    regimes[
        (rolling_variance > baseline * alpha) &
        (rolling_variance <= baseline * beta)
    ] = "Transitional"

    regimes[rolling_variance > baseline * beta] = "Unstable"

    #Return
    return regimes


