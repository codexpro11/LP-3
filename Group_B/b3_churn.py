import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_auc_score
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(SCRIPT_DIR, "Churn_Modelling.csv") if not os.path.exists("Churn_Modelling.csv") else "Churn_Modelling.csv"

df = pd.read_csv(data_path).drop_duplicates()
required = {
    "Exited", "CreditScore", "Geography", "Gender", "Age",
    "Tenure", "Balance", "NumOfProducts", "HasCrCard",
    "IsActiveMember", "EstimatedSalary"
}
if not required.issubset(df.columns):
    raise ValueError(f"Missing: {sorted(required - set(df.columns))}")
df = df.dropna(subset=["Exited"])
X = df.drop(
    columns=["Exited", "RowNumber", "CustomerId", "Surname"],
    errors="ignore"
)
y = df["Exited"].astype(int)
if set(y.unique()) != {0, 1}:
    raise ValueError("Exited must contain both 0 and 1")
categorical = ["Geography", "Gender"]
numeric = [c for c in X.columns if c not in categorical]
X[numeric] = X[numeric].apply(pd.to_numeric, errors="raise")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
prep = ColumnTransformer([
    ("num", make_pipeline(
        SimpleImputer(strategy="median"), StandardScaler()
    ), numeric),
    ("cat", make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    ), categorical)
])
model = Pipeline([
    ("prep", prep),
    ("nn", MLPClassifier(
        hidden_layer_sizes=(16,), activation="relu",
        solver="adam", max_iter=600, random_state=42
    ))
])
# First candidate is the baseline; others test improvements.
# All transformations are refitted inside each CV training fold.
grid = [
    {"nn__hidden_layer_sizes": [(16,)], "nn__alpha": [0.0001]},
    {"nn__hidden_layer_sizes": [(32, 16)],
     "nn__alpha": [0.001, 0.01]}
]
search = GridSearchCV(
    model, grid, scoring="roc_auc", cv=3, n_jobs=1,
    refit=True
)
search.fit(X_train, y_train)
for params, score in zip(
    search.cv_results_["params"],
    search.cv_results_["mean_test_score"]
):
    print("CV ROC-AUC:", round(score, 4), params)
print("Selected configuration:", search.best_params_)
best = search.best_estimator_
pred = best.predict(X_test)
prob = best.predict_proba(X_test)[:, 1]
print("Test accuracy:", accuracy_score(y_test, pred))
print("Test ROC-AUC:", roc_auc_score(y_test, prob))
print("Confusion matrix:\n",
      confusion_matrix(y_test, pred, labels=[0, 1]))
print(classification_report(y_test, pred, zero_division=0))
print("Iterations:", best.named_steps["nn"].n_iter_)
