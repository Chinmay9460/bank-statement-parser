
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ─── Step 1: Prepare sample data ─────────────────────────────────────────────
data = [
    ["Txn Date", "Value Date", "Description", "Debit", "Credit", "Balance"],
    ["01/03/2024", "01/03/2024", "ATM Withdrawal", "1000.00", "", "49000.00"],
    ["02/03/2024", "02/03/2024", "Salary from ABC Pvt Ltd", "", "50000.00", "99000.00"],
    ["04/03/2024", "04/03/2024", "Amazon India Payment", "1500.00", "", "97500.00"],
    ["06/03/2024", "06/03/2024", "UPI Transfer - rent March", "8000.00", "", "89500.00"],
    ["09/03/2024", "09/03/2024", "NEFT: Gpay Cashback", "", "100.00", "89600.00"],
    ["10/03/2024", "10/03/2024", "Interest Credit", "", "150.50", "89750.50"]
]

# ─── Step 2: Plot Balance Chart ──────────────────────────────────────────────
# Extract dates and balances
dates = [row[0] for row in data[1:]]
balances = [float(row[5]) for row in data[1:]]

plt.figure()
plt.plot(dates, balances)            # default styling
plt.title("Account Balance Over Time")
plt.xlabel("Date")
plt.ylabel("Balance (₹)")
plt.grid(True)
chart_path = "data/raw/balance_chart.png"
os.makedirs(os.path.dirname(chart_path), exist_ok=True)
plt.tight_layout()
plt.savefig(chart_path)
plt.close()

# ─── Step 3: Generate Two‑Page PDF ────────────────────────────────────────────
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Bank of Python Ltd. - Statement", 0, 1, "C")
        self.ln(2)

    def add_table(self, table_data):
        self.set_font("Courier", size=9)
        col_widths = [25, 25, 70, 25, 25, 30]
        for row in table_data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 8, cell, 1)
            self.ln()

# build PDF
pdf = PDF()
pdf.add_page()

# Page 1: the transactions table
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "Account Statement: 01/03/2024 - 10/03/2024", 0, 1)
pdf.ln(4)
pdf.add_table(data)

# Page 2: the balance chart
pdf.add_page()
pdf.cell(0, 10, "Balance Trend", 0, 1, "L")
pdf.image(chart_path, x=15, y=25, w=180)  # adjust positioning/size as needed

# save
output_pdf = "data/raw/statement_full.pdf"
pdf.output(output_pdf)
print(f"✅ Sample PDF with chart saved to {output_pdf}")