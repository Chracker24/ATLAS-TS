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
Scenario FORECASTING

Gives predictions based on the Scenario that you imagine
"""

print(ie_output.to_string)
index = int(input("Provide Reference for doing Scenario : "))
ie_output = ie_output[:index+1].copy()
scenario = input("Provide the Scenario that you want to add (Stable, Transitional, Unstable) : ")
assert scenario in ["Stable","Transitional","Unstable"], "Please Enter a valid Scenario"
result = f_engine.forecast(ie_output, mode="scenario", scenario_regime=scenario)

print("\n\n" + "-" * 60)
print(f"SCENARIO (What if lap {index} was {scenario}")
print("-" * 60)

print(f"Status : {result["status"]}")
print(f"Overriden Regime : {result['regime']}")

if result['status'] == "BLOCKED":
    print(f"Reasons : {result['message']}")
else:
    print(f"Forecast: {[f'{x:.2f}' for x in result['forecast_values']]}")


print("\n\n"+"-"*60)
print("")