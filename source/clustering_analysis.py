import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

conn = sqlite3.connect("players.db")
df = pd.read_sql_query("SELECT * FROM players", conn)
conn.close()

non_numeric = ["player", "team", "nationality", "position"]

df_num = df.drop(columns=non_numeric)
df_num = df_num.apply(pd.to_numeric, errors='coerce')
df_num = df_num.dropna()
scaler = StandardScaler()
X = scaler.fit_transform(df_num)
# Elbow method
inertia = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

plt.figure()
plt.plot(K_range, inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("Số cụm (k)")
plt.ylabel("Inertia")
plt.show()

# Silhouette
sil_scores = []

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    sil_scores.append(silhouette_score(X, labels))

plt.figure()
plt.plot(K_range, sil_scores, marker='o')
plt.title("Silhouette Score")
plt.xlabel("Số cụm (k)")
plt.ylabel("Score")
plt.show()

# Chọn k
k = 4

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)
# PCA 2D
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=df["cluster"], cmap='viridis', alpha=0.6)
plt.colorbar(scatter, label='Cluster ID') 
import random
random_indices = random.sample(range(len(df)), min(15, len(df)))
for i in random_indices:
    plt.annotate(df['player'].iloc[i], 
                 (X_2d[i, 0], X_2d[i, 1]), fontsize=8, alpha=0.9, xytext=(5, 5), textcoords='offset points')

plt.title("PCA 2D Clustering")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()
# PCA 3D
from mpl_toolkits.mplot3d import Axes3D

pca_3d = PCA(n_components=3)
X_3d = pca_3d.fit_transform(X)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

p = ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], c=df["cluster"], cmap='viridis', s=50, alpha=0.6)

fig.colorbar(p, ax=ax, label='Cluster ID', shrink=0.5)

ax.set_title("PCA 3D Clustering")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")

ax.view_init(elev=20, azim=45) 
plt.show()
df.to_csv("players_clustered.csv", index=False)

print(" Đã phân cụm và lưu file players_clustered.csv")