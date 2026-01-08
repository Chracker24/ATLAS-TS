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

print(ie_output.to_string)
index = int(input("Provide the reference point you would like to backtest : "))
result = f_engine.forecast(ie_output, mode="backtest", anchor_index=index)

print("\n\n"+"-"*60)
print(f"BACKTEST - Reference from lap {index}")
print("-"*60)

print(f"Status - {result["status"]}")
print(f"Forecasting from lap: {result["anchor_index"]}")
print(f"Regime : {result['regime']}")
if 'reasons' in result.keys():
    print(f"Reasons : {result["message"]}")

if result['status'] == "PERMITTED":
    print(f"Horizon : {result.get('horizon',0)}")
    print(f"Forecast Values : {[f"{x:.2f}" for x in result['forecast_values']]}")
    print(f"Actual Values : {[f"{x:.2f}" for x in result["actual_values"]]}")

    if "forecast_error" in result:
        print("Forecast Errors")
        print(f" MAE: {result["forecast_error"]['MAE']:.3f}")
        print(f" RMSE: {result["forecast_error"]["RMSE"]:.3f}")
        print(f" MAPE: {result["forecast_error"]["MAPE"]:.3f}")
