import pandas as pd

def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df["Category"] = "Uncategorized"
    return df