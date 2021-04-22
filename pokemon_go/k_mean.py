from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def convert_all_to_float(df):

    df = df.astype({"win%": "float", "win%_human": "float", "win%_bot": "float", "bot%": "float", "wb%": "float",
                "ww%": "float", "wb_human%": "float", "wb_bot%": "float", "ww_human%": "float", "ww_bot%": "float"})
    return df

def optimal_k(df, save_path=None):

    '''
    Find the optimal k value for k mean clustering
    Specify two columns of the dataframe in df
    save to the save path if specified

    eg. optimal_k(df[['x', 'y']], save_path='C:\a_file\opti_k.png')
    '''

    K = range(1,15)
    Sum_of_squared_distances = []
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(df)
        Sum_of_squared_distances.append(km.inertia_)
    
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')

    if save_path:    
        plt.savefig(save_path)
    plt.show()


def cluster_df(df, x_label, y_label, n_cluster, modify=None, save_path=None, color_centroid=True):
    
    """
    Cluster 2d from dataframe with colored controids
    save to the save path if specified
    the graph can be modified by calling another function

    eg. cluster_df(df=df[['a', 'b']], x="bot%",y_label="win%", n_cluster=3)
    """
    
    
    kmeans = KMeans(n_clusters=n_cluster)
    kmeans.fit(df)

    plt.scatter(df.iloc[:,0], df.iloc[:,1], c=kmeans.labels_, cmap='rainbow')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Color centroids black
    x = kmeans.cluster_centers_[:,0]
    y = kmeans.cluster_centers_[:,1]
    if color_centroid:
        plt.scatter(x, y, color='black')
    
    # Modify the graph
    if modify:
        modify(x, y)

    if save_path:
        plt.savefig(save_path)

    plt.show()



if __name__=="__main__": 
    path = r"C:\go_concat\pca_new_table.pkl"
    df = pd.read_pickle(path)

    print(df.head().to_string())

    x = "bot%"
    y = "win%"

    plt.style.use("seaborn")
    df = df.sort_values(by=[x, y])
    new_df = df[[x, y]]

    print(new_df.head().to_string())
    path = r"C:\go_concat\graph\optimal_k_0_0.png"
    optimal_k(new_df, save_path=path)
    path = r"C:\go_concat\graph\kmean_0_0.png"
    cluster_df(df=new_df, x_label=x, y_label=y, n_cluster=3,save_path=path)