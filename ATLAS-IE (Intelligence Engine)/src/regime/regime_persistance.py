import pandas as pd

def regime_persistance(
        instant : pd.Series,
        confirm : int = 3,
        decay : int = 1
) -> pd.Series:
    final_regime = []
    current_regime = "Unknown"
    confirm_counter = 0
    decay_counter = 0

    for regime in instant:
        if regime == "Unknown":
            final_regime.append("Unknown")
            current_regime = "Unknown"
            confirm_counter = 0
            decay_counter = 0

            continue

        if regime == current_regime:
            confirm_counter = 0
            decay_counter = 0
            final_regime.append(current_regime)
            continue
        
        #Determine Regime Change 

        candidate = regime
        if current_regime=="Stable" and regime == "Unstable":
            if decay_counter >= decay:
                decay_counter=0
                candidate = "Transitional"
            else:
                decay_counter+=1
        elif (current_regime=="Transitional" and regime == "Stable") or (current_regime=="Unstable" and regime == "Transitional"):
            if confirm_counter >= confirm:
                confirm_counter=0
                candidate = regime
            else:
                confirm_counter+=1
        else:
            confirm_counter=0
            decay_counter=0

        current_regime = candidate
        final_regime.append(current_regime)


    return pd.Series(final_regime, index=instant.index)