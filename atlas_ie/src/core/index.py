import pandas as pd

def indexing(df : pd.DataFrame) -> tuple:
    cols = df.columns.tolist()
    for i in cols:
        print(i)
    ind = input("\nIs there a column that you would like to be a reference out of the following? (Y/N) :")
    if ind in ["Y", "Yes", "yes","y"]:
        c = input("Enter the name of the column")
        if c not in cols:
            raise ValueError("The Column does not exist in the Dataframe")
        else:
            df[c] = df[c].astype(str)
            return (df,True)
    else:
        print("Okay!")
        return (df,False)