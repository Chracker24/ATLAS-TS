import pandas as pd

def regime_persistance(
        instant : pd.Series,
        confirm : int = 3
) -> pd.Series:
    final_regime = []
    current_regime = "Unknown"
    counter = 0


    for regime in instant:
        if regime == "Unknown":
            final_regime.append("Unknown")
            current_regime = "Unknown"
            counter = 0

            continue

        if regime == current_regime:
            counter = 0
            final_regime.append(current_regime)
            continue
        
        #Determine Regime Change 

        candidate = regime
        if current_regime=="Unstable" and regime == "Stable":
            candidate = "Transitional"

        #Potential change in regime
        counter+=1

        if counter>= confirm:
            current_regime = candidate
            counter = 0


        final_regime.append(current_regime)


    return pd.Series(final_regime, index=instant.index)