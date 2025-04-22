# pdf_to_dataframe.py

import pdfplumber
import pandas as pd
import re

# Match formats like "1 February ... 24.50 39,975.50"
COMPACT_LINE_REGEX = re.compile(
    r"^(?P<date>\d{1,2} [A-Za-z]+)(?:.*?)?(?P<amount>-?[\d,]+\.\d{2})\s+(?P<balance>[\d,]+\.\d{2})$"
)


def extract_text_lines(pdf_path: str) -> list[str]:
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for l in text.splitlines():
                line = l.strip()
                if line:
                    lines.append(line)
    print("[DEBUG] Raw lines extracted from PDF:")
    for l in lines:
        print("  ", l)
    return lines


def parse_fallback_from_compact(lines: list[str]) -> pd.DataFrame:
    records = []
    for i, line in enumerate(lines):
        m = COMPACT_LINE_REGEX.match(line)
        if not m:
            continue
        date = pd.to_datetime(m.group("date") + " 2019", dayfirst=True, errors="coerce")
        if pd.isna(date):
            continue
        amount = float(m.group("amount").replace(",", ""))
        balance = float(m.group("balance").replace(",", ""))
        action = "Credit" if amount >= 0 else "Debit"
        # Combine this and previous line for better description
        description = lines[i - 1] if i > 0 else ""
        records.append({
            "Date": date,
            "Description": description.strip(),
            "Amount": amount,
            "Balance": balance,
            "Action": action
        })
    return pd.DataFrame(records)


def parse_dataframe_from_pdf(pdf_path: str) -> pd.DataFrame:
    lines = extract_text_lines(pdf_path)
    df = parse_fallback_from_compact(lines)
    if not df.empty and 'Date' in df.columns:
        df = df.sort_values('Date').reset_index(drop=True)
    return df


if __name__ == '__main__':
    import sys
    pdf = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/statement_sample1.pdf'
    df = parse_dataframe_from_pdf(pdf)
    print(df)
    df.to_csv('parsed_statement.csv', index=False)
    print(f"[INFO] Parsed {len(df)} rows to parsed_statement.csv")