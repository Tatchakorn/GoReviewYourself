from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



path = r"C:\go_concat\new_player_table.pkl"
df = pd.read_pickle(path)

df = df.astype({"win%": "float", "win%_human": "float", "win%_bot": "float", "bot%": "float", "wb%": "float",
                "ww%": "float", "wb_human%": "float", "wb_bot%": "float", "ww_human%": "float", "ww_bot%": "float"})



plt.style.use("seaborn")
df = df.dropna()
df = df[["win%", "ww%", "wb%", "win%_human", "win%_bot", "wb_human%", "ww_human%", "ww_bot%", "wb_bot%"]]

# Scale the data so that each row the mean = 0 and std = 1
# The scale function expects samples to be rows so -> transpose it
scaled_data = preprocessing.scale(df.T)
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

print(pca_data.shape)


# scree plot
# Displays how much variation each principal component captures from the data
per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
labels = ['PC' + str(i) for i in range(1, len(per_var)+1)]

plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel("Variance Ratio%")
plt.xlabel("Principle components")
plt.title("Scree plot")
path = r"C:\go_concat\graph\pca_scree_plot.png"
plt.savefig(path)
plt.show()
index = ["win%", "ww%", "wb%", "win%_human", "win%_bot", "wb_human%", "ww_human%", "ww_bot%", "wb_bot%"]


# Draw PCA plot 
# A PCA plot shows clusters of samples based on their similarity.
pca_df = pd.DataFrame(pca_data, index=index, columns=labels)

plt.scatter(pca_df['PC1'], pca_df['PC2'])
plt.title('PCA Graph')
plt.xlabel('PC1 -{0}%'.format(per_var[0]))
plt.ylabel('PC2 -{0}%'.format(per_var[1]))

for i in pca_df.index:
    plt.annotate(i, (pca_df['PC1'].loc[i],pca_df['PC2'].loc[i]))

from k_mean import cluster_df
path = r"C:\go_concat\graph\pca_graph.png"
cluster_df(df=pca_df[["PC1","PC2"]], x_label="PC1", y_label="PC2", n_cluster=3,save_path=path, color_centroid=False)

print(pca_df["PC1"])
# A loading plot shows how strongly each characteristic influences a principal component.
loading_scores = pd.Series(pca.components_[0], index=df.index)
sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)
top_10_genes = sorted_loading_scores[0:10].index.values
print(loading_scores[top_10_genes])
# ----- END ----- ----- END ----- ----- END ----- ----- END ----- ----- END -----

'''
y_label = df.iloc[:, 0]

print(X)
pca = PCA(n_components=9)
pca.fit(X)

# print(pca.components_)
# print(pca.explained_variance_)
# print(pca.explained_variance_ratio_)

pca = PCA(n_components=1)
pca.fit(X)
X_pca = pca.transform(X)
print("original shape:   ", X.shape)
print("transformed shape:", X_pca.shape)

# new_df = {"name": df["name"].tolist(),"n_game":  df["n_game"].tolist(), "win%":  df["win%"].tolist(), "bot%":  df["bot%"].tolist(), "pca_1": X_new[:,0]}
print(X_pca)
new_df = {"name": df["name"].tolist(),"n_game":  df["n_game"].tolist(), "win%":  df["win%"].tolist(), "bot%":  df["bot%"].tolist(), "pca_1": X_pca[:,0]}
new_df = pd.DataFrame(new_df)
path = r"C:\go_concat\pca_new_table.pkl"
new_df.to_pickle(path)

X_new = pca.inverse_transform(X_pca)
print(new_df.head())

# plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
# plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
# plt.show()
# print(X_new[:, 0])
# print(X_new[:, 1])
# print(X_new[:, 2])
# print(X_new[:, 3])
# print(X_new[:, 4])
print(X_new[:,0])


# plt.axis('equal')
# plt.show()

pca2 = PCA(n_components=3)
pca2.fit(X_features)
x_3d = pca2.transform(X_features)
print(x_3d)

plt.figure(figsize=(8,6))
plt.scatter(x_3d[:,0], x_3d[:,1], c=df["n_game"], cmap="rainbow")

# X_new = pca2.inverse_transform(x_3d)
# plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
# plt.axis('equal')

# print(X_new[:, 0])


path = r"C:\go_concat\pca2.png"
plt.savefig(path)
plt.show()


# def color_player(row):
#     if row["bot%"] >= 60:
#         return "g"
#     else:
#         return "b"
# New color column indicate color
# df['color'] = df.apply (lambda row: color_player(row), axis=1)
'''