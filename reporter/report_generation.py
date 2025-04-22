import os
from datetime import datetime
import pandas as pd

def generate_report(df: pd.DataFrame, chart_path: str, out_dir: str) -> str:
    """Produce a simple HTML report with embedded chart."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_fn = f"statement_{ts}.csv"
    html_fn = f"report_{ts}.html"
    df.to_csv(os.path.join(out_dir, csv_fn), index=False)

    html = f"""
    <!DOCTYPE html><html><body>
      <h1>Statement Report</h1>
      <img src="{os.path.basename(chart_path)}" style="max-width:600px;"/><br/>
      {df.to_html(index=False)}
    </body></html>
    """
    with open(os.path.join(out_dir, html_fn), "w") as f:
        f.write(html)
    return os.path.join(out_dir, html_fn)