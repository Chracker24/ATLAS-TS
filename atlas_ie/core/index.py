import pandas as pd

def indexing(df : pd.DataFrame) -> tuple[pd.DataFrame,bool]:
    if df.empty:
        raise ValueError("DataFrame is Empty")
    else:
        signal_col = df.select_dtypes(include="number").columns[0]
        cols = df.columns.tolist()
        for i in cols:
            print(i)
        ind = input("\nIs there a column that you would like to be a reference out of the following? (Y/N) :")
        if ind in ["Y", "Yes", "yes","y"]:
            c = input("Enter the name of the column")
            c = c.strip()
            if c not in cols:
                raise ValueError("The Column does not exist in the Dataframe")
            else:
                df[c] = df[c].astype(str)
                return (df[[signal_col,c]],True)
        else:
            print("Okay!")
            return (df[[signal_col]],False)