import matplotlib.pyplot as plt
import read_write_path as rw
import map_functions as m
import table_functions as tf
import pandas as pd
import numpy as np
import glob
import hashlib
import time
import sys
import os
import re
import shutil

'''
-> Record_table: File name, Record
-> Result_table: File name, Black player, Black Rank, White player, White Rank, Result
-> Player_table: name,  n_game,  n_win,  n_lose,  n_black, ETC...
-> rank_info_table: name, rank, op rank
-> level_up_player_table: name, rank, op rank, intervals

NEW

-> player_table_new + player_table_update =  player_table_concat
-> rank_info_table_new
-> unique_bot_table: , rank, n_game

'''

"""
TODO
read new sgf andread new sgf and make Record_table & Result_table
make player table

make a new table to make the rank the same as the bot rank
find GT bot and GoTrend
ammount of rank with the same rank
range of rank
"""


result_table =  rw.read_result_table()
player_table = rw.read_player_table()
unique_bot = rw.read_unique_bot()
bot_game = lambda df: df["Black player"].str.contains('^GoTrend|^GT', regex=True) | df["White player"].str.contains('^GoTrend|^GT', regex=True)
print(result_table[bot_game])
# print(unique_bot.info())
sys.exit()


# record_table = rw.read_record_table_new(1)
result_table = rw.read_result_table()
# rank_info_table = rw.read_rank_info_table()
# level_up_player_table = rw.read_level_up_player_table()

# tf.unique_bot_table(result_table)

unique_bot = rw.read_unique_bot()
print(unique_bot.to_string())

player_hash_name = player_table["name"].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
player_name = (i for i in player_hash_name)


for hash_name, name in zip(player_hash_name, player_table["name"]):
    if '201f6534909' in hash_name: # rank_graph_103
        print('Hashed:')
        print(hash_name)
        print('name:')
        print(name)
        name_f = name

# New sgf file path
path = r"/home/tatchakorn/Downloads/new gibo/"
path_list = os.listdir(path) # directory list
sgf_file_path = [os.path.join(path, _path, '*.sgf') for _path in path_list]
# generator expression for files end with '.sgf'
sgf_file_list = (glob.glob(_path) for _path in sgf_file_path)
sgf_files = (sgf_file for sgf_files in sgf_file_list for sgf_file in sgf_files)

counter_g = 0
for sgf_file in sgf_files:
    counter_g += 1
print(counter_g)
sys.exit()

player_game = m.find_player_games(name_f)
player_game = player_game["File name"].to_list()
for file_name in player_game:
    print(file_name)


player_game_path = [i for i in sgf_files if os.path.split(i)[-1] in player_game]

print(len(player_game_path))



dest_path = '/home/tatchakorn/Desktop/sgf_file_temp'

for game_path in player_game_path:
    g_file_name = os.path.split(game_path)[-1]
    dest = os.path.join(dest_path, g_file_name)
    print(g_file_name)
    print(dest)
    shutil.copyfile(game_path, dest) 

# print('+'*15)

# for sgf_file in sgf_files:
#     file_name = os.path.split(sgf_file)[-1]
#     print(file_name)

#     break
# 3e666d03069da7086237bfe49ac5f48e

