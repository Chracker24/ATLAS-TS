import pandas as pd
import numpy as np

class validate_timeseries_input(Exception):
    "TO PASS FOUND EXCEPTIONS"
    pass

def find_error_inInput(df : pd.DataFrame, window: int ) -> None:
    """
    Rules for Finding Error

    df -> should be a Pandas Dataframe
    df -> should NOT be empty
    df -> should only have one numerical column
    df -> must not entirely be NANs
    df -> should be having length >= window
    """

    #Checking the Type
    if not isinstance(df, pd.DataFrame):
        raise validate_timeseries_input("Input must be a Pandas Dataframe")

    if df.empty:
        raise validate_timeseries_input("Dataframe is Empty")

    numerical_cols = df.select_dtypes(include=[np.number]).columns

    if len(numerical_cols)==0:
        raise validate_timeseries_input("No Numerical Column present in the Dataframe")

    if len(numerical_cols) > 1:
        raise validate_timeseries_input(
            "Multiple numerical columns found"
            "Only one numerical time series column needed")
    
    signal = df[numerical_cols[0]]

    if signal.isna().all():
        raise validate_timeseries_input("The Time Series data only has NAN values")
    
    if len(df) < window:
        raise validate_timeseries_input(
            "Input Data has data lesser than given window"
            f"Data should have data above window size : {window}, length of DataFrame : {len(df)}"
        )