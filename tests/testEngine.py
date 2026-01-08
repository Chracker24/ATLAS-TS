import pandas as pd
from atlas_ie.core.engine import ATLASIntelligenceEngine as ie
from atlas_ie.core.index import indexing

df = pd.read_csv("01_Data_Handling/Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
engine = ie(window=5, sensitivity="loose", domain="f1")
# Explicitly select the signal (example: LapTime)
out = engine.run(df)
print(out.to_string())
