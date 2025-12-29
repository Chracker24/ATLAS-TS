import pandas as pd

Reasons={
    "VA_SP" : "Variance Instability",
    "NO_HIS" : "Insufficient History for analysis",
    "UNST" : "Unstable Regime detected",
    "TR_PRO" : "Transitional period, awaiting stabilization",
    "REC" : "RECOVERED",
    "TR_PH" : "Transitional Phase",
    "STBL" : "Stable Phase"
}



def reasons(
        df:pd.Series)->list[list[str]]:
    """
    To look over the whole Dataframe and return a Dataframe containing feedback on Reasons explaining confidence band
    """

    
    reasons=[]
    for i in range (len(df)):
        reasonsPerRow = []
        if df.iloc[i]=="Unknown":
            reasonsPerRow.append("NO_HIS")
        elif df.iloc[i]=="Unstable":
            reasonsPerRow.append("UNST")
        elif df.iloc[i]=="Stable":
            reasonsPerRow.append("STBL")
        elif df.iloc[i]=="Transitional":
            reasonsPerRow.append("TR_PH")
        if i > 0:
            prev = df.iloc[i-1]
            curr = df.iloc[i]
            if prev == "Unstable" and curr == "Transitional":
                reasonsPerRow.append("TR_PRO")
            elif prev == "Transitional" and curr ==  "Stable":
                reasonsPerRow.append("REC")
            elif prev == "Stable" and curr == "Unstable":
                reasonsPerRow.append("VA_SP")
        reasons.append(reasonsPerRow)

    return reasons


def summary(reason_codes: list[str]) -> str:
    messages = [Reasons[c] for c in reason_codes]
    return "; ".join(messages)

        