from flask import Flask, render_template, send_from_directory
import os

# Tell Flask where to find templates and static files
app = Flask(__name__, template_folder='templates', static_folder='data/output')

# List all HTML reports in data/output
def list_reports():
    files = os.listdir('data/output')
    return sorted([f for f in files if f.startswith('report_') and f.endswith('.html')])

# List all chart images in data/output
def list_charts():
    files = os.listdir('data/output')
    return sorted([f for f in files if f.startswith('balance_trend_') and f.endswith('.png')])

@app.route('/')
def dashboard():
    reports = list_reports()
    charts = list_charts()
    return render_template('dashboard.html', reports=reports, charts=charts)

# Serve report HTML and chart PNG under /outputs/<filename>
@app.route('/outputs/<path:filename>')
def output_file(filename):
    return send_from_directory('data/output', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)