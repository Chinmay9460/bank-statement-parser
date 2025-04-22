# run.py

import argparse
import os
import glob
import pandas as pd
from utils.normalize import normalize_transactions
from utils.cache import is_new_data
from classifier.categorize import categorize_transactions
from reporter.report_generation import generate_report
from utils.notification import send_alerts
from pdf_to_dataframe import parse_dataframe_from_pdf
from utils.chart import generate_balance_chart


def main():
    parser = argparse.ArgumentParser(description="Bank Statement Parser")
    parser.add_argument("--source", choices=["pdf", "csv"], default="pdf", help="Source file type")
    parser.add_argument("--input_dir", type=str, default="data/raw", help="Input directory or PDF file")
    parser.add_argument("--output_dir", type=str, default="data/output", help="Output directory for reports")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.source == "pdf":
        # Determine PDF files to process
        if os.path.isdir(args.input_dir):
            pdf_files = glob.glob(os.path.join(args.input_dir, "*.pdf"))
            if not pdf_files:
                print(f"[WARN] No PDF files found in directory: {args.input_dir}")
                return
        elif os.path.isfile(args.input_dir) and args.input_dir.lower().endswith(".pdf"):
            pdf_files = [args.input_dir]
        else:
            print(f"[ERROR] Input path is not a PDF or directory: {args.input_dir}")
            return

        # Parse each PDF and merge
        df_list = []
        for pdf_file in pdf_files:
            print(f"[INFO] Parsing PDF: {pdf_file}")
            df_pdf = parse_dataframe_from_pdf(pdf_file)
            if df_pdf is not None and not df_pdf.empty:
                df_list.append(df_pdf)

        if not df_list:
            print("[WARN] No data extracted from any PDF. Exiting.")
            return
        df = pd.concat(df_list, ignore_index=True)
    else:
        print("[ERROR] CSV parsing not implemented yet.")
        return

    if df.empty:
        print("[WARN] No data extracted. Exiting.")
        return

    # Normalize and categorize if needed
    try:
        df = normalize_transactions(df)
    except Exception:
        pass
    try:
        df = categorize_transactions(df)
    except Exception:
        pass

    # Cache check
    if not is_new_data(df):
        print("[INFO] No new data. Exiting.")
        return

    # Generate report and alerts
    print("[INFO] Generating report...")
    chart_path = generate_balance_chart(df, args.output_dir)
    report_path = generate_report(df, chart_path, args.output_dir)
    send_alerts(df)

    print(f"[✅] Report saved at: {report_path}")


if __name__ == "__main__":
    main()