import matplotlib.pyplot as plt
import read_write_path as rw
import map_functions as m
import table_functions as tf
import pandas as pd
import numpy as np
import hashlib
import sys
import os
import re

'''
-> Record_table: File name, Record
-> Result_table: File name, Black player, Black Rank, White player, White Rank, Result
-> Player_table: name,  n_game,  n_win,  n_lose,  n_black, ETC...
-> rank_info_table: name, rank, op rank
-> level_up_player_table: name, rank, op rank, intervals
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

test_file_name = "58258547.sgf"
test_player_name = "lylotus"
name = 'shigepo'

df = rw.read_result_table_new()

tf.player_table(df)

# print(m.find_all_bot_games())

# df = rw.read_player_table()
# df.loc[]
# print(df.head())
# print(m.find_all_bot_games().describe)
# print(m.find_all_bot_games(), "\n") # 478206
# m.get_Unique_bots("both")




# m.check_ranks(check=True) # Rank list -> kyu, dan, pro
# df = m.find_player_ranks(test_player_name)

# sys.stdout = open(r'C:\power_rangers\out_buff.txt','w') # print to file 
# df = rw.read_record_table(0)
# df = rw.read_level_up_player_table()
# print(df.describe())
# f_index = 0
# df = rw.read_level_up_player_table()
# for index, player in df.iterrows():
#     games = m.find_player_games(player['name'])
#     name = hashlib.md5(player['name'].encode('UTF-8')).hexdigest()

#     games['Black player'] = games['Black player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
#     games['White player'] = games['White player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
#     print(name)
#     print(games.to_string())
#     # print(player)
    
#     # print(name)
#     # print(game)
#     # print(player[['rank', 'op rank']])

#     # --- Graph Stuff ---
#     plt.title(name)
#     plt.xlabel('Game')
#     plt.ylabel('Rank')
#     plt.style.use('seaborn')
    
#     x = [i for i in range(len(player['rank']))]
#     y1 = player['rank']
#     y2 = player['op rank']
    
#     plt.plot(x, y1, color = 'g', alpha=0.6)
#     plt.plot(x, y2, color = 'r', alpha=0.5)
#     plt.legend(['player rank','opponent rank'])
#     path = rw.save_graph_path(f'fuck_this_shit\\rank_graph_{f_index}.png')
#     f_index += 1
#     plt.savefig(path)
#     plt.cla()

# sys.stdout.close()


'''
df = rw.read_level_up_player_table()
for index, player in df.iterrows():

    games = m.find_player_games(player['name'])
    name = hashlib.md5(player['name'].encode('UTF-8')).hexdigest()

    games['Black player'] = games['Black player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
    games['White player'] = games['White player'].map(lambda name: hashlib.md5(name.encode('UTF-8')).hexdigest())
    print(name)
    print(games.to_string())
    # print(player)
    
    
    
    # print(name)
    # print(game)
    # print(player[['rank', 'op rank']])

    # --- Graph Stuff ---
    #  plt.title(name)
    # plt.xlabel('Game')
    # plt.ylabel('Rank')
    # plt.style.use('seaborn')
    
    # x = [i for i in range(len(player['rank']))]
    # y1 = player['rank']
    # y2 = player['op rank']
    
    # plt.plot(x, y1, color = 'g', alpha=0.6)
    # plt.plot(x, y2, color = 'r', alpha=0.5)
    # plt.legend(['player rank','opponent rank'])
    # path = rw.save_graph_path(f'rank_graph_{f_index}.png')
    # f_index += 1
    # plt.savefig(path)
    # plt.cla()
'''