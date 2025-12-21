import pandas as pd
from .validation import find_error_inInput
from .regime_instantaneous import classify_regimes
from .regime_persistance import regime_persistance

class MTSEngine:
    """
    core Multi Domain Time Series (MTS) Engine
    Stateless, local and Rolling statistics-based
    """

    def __init__(self, window : int = 5):
        self.window = window

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

        result["Regime_Raw"] = classify_regimes(result["Rolling Variance"], self.window)
        result["Regime_Final"] = regime_persistance(result["Regime_Raw"], confirm=2)
        return result