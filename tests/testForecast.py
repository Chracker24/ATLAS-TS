# From testEngine for Intelligence Engine output
import pandas as pd
from atlas_ie.src.core.engine import ATLASIntelligenceEngine as ie

df= pd.read_csv("atlas_ie/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
engine_window = 5
engine = ie(window=engine_window, sensitivity="loose", domain="f1")

out = engine.run(df)

# now testing Forecast Engine with the output

from atlas_f.forecast_engine import ATLASForecastEngine as af
engine = af(domain="f1", window = engine_window)
forecast_result = engine.forecast(out, anchor_index = 83)
print(forecast_result)

