import pandas as pd
from atlas_ie.core.engine import ATLASIntelligenceEngine as IE
from atlas_f.forecast_engine import ATLASForecastEngine as F

#Loading Data
df = pd.read_csv("01_Data_Handling/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
domain = "f1"
#Create and Run Intelligence Engine
ie_engine = IE(domain=domain)
ie_output = ie_engine.run(df)

#Create Forecast Engine
f_engine = F(domain=domain)

"""
Backtest FORECASTING

looks at the given reference and makes the predictions
"""

