from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import read_write_path as rw
import map_functions as m
import seaborn as sns
import pandas as pd
import numpy as np
import hashlib

"""
convert_all_to_float (Only player table)

optimal_k
cluster_df
scatter_with_linReg
"""

def convert_all_to_float(df):

    df = df.astype({"win%": "float", "win%_human": "float", "win%_bot": "float", "bot%": "float", "wb%": "float", "ww%": "float", "wb_human%": "float", "wb_bot%": "float", "ww_human%": "float", "ww_bot%": "float"})
    return df


def scatter_with_linReg(dataframe, sort_val, ax_list, title, save_path=None, x_label, y_label):
    
    '''
    Plot scatter graph
    eg. scatter_with_linReg(dataframe=df_non_biased, sort_val="n_game", ax_list=["win%_bot", "win%_human", "win%"], title="All players", save_path=save_path, x_label="number of games", y_label="win rate")
    '''

    dataframe = dataframe.sort_values(by=sort_val, ascending=True, na_position='first')
    
    ax = dataframe.plot(kind="scatter", x=sort_val, y=ax_list[0], color="b", label=ax_list[0], title=title)
    if len(ax_list) > 1:
        dataframe.plot(kind="scatter", x=sort_val, y=ax_list[1], color="g", label=ax_list[1], ax=ax)
        if len(ax_list) > 2:
            dataframe.plot(kind="scatter", x=sort_val, y=ax_list[2], color="r", label=ax_list[2], ax=ax)
    
    # ----- Linear Regression ----- #
    sns.regplot(x=df[sort_val], y=df[ax_list[0]], color="b")
    if len(ax_list) > 1:
        sns.regplot(x=df[sort_val], y=df[ax_list[1]], color="g")
        if len(ax_list) > 2:
            sns.regplot(x=df[sort_val], y=df[ax_list[2]], color="r")
    
    # ----- Linear Regression ----- #
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.ylim(0, 100)

    if save_path:
        plt.savefig(save_path) # --> Save file <--
    
    plt.show()


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
        plt.savefig(save_path) # --> Save file <--
    plt.show()


def cluster_df(df, x_label, y_label, n_cluster, save_path=None, color_centroid=True):
    
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
    
    if save_path:
        plt.savefig(save_path) # --> Save file <--

    plt.show()

def plot_rank_game(player, f_index, x, y):
    plt.title(player)
    plt.xlabel('Game')
    plt.ylabel('Rank')
    plt.style.use('seaborn')
    plt.plot(x, y)
    path = rw.save_graph_path(f'rank_graph_{f_index}.png')
    plt.savefig(path)
    plt.cla()


def beautiful_graph():
    df = rw.read_level_up_player_table()
    f_index = 0
    for index, player in df.iterrows():

        games = m.find_player_games(player['name'])
        name = hashlib.md5(player['name'].encode('UTF-8')).hexdigest()

        games['Black player'] = games['Black player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
        games['White player'] = games['White player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
        print(name)
        print(games.to_string())
        print(name)
        print(player[['rank', 'op rank']])

        # --- Graph Stuff ---
        plt.title(name)
        plt.xlabel('Game')
        plt.ylabel('Rank')
        plt.style.use('seaborn')
        
        x = [i for i in range(len(player['rank']))]
        y1 = player['rank']
        y2 = player['op rank']
        
        plt.plot(x, y1, color = 'g', alpha=0.6)
        plt.plot(x, y2, color = 'r', alpha=0.5)
        plt.legend(['player rank','opponent rank'])
        path = rw.save_graph_path(f'fuck_this_shit\\rank_graph_{f_index}.png')
        f_index += 1
        plt.savefig(path)
        plt.cla()
    

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