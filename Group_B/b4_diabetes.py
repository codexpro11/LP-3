import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(SCRIPT_DIR, "diabetes.csv") if not os.path.exists("diabetes.csv") else "diabetes.csv"

df = pd.read_csv(data_path).drop_duplicates()
features = [
    "Pregnancies", "Glucose", "BloodPressure",
    "SkinThickness", "Insulin", "BMI",
    "DiabetesPedigreeFunction", "Age"
]
required = set(features + ["Outcome"])
if not required.issubset(df.columns):
    raise ValueError(f"Missing: {sorted(required - set(df.columns))}")
df = df.dropna(subset=["Outcome"])
X = df[features].apply(pd.to_numeric, errors="raise").copy()
y = df["Outcome"].astype(int)
if set(y.unique()) != {0, 1}:
    raise ValueError("Outcome must contain both 0 and 1")
zero_missing = [
    "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"
]
X[zero_missing] = X[zero_missing].replace(0, np.nan)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
model = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)
model.fit(X_train, y_train)
pred = model.predict(X_test)
cm = confusion_matrix(y_test, pred, labels=[0, 1])
tn, fp, fn, tp = cm.ravel()
accuracy = accuracy_score(y_test, pred)
print("Confusion matrix:\n", cm)
print("TN, FP, FN, TP:", tn, fp, fn, tp)
print("Accuracy:", accuracy)
print("Error rate:", 1 - accuracy)
print("Precision:", precision_score(y_test, pred, zero_division=0))
print("Recall:", recall_score(y_test, pred, zero_division=0))
print("F1:", f1_score(y_test, pred, zero_division=0))
