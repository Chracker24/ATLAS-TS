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
LIVE FORECASTING

looks at the last instance and forecasts possiblities for the future instances
"""

result = f_engine.forecast(ie_output,mode="live")

print("-" * 60)
print(" LIVE TESTING ")
print("-" * 60)

print(f" Status : {result['status']}")
print(f" Index : {result['anchor_index']}")
print(f" Regime : {result['regime']}")
print(f" Confidence : {result['confidence']:.1f}")
print(f" Horizon : {result.get('horizon',0)}")

if result['status'] == "PERMITTED":
    print(f"\nModel {result['model']}")
    print(f"Parameters : Alpha = {result["parameters"]["alpha"]:.2f}, Beta = {result["parameters"].get("beta","N/A")}")
    print(f"\n\nForecast : {[f'{x:.2f}' for x in result['forecast_values']]}")
    print(f"90% Bounds: {[f'{x:.2f}' for x in result['lower_bounds']]} to {[f'{x:.2f}' for x in result['upper_bounds']]}")
    print(f"\n\n Why this Horizon? : {result['why_this_horizon']}")
    print(f"Why use this model? : {result['why_this_model']}")
    print(f"Forecast Quality : {result["forecast_quality"]}")
else:
    print(f"\nReasons : {result["message"]}")

'''

response = {
            "status" : "PERMITTED",
            "mode" : mode, 
            "anchor_index" : anchor_index,
            "regime" : regime,
            "confidence" : float(confidence),
            "domain" : self.domain,

            "horizon" : horizon,
            "forecast_values" : [float(f) for f in result['forecast']],
            "lower_bounds" : [float(l) for l in lower_bounds],
            "upper_bounds" : [float(u) for u in upper_bounds],

            "model": model_used,
            "parameters" : {
                "alpha" : alpha,
                "beta" : beta if 'trend' in result else None
            },
            'level' : float(result['level']),
            'trend' : float(result.get('trend', 0.0)),

            "why_this_horizon" : explain_horizon(regime, self.domain),
            "why_this_model"  : _explain_model_choice(regime),
            "forecast_quality" : _assess_quality(result['residuals'], confidence)
        }
'''