import read_write_path as rw
import map_functions as m
import pandas as pd
import numpy as np
import hashlib
import glob
import re

# Find rows that have bot name (i.e. "Gotrend" in name)
bot_name = lambda df: (df["Black player"].str.contains('^GoTrend|^GT', regex=True) | df["White player"].str.contains('^GoTrend|^GT', regex=True))

def find_PlayerVsOpponent_games(player1, player2):
    df = rw.read_result_table()
    p_name = lambda df: (((df["Black player"] == player1) | (df["White player"] == player1)) & ((df["Black player"] == player2) | (df["White player"] == player2)))
    df_player = df.loc[p_name]
    return df_player

def find_player_rows(name):
    '''    
    name -> player_table
    Find player in player table
    '''
    df = rw.read_player_table()
    df = df[df["name"]==name]
    return df

def find_player_games(name, with_bot=False, with_human=False):

    '''    
    player_table -> result_table
    
    Find rows all games the player's name appear
    or only games played with bot
    '''

    df = rw.read_result_table()
    
    # Find rows that have player name
    p_name = lambda df: (df["Black player"] == name) | (df["White player"] == name)
    df_player = df.loc[p_name]

    if ((not with_bot) and (not with_human)) or (with_bot and with_human): # result of all games
        return df_player

    # Find rows that have bot name (i.e. "Gotrend" in name)
    if with_bot: # results of ONLY BOT games
        return df_player[bot_name]
    
    else: # results of ONLY HUMAN games
        human_name = lambda df: ~(df["Black player"].str.contains('^GoTrend|^GT', regex=True) | df["White player"].str.contains('^GoTrend|^GT', regex=True))
        return df_player[human_name]
        
def find_all_bot_games():
    '''    
    result_table
    
    Find games with bots 
    '''
    df = rw.read_result_table()
    return df[bot_name]
        
def get_Unique_bots(colour = "both"):
    df = m.find_all_bot_games()

    # Black bot
    black_bot = lambda df: df["Black player"].str.contains('^GoTrend|^GT', regex=True)
    black_set = set(df[black_bot]["Black player"].to_list())

    # White bot
    white_bot = lambda df: df["White player"].str.contains('^GoTrend|^GT', regex=True)
    white_set = set(df[white_bot]["White player"].to_list())

    unique_bots = black_set.union(white_set)

    if colour == "both":
        print(unique_bots)
        print("\n>> number of unique bots as both black and white <<")
        print(len(unique_bots))
    if colour == "black":
        print(black_set)
        print("\n>> number of unique bots as black <<")
        print(len(black_set))
    if colour == "white":
        print(white_set)
        print("\n>> number of unique bots as white <<")
        print(len(white_set))

def get_bot_rank(df):
    '''
    player_table -> player_table 
    Return a List of bots' ranks from player dataframe
    '''
    # Black bot
    black_bot = lambda df: df["Black player"].str.contains('^GoTrend|^GT', regex=True)
        
    # White bot
    white_bot = lambda df: df["White player"].str.contains('^GoTrend|^GT', regex=True)
        
    return df[black_bot]["Black Rank"].to_list() + df[white_bot]["White Rank"].to_list()


def get_game_record(file_name):
    '''
    result_table -> record_table
    '''
    
    for i in range(5): # 5 record tables

        print('reading:', i)
        df = rw.read_record_table(i)
        
        n_row = df.loc[df["File name"] == file_name].shape[0]
        
        if n_row:
            print('found at:', i)
            return df.loc[df["File name"] == file_name]
    print('file not found!')


def find_player_ranks(name):
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

    player = m.find_player_games(name) # table of 'name' player only

    playerRank = player.loc[:, ['File name']] # create new df

    # print(player) # see original table

    player.loc[player['Black player'].str.contains(name), 'rank'] = player["Black Rank"]
    player.loc[player['White player'].str.contains(name), 'rank'] = player["White Rank"]
    playerRank['rank'] = player['rank'] # add player's rank to dataframe
    
    player.loc[player['Black player'].str.contains(name), 'op_rank'] = player["White Rank"]
    player.loc[player['White player'].str.contains(name), 'op_rank'] = player["Black Rank"]
    playerRank['op_rank'] = player['op_rank'] # add opponent's rank to dataframe

    return playerRank

def check_ranks(check=False):
    '''
    Result table
    Check Ranks that exist in the result table
    '''
    df = rw.read_result_table()
    rank_set = set(df["Black Rank"].to_list()).union(set(df["White Rank"].to_list()))

    kyu_set = {i for i in rank_set if i[-1] == 'K'}
    rank_set = rank_set - kyu_set

    dan_set = {i for i in rank_set if i[-1] == 'D'}
    pro_set = rank_set - dan_set

    kyu_num = ' '.join(kyu_set)
    kyu_num = re.findall(r'\d+', kyu_num)
    kyu_num = list(map(int, kyu_num))
    kyu_num.sort()

    dan_num = ' '.join(dan_set)
    dan_num = re.findall(r'\d+', dan_num)
    dan_num = list(map(int, dan_num))
    dan_num.sort()


    pro_num = ' '.join(pro_set)
    pro_num = re.findall(r'\d+', pro_num)
    pro_num = list(map(int, pro_num))
    pro_num.sort()

    if check == True:
        print("Kyu Ranks:\n", kyu_set)
        print("Kyu numbers:\n", kyu_num)

        print("Dan Ranks:\n", dan_set)
        print("Dan numbers:\n", dan_num)

        print("Pro Ranks:\n", pro_set)
        print("Pro numbers:\n", pro_num)

    return kyu_set, dan_set, pro_set


def rank_to_num(rank):
    '''
    map kyu  ('40K', '1K') -> range(0,40)
    map dan  ('1D', '41D') -> range(40, 80)
    map pro  ('P1', 'P9') -> range(81, 89)
    '''
    
    rank_char = re.findall(r'\D', rank)[0]
    num = re.findall(r'\d+', rank)[0] # Extract number from string
    if rank_char == 'K': # kyu rank
        return np.abs(int(num) - 40)
    
    elif rank_char == 'D': # dan rank
        return int(num) + 39

    else: # pro rank
        return int(num) + 80
        

# ----- object ----- ----- object ----- ----- object ----- ----- object -----

def player_name_list(n_game=0):
    '''
    return a list of player name
    with specified number of games
    '''
    df = rw.read_player_table()
    if n_game:    
        df = df[df['n_game'] >= n_game]
    return df['name'].to_list()

def is_BotPlayer(name):
    '''
    check if the player is a bot player
    return a list of player name
    with specified number of games
    '''
    
    p_bot = float(m.find_player_info(name)["bot%"].values[0]) # bot% value
    
    if p_bot >= 60:
        return 1
    return 0

def hash_name(name):
    return hashlib.md5(name.encode('UTF-8')).hexdigest()
    
if __name__=="__main__": 
    
    df_player = find_player_games(name='tomo1990', with_bot=True, with_human=True)
    print(df_player.to_string())
    print(get_bot_rank(df_player))