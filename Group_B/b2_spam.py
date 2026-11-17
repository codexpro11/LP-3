import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report
)

df = pd.read_csv("emails.csv").drop_duplicates()
df.columns = df.columns.str.strip()
if "Prediction" not in df:
    raise ValueError("Expected target column Prediction")
df = df.dropna(subset=["Prediction"])
y = pd.to_numeric(df["Prediction"], errors="raise").astype(int)
if set(y.unique()) != {0, 1}:
    raise ValueError("Expected both labels 0 and 1")
X = df.drop(columns=["Prediction", "Email No."], errors="ignore")
X = X.apply(pd.to_numeric, errors="raise")
# Remove duplicate feature vectors with identical labels.
combined = X.copy()
combined["_target_"] = y
keep = ~combined.duplicated()
X, y = X.loc[keep], y.loc[keep]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "SVM": SVC(kernel="linear", C=1.0)
}
for name, classifier in models.items():
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(), classifier
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print("\n", name)
    print("Accuracy:", accuracy_score(y_test, pred))
    print("Confusion matrix:\n",
          confusion_matrix(y_test, pred, labels=[0, 1]))
    print(classification_report(
        y_test, pred, labels=[0, 1],
        target_names=["Not spam", "Spam"], zero_division=0
    ))
