import pandas as pd
from atlas_ie.src.core.engine import ATLASIntelligenceEngine

df_raw = pd.read_csv("atlas_ie/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
engine = ATLASIntelligenceEngine(window=5, sensitivity="loose", domain="f1")
# Explicitly select the signal (example: LapTime)
df = df_raw[["LapTime"]]

out = engine.run(df)
result = engine.results_schema(out)
print(result.to_string())
