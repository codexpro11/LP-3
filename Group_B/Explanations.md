# LP III - Group B
## Machine Learning
SPPU | Fourth Year Computer Engineering | 2019 Course | 410246

All five assignments from the supplied LP III.pdf. Each program is independent and uses Python. Copy its complete code block into the named .py file. Download the specified CSV into the same folder; datasets are not bundled. Column checks make mismatched downloads fail clearly.

## Setup and evaluation rules
Create an environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install numpy pandas matplotlib scikit-learn
```
On Windows, activate with `.venv\Scripts\activate`. Run with `python3 b1_uber.py`, changing the filename for each assignment. The code uses the modern OneHotEncoder sparse_output parameter (scikit-learn 1.2 or later). Plots appear in windows and are also saved as PNG files.

**Important:** The real CSVs have not been run here. Accuracy, R2, RMSE and cluster count must come from your run, not copied example numbers. Random state 42 makes splits and supported algorithms reproducible within the same software/data setup.

Split before fitting imputers, scalers or encoders. A pipeline learns preprocessing only from training data. Keep the test set for final reporting; choose hyperparameters using validation or cross-validation on the training set.

## B1. Uber fare prediction
**Aim:** Predict fare_amount from pickup/drop-off location and ride context. Compare linear regression and random forest regression.

**Dataset:** https://www.kaggle.com/datasets/yasserh/uber-fares-dataset
Download the CSV and save it as uber.csv.

**Required fields:** fare_amount, pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count.

**Approach:** Remove duplicate records and physically invalid records, calculate straight-line trip distance with the Haversine formula, derive time features, inspect training-set outliers with IQR and examine numeric correlations. The IQR flag is diagnostic: plausible long/expensive trips are retained rather than removing every flagged observation. Both models use the same held-out rows.

### Code - b1_uber.py
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("uber.csv").drop_duplicates()
required = [
    "fare_amount", "pickup_datetime", "pickup_longitude",
    "pickup_latitude", "dropoff_longitude",
    "dropoff_latitude", "passenger_count"
]
missing = set(required) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

numeric = [c for c in required if c != "pickup_datetime"]
df[numeric] = df[numeric].apply(pd.to_numeric, errors="coerce")
df["pickup_datetime"] = pd.to_datetime(
    df["pickup_datetime"], errors="coerce", utc=True
)
before = len(df)
df = df.dropna(subset=required).copy()
valid = (
    (df["fare_amount"] > 0)
    & df["passenger_count"].between(1, 6)
    & (df["passenger_count"] % 1 == 0)
    & df["pickup_latitude"].between(-90, 90)
    & df["dropoff_latitude"].between(-90, 90)
    & df["pickup_longitude"].between(-180, 180)
    & df["dropoff_longitude"].between(-180, 180)
)
df = df.loc[valid].copy()

lat1 = np.radians(df["pickup_latitude"])
lat2 = np.radians(df["dropoff_latitude"])
dlat = lat2 - lat1
dlon = np.radians(
    df["dropoff_longitude"] - df["pickup_longitude"]
)
a = (np.sin(dlat / 2) ** 2
     + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2)
df["distance_km"] = 6371.0 * 2 * np.arcsin(
    np.sqrt(np.clip(a, 0, 1))
)
# This lab assumes local NYC trips and at most six passengers.
# These are explicit domain filters, not learned IQR thresholds.
df = df[df["distance_km"].between(0.05, 100)].copy()
print("Rows excluded by missing/domain checks:", before - len(df))
dt = df["pickup_datetime"].dt
df["hour"] = dt.hour
df["weekday"] = dt.dayofweek
df["month"] = dt.month
df["year"] = dt.year

features = [
    "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude",
    "passenger_count", "distance_km",
    "hour", "weekday", "month", "year"
]
X = df[features]
y = df["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
train = X_train.copy()
train["fare_amount"] = y_train
for column in ["fare_amount", "distance_km"]:
    q1, q3 = train[column].quantile([0.25, 0.75])
    iqr = q3 - q1
    flags = (
        (train[column] < q1 - 1.5 * iqr)
        | (train[column] > q3 + 1.5 * iqr)
    )
    print(column, "training IQR outliers:", int(flags.sum()))

corr = train.corr(numeric_only=True)
print("Training correlations with fare:")
print(corr["fare_amount"].sort_values(ascending=False))
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr)), corr.columns, rotation=90)
ax.set_yticks(range(len(corr)), corr.columns)
fig.colorbar(im, ax=ax)
fig.tight_layout()
fig.savefig("uber_correlation.png", dpi=160)
plt.show()

models = {
    "Linear regression": make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(), LinearRegression()
    ),
    "Random forest": make_pipeline(
        SimpleImputer(strategy="median"),
        RandomForestRegressor(
            n_estimators=150, min_samples_leaf=2,
            random_state=42, n_jobs=-1
        )
    )
}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(name, "R2 =", round(r2_score(y_test, pred), 4),
          "RMSE =", round(rmse, 4))
```

