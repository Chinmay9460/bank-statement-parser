import matplotlib.pyplot as plt
import os

def generate_balance_chart(df, out_dir):
    dates = df["Date"]
    balances = df["Balance"]
    plt.figure()
    plt.plot(dates, balances)
    plt.title("Balance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.tight_layout()
    chart_path = os.path.join(out_dir, "balance_trend.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path