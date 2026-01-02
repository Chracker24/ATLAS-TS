def select_horizon(regime: str) -> int:
    if regime == "Stable":
        return 5
    elif regime == "Transitional":
        return 2
    else:
        return 0