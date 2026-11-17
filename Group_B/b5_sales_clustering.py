import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(SCRIPT_DIR, "sales_data_sample.csv") if not os.path.exists("sales_data_sample.csv") else "sales_data_sample.csv"

df = pd.read_csv(
    data_path, encoding="latin-1"
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
plt.savefig(os.path.join(SCRIPT_DIR, "sales_elbow.png"), dpi=160)
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
df.to_csv(os.path.join(SCRIPT_DIR, "sales_clustered.csv"), index=False)

plt.scatter(
    imputed[:, 0], imputed[:, 2], c=labels,
    cmap="tab10", s=18, alpha=0.7
)
plt.xlabel("Quantity ordered")
plt.ylabel("Sales")
plt.title("Order-line clusters: two-feature view")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "sales_clusters.png"), dpi=160)
plt.show()
