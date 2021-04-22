import read_write_path as rw
import map_functions as m
import pandas as pd
import numpy as np
import os

'''
-> Result_table: File name, Black player, Black Rank, White player, White Rank, Result
-> Player_table: name,  n_game,  n_win,  n_lose,  n_black, ...
-> Record_table: File name, Record

extract RANKS from each game from the result table FOR A GIVEN PLAYER NAME
loop through each player and read the result table, output the filename and the player’s rank 


order by file name
read (b/w) rank and player name
print df

input player name -> file name | rank
'''

name = 'shigepo' # search this player

# df = rw.read_result_table() # the original table
# print(df.loc[:,:], '\n') # show table

player = m.find_player_games(name) # table of 'name' player only
print(player.loc[:,:], '\n') # show table

playerRank = player.loc[:, ['File name']] # create new df

player.loc[player['Black player'].str.contains(name), 'rank'] = player["Black Rank"]
player.loc[player['White player'].str.contains(name), 'rank'] = player["White Rank"]
print(player)

playerRank['rank'] = player['rank'] #
print(playerRank.to_string())

# # bot_name = lambda df: (df["Black player"].str.contains('GoTrend', regex=False) | df["White player"].str.contains('GoTrend', regex=False))
# if (player.loc[player['Black player'].str.contains(name)], 'sth'):
#     df_rank = player.loc[player['Black player'].str.contains(name), 'sth'] = player.loc[:,'File name':'Black Rank']
#     # df_rank = player.loc[:,'File name':'Black Rank']
#     print(df_rank)

# if ((not with_bot) and (not with_human)) or (with_bot and with_human):