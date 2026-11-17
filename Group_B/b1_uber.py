import os
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(SCRIPT_DIR, "uber.csv") if not os.path.exists("uber.csv") else "uber.csv"

df = pd.read_csv(data_path).drop_duplicates()
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
fig.savefig(os.path.join(SCRIPT_DIR, "uber_correlation.png"), dpi=160)
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