**Explain the code:** Haversine converts latitude/longitude into an approximate direct distance in kilometres; it is not actual road distance. Datetime features capture time-related fare differences. Linear regression learns an additive linear relationship. Random forest averages decision trees and can model nonlinear relationships. Scaling is useful for the linear baseline; trees do not require it.

**Interpretation:** Lower RMSE means smaller typical prediction error in fare units; R2 = 1 is perfect, 0 matches predicting the test mean, and negative values are possible. Do not assume random forest wins until comparing actual results.

**Limitations:** The 0.05-100 km and passenger filters define the population being evaluated and can exclude legitimate unusual rides. UTC hour is used, not converted NYC local hour. Correlation does not imply causation. Historical fare data does not establish current Uber pricing; a random split assesses interpolation, while a chronological split is better for future forecasting.

**Tell the examiner:** "I clean invalid trips, create a distance feature, inspect outliers and correlations on the training set, then compare a linear baseline with a nonlinear random forest on identical test data."

## B2. Email spam classification using KNN and SVM
**Aim:** Classify email as 0 = not spam or 1 = spam and compare both classifiers.

**Dataset:** https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv
Save emails.csv. This dataset contains numeric word-count features, an Email No. identifier, and Prediction labels. It is not a CSV containing raw message text.

**Approach:** Remove the identifier, split with stratification to preserve class proportions, impute missing values, scale features and compare classification metrics.

### Code - b2_spam.py
```python
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
```

**Explanation:** KNN assigns the majority class among the five nearest training points. Scaling prevents frequent/high-range words from dominating distances. Linear SVM finds a separating hyperplane with a large margin; C controls the trade-off between margin size and classification penalties.

**Performance analysis:** Compare spam precision, recall and F1, as well as accuracy. High precision reduces legitimate mail wrongly marked spam; high recall catches more spam. KNN stores the training set and can predict slowly in thousands of dimensions. SVM may fit high-dimensional word features better, but your measured results decide.

**Confusion matrix layout:** Rows are true labels and columns predicted labels: [[TN, FP], [FN, TP]]. Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 is their harmonic mean. zero_division=0 handles undefined metric ratios.

**Tell the examiner:** "The emails are already represented by word counts. I remove the email identifier, normalize features without using the test data, train KNN and SVM, and compare their spam-detection errors."

**Viva:** Does KNN train weights? No, it mainly stores examples. Can this program classify a pasted new email? Only after converting that email into the exact same word-feature vocabulary and order.

## B3. Bank customer churn with a neural network
**Aim:** Predict Exited from bank customer characteristics, using a neural-network classifier and a training-only improvement search.

**Dataset:** https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling
Save Churn_Modelling.csv. Required target: Exited. Geography and Gender are categorical. RowNumber, CustomerId and Surname are excluded identifiers.

**Scope:** The syllabus describes leaving within six months; the supplied Exited label is used as given. Without documented timing, this is churn-label prediction, not proof of a calibrated six-month forecast.

### Code - b3_churn.py
```python
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

df = pd.read_csv("Churn_Modelling.csv").drop_duplicates()
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
```

**Explanation:** StandardScaler learns numeric means and standard deviations from training data. One-hot encoding creates indicator columns, avoiding a false ordering of countries or genders. MLPClassifier is a fully connected feed-forward neural network trained by backpropagation. ReLU transforms hidden-layer activations; Adam adjusts weights. Binary output probabilities estimate the positive-class likelihood.

**Implemented improvement:** Cross-validation compares a 16-neuron baseline with a two-hidden-layer network, testing stronger L2 regularization via alpha. This is an attempted improvement, not a promised score increase. ROC-AUC selects the configuration on training folds; only the selected model is evaluated on the held-out test set.

**Practical notes:** Training may take a few minutes. A ConvergenceWarning means the optimiser hit its iteration limit; inspect the loss and increase max_iter or tune settings using training data. A majority-class classifier can have misleadingly high accuracy, so also inspect churn recall and ROC-AUC. Threshold tuning must use validation data, not test labels.

**Tell the examiner:** "I remove identifiers, scale numeric features, encode categories and train a multilayer perceptron. I compare architecture and regularization choices with cross-validation, then evaluate the chosen network on unseen customers."

**Viva:** What is an epoch? One pass through the training examples. What is overfitting? Learning training-specific patterns that do not generalize. What does alpha do? It controls L2 regularization of weights.

## B4. Diabetes prediction using KNN
**Aim:** Compute confusion matrix, accuracy, error rate, precision and recall.

**Dataset:** https://www.kaggle.com/datasets/abdallamahgoub/diabetes
Save diabetes.csv. Expected target: Outcome. This solution assumes the common Pima diabetes schema; if the download differs, the explicit check will identify missing columns.

**Preprocessing:** Zero is an invalid/missing measurement for glucose, blood pressure, skin thickness, insulin and BMI in this lab's preprocessing convention. Zero pregnancies is valid and is retained. Impute using training medians.

### Code - b4_diabetes.py
```python
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

df = pd.read_csv("diabetes.csv").drop_duplicates()
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
```

**Metric meaning:** Accuracy = (TP+TN)/all; error = (FP+FN)/all = 1-accuracy; precision = TP/(TP+FP); recall = TP/(TP+FN). A false negative is a positive case classified as negative.

