import pandas as pd
import os

def read_record_table(num):
    path = f"/home/tatchakorn/Desktop/documents/power_rangers/go_record_table_{num+1}.pkl"
    if num > 4:
        print(num, "file does not exist")
        return
        
    return pd.read_pickle(path)

def read_result_table():
    path = r"/home/tatchakorn/Desktop/documents/New_Table/result_table_concat.pkl"
    return pd.read_pickle(path)


def read_player_table():
    path = r"/home/tatchakorn/Desktop/documents/New_Table/player_table_update.pkl"
    return pd.read_pickle(path)

def read_rank_info_table():
    path = r"/home/tatchakorn/Desktop/documents/go_data/table/rank_info_table.pkl"
    return pd.read_pickle(path)

def read_level_up_player_table():
    path = r"/home/tatchakorn/Desktop/documents/go_data/table/level_up_player_table.pkl"
    return pd.read_pickle(path)

def read_record_table_new(num):
    path = f"/home/tatchakorn/Desktop/documents/New_Table/go_record_table_new_{num}.pkl"
    if num > 9:
        print(num, 'file does not exist')
        return
    return pd.read_pickle(path)

def read_unique_bot():
    path = r"/home/tatchakorn/Desktop/documents/New_Table/unique_bot.pkl"
    return pd.read_pickle(path)


# ----- Save ----- ----- Save ----- ----- Save ----- ----- Save -----

def save_stat_path(name):
    path = r"/home/tatchakorn/Desktop/project/_save_"
    return os.path.join(path, name)


def save_graph_path(name):
    path = r"/home/tatchakorn/Desktop/project/_save_"
    return os.path.join(path, name)


def save_table_path(name):
    path = r"/home/tatchakorn/Desktop/documents/New_Table"
    return os.path.join(path, name)
