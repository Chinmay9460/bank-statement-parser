
#Train model.py

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

#Load dataset
labeled = pd.read_csv("./data/labeled_lines.csv")

#Extract features and labels
X = labeled['line']
y = labeled['label']

#Train/test split
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=1000, random_state=42))
])

#Train model
pipeline.fit(X_train, Y_train)

#Evaluate model
y_pred = pipeline.predict(X_test)
print("\n Classification Report: \n")
print(classification_report(Y_test, y_pred))

#Save Model
joblib.dump(pipeline, './model.pkl')
print("\n[INFO] Model saved to ml_parser/model.pkl")