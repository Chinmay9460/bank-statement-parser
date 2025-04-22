def send_alerts(df):
    # Example: warn if any negative balance
    if (df["Balance"] < 0).any():
        print("[ALERT] Negative balance detected!")
    else:
        print("[INFO] All balances non-negative.")