**Explanation:** KNN compares the standardized feature vectors and votes among five neighbors. Small k may be sensitive to noise; larger k smooths the decision boundary and may underfit. Use training-only cross-validation to choose k rather than repeatedly checking the test set.

**Tell the examiner:** "I handle missing measurements, scale every feature so distances are comparable, classify by the nearest neighbors and derive the requested metrics from the confusion matrix."

**Scope:** This is a dataset classification exercise, not a medical diagnostic tool.

## B5. Sales clustering and elbow method
**Aim:** Apply K-means to sales_data_sample.csv and choose the cluster count using an elbow plot.

**Dataset:** https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
Save sales_data_sample.csv. Common exports use latin-1 encoding.

**Unit of analysis:** One row represents a sales order line, not a customer. Features are QUANTITYORDERED, PRICEEACH and SALES. If the aim is customer segmentation instead, first aggregate by CUSTOMERNAME; this program intentionally clusters order lines.

### Code - b5_sales_clustering.py
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv(
    "sales_data_sample.csv", encoding="latin-1"
).drop_duplicates()
features = ["QUANTITYORDERED", "PRICEEACH", "SALES"]
if not set(features).issubset(df.columns):
    raise ValueError("Missing required sales columns")
X = df[features].apply(pd.to_numeric, errors="coerce")
keep = X.notna().any(axis=1)
df, X = df.loc[keep].copy(), X.loc[keep]
if len(X) < 3 or X.isna().all().any():
    raise ValueError("Need at least 3 rows and observed feature values")
imputed = SimpleImputer(strategy="median").fit_transform(X)
scaled = StandardScaler().fit_transform(imputed)
unique_count = len(np.unique(scaled, axis=0))
max_k = min(10, len(scaled) - 1, unique_count)
if max_k < 2:
    raise ValueError("Not enough distinct rows for clustering")
ks = list(range(1, max_k + 1))
inertias = []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(scaled)
    inertias.append(km.inertia_)

plt.plot(ks, inertias, "o-")
plt.xlabel("Number of clusters k")
plt.ylabel("Within-cluster sum of squares")
plt.title("Elbow method - sales order lines")
plt.xticks(ks)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("sales_elbow.png", dpi=160)
plt.show()
print("k and inertia:", list(zip(ks, inertias)))
k = int(input(f"Choose elbow k from 2 to {max_k}: "))
if not 2 <= k <= max_k:
    raise ValueError("k outside allowed range")

model = KMeans(n_clusters=k, n_init=10, random_state=42)
labels = model.fit_predict(scaled)
df["Cluster"] = labels
print("Cluster sizes:\n", df["Cluster"].value_counts().sort_index())
numeric_result = X.copy()
numeric_result["Cluster"] = labels
print("Mean observed values in original units:")
print(numeric_result.groupby("Cluster")[features].mean())
if 1 < len(set(labels)) < len(labels):
    print("Silhouette:", silhouette_score(scaled, labels))
df.to_csv("sales_clustered.csv", index=False)

plt.scatter(
    imputed[:, 0], imputed[:, 2], c=labels,
    cmap="tab10", s=18, alpha=0.7
)
plt.xlabel("Quantity ordered")
plt.ylabel("Sales")
plt.title("Order-line clusters: two-feature view")
plt.tight_layout()
plt.savefig("sales_clusters.png", dpi=160)
plt.show()
```

**Explanation:** K-means repeatedly assigns points to the nearest centroid and updates centroids to cluster means. Standardization prevents SALES from overwhelming the other features because of its larger numeric scale. n_init=10 tries several centroid initializations.

**Choosing k:** Find where the inertia curve changes from steep to relatively flat, close the plot and enter that k. For example, choose 3 only if your actual plot supports an elbow around 3. There may be no clear elbow; report ambiguity instead of inventing a result. Silhouette provides complementary evidence, not ground-truth accuracy.

**Interpretation:** Describe clusters using printed sizes and original-unit means, such as larger-value versus smaller-value order lines. Labels 0, 1, 2 are arbitrary identifiers, not ranks. SALES and quantity/price are related, which can influence the groups; document this feature choice. Scaling does not remove outliers, and unusual bulk purchases can move centroids.

**Complexity:** Approximately O(n × k × d × iterations) for one initialization. Ten starts multiply the work. Silhouette evaluation can be expensive for very large datasets.

**Tell the examiner:** "I group similar order lines without target labels. I use the elbow plot to choose a reasonable cluster count and interpret each cluster from its sales characteristics."

**Viva:** Is a train-test split required here? Not for this descriptive exploratory clustering task; there is no supervised prediction score. Does the elbow guarantee the true number of groups? No; it is a heuristic.

## Reference notes
- Assignment scope and dataset URLs: supplied SPPU LP III.pdf, Group B.
- Preprocessing API: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
- Neural network concepts: https://scikit-learn.org/stable/modules/neural_networks_supervised.html
- These are complete teaching implementations. Record dataset version, software versions, actual scores and screenshots in your practical journal.

