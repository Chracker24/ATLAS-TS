import pandas as pd
from src.Formula1.engine import MTSEngine

df_raw = pd.read_csv("01_Data/Canonical/lewisHamilton_AbuDhabi_2021.csv")
engine = MTSEngine(window=5)
# Explicitly select the signal (example: LapTime)
df = df_raw[["LapTime"]]

out = engine.run(df)
print(out.to_string())