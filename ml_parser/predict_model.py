
# predict_model.py

import pandas as pd
import joblib

# Load model
model = joblib.load("./model.pkl")
print("[INFO] Model loaded.")

# Load raw PDF lines from a CSV
unlabeled = pd.read_csv("./data/unlabeled_lines.csv")
X_new = unlabeled["line"]

# Predict labels (valid/irrelevant)
predictions = model.predict(X_new)

# Attach predictions to DataFrame
unlabeled["prediction"] = predictions
print("\n[INFO] Predictions:\n")
print(unlabeled)

# Save result
unlabeled.to_csv("./data/predicted_lines.csv", index=False)
print("\n[INFO] Saved predictions to ml_parser/data/predicted_lines.csv")