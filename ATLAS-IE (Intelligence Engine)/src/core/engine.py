import pandas as pd

from .validation import find_error_inInput
from .confidence import confidenceScore, forecastingAllowed, confidenceBand

from ..regime.regime_instantaneous import classify_regimes
from ..regime.regime_persistance import regime_persistance

from ..explainability.explainability import reasons, summary


sensitivityBand ={
        "strict" : {
            "alpha" : 0.1,
            "beta" : 1.5,
            "confirm" : 2
        },
        "normal" : {
            "alpha" : 0.2,
            "beta" : 2.0,
            "confirm" : 3
        },
        "loose" : {
            "alpha" : 0.3,
            "beta" : 3.0,
            "confirm" : 4
        }
        
    }
class MTSEngine:
    """
    core Multi Domain Time Series (MTS) Engine
    Stateless, local and Rolling statistics-based
    """
    

    def __init__(self, window : int = 5, sensitivity : str = "normal"):
        self.window = window
        if sensitivity not in sensitivityBand.keys():
            raise ValueError(f"Sensitivty must be one of {list(sensitivityBand.keys())}")
        self.sensitivity = sensitivity
        self.alpha = sensitivityBand[sensitivity]["alpha"]
        self.beta = sensitivityBand[sensitivity]["beta"]
        self.confirm = sensitivityBand[sensitivity]["confirm"]


    def run(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Analyses Time series Dataframe
        returns a new Dataframe with rolling statistics added
        """

        #Validating input
        find_error_inInput(df, self.window)

        #Copying the Dataframe 
        result = df.copy()

        #identifying the signal column
        signal_col = result.select_dtypes(include="number").columns[0]

        #Rolling Mean
        result["Rolling mean"] = result[signal_col].rolling(window = self.window, min_periods=self.window).mean()

        #Rolling Variance
        result["Rolling Variance"] = result[signal_col].rolling(window = self.window, min_periods=self.window).var()

        result["Regime_Raw"] = classify_regimes(result["Rolling Variance"], self.window, alpha = self.alpha, beta = self.beta)
        result["Regime_Final"] = regime_persistance(result["Regime_Raw"], confirm=self.confirm)

        result["Confidence"] = confidenceScore(result["Regime_Final"])

        result["Forecasting_Allowed"] = forecastingAllowed(
        result["Confidence"],
        threshold=0.7,
        window=5
        )
        result["Confidence_Band"] = confidenceBand(result["Confidence"])
        # Engine Reasons, Summary and Data Quality checks to be added
        result["Reasons"] = reasons(result["Regime_Final"])
        result["Summary"] = result["Reasons"].apply(summary)
        return result
    
    def results_schema(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Provides a proper schema for domain agnostic results
        """

        result = df.copy()
        signal_col = result.select_dtypes(include="number").columns[0]
        result = result[[signal_col, "Confidence_Band","Reasons","Summary"]].rename(columns={signal_col: f"Signal ({signal_col})", "Confidence_Band" : "FORECASTING_STATE", "Reasons": "Forecasting Reasons"})
        return result