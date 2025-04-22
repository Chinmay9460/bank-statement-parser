
import camelot
import pandas as pd
import os

def parse_pdfs(input_dir: str) -> pd.DataFrame:
    all_rows = []

    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(input_dir, fname)
        print(f"[INFO] Parsing PDF: {path}")
        tables = camelot.read_pdf(path, pages="all", flavor="stream")

        for i, table in enumerate(tables):
            df = table.df
            print(f"  [DEBUG] Table {i} extracted with {len(df)} rows")
            all_rows.append(df)

    if not all_rows:
        print("[WARN] No tables found in PDFs.")
        return pd.DataFrame()

    combined = pd.concat(all_rows, ignore_index = True)
    return combined