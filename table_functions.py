from pympler.asizeof import asizeof
import read_write_path as rw
import graph_functions as g
import map_functions as m
import pandas as pd
import numpy as np
import glob
import sys
import os
import re


'''
-> Player_table: name,  n_game,  n_win,  n_lose,  n_black, ETC...
-> Record_table: File name, Record
-> Result_table: File name, Black player, Black Rank, White player, White Rank, Result
-> rank_info_table: name, rank, op rank
-> level_up_player_table: name, rank, op rank, intervals
'''

def concat_table(path, file_name):
    """
        Combine all '.pkl' files in a folder
    """
    print("Concatinating..")

    files = glob.glob(os.path.join(path, '*.pkl'))
    print(files)

    df = pd.concat([pd.read_pickle(pkl) for pkl in files], ignore_index=True)

    save_path = rw.save_table_path(file_name)
    df.to_pickle(save_path)
    print("done!")


def split_df_in_half(df):
    """
        split a '.pkl' file in half
    """
    print('original file size:', asizeof(df), 'bytes')

    path = rw.save_table_path("sep_01.pkl")

    sep_1 = df.iloc[0:df.shape[0] // 2]
    sep_1.to_pickle(path)   # --> Save file <--

    print('file 1 size:', asizeof(sep_1), 'bytes')
    path = rw.save_table_path("sep_02.pkl")

    sep_2 = df.iloc[df.shape[0] // 2:df.shape[0]] 
    sep_2.to_pickle(path)   # --> Save file <--

    print('file 2 size:', asizeof(sep_2), 'bytes')
    

def Freq_table():
    # The dictionary to pass to pandas DataFrame
    df_dict = {}
    df_dict_index = 0

    for player in m.player_name_list():
        
        game_list = m.find_player_games(player)
        # len(game.index) -> The fastest way to get # of rows
        if len(game_list.index) == 0:
            continue

        # Extract file name (discard file extension)        
        game_list = list(set(game_list['File name'].to_list())) # Get rid of the same file names
        game_list = [int(os.path.splitext(game)[0]) for game in game_list]
        
        game_list.sort(reverse=True)
        game_diff = np.array([(game_list[i]-game_list[i+1]) for i in range(len(game_list)-1)])    

        # Game diff table
        if len(game_diff) == 0:
            continue
        df_dict[df_dict_index] = {"name":player,"min":np.min(game_diff), "max":np.max(game_diff), "avg": np.average(game_diff)}
        df_dict_index += 1

    df = pd.DataFrame.from_dict(df_dict, "index")
    path = rw.save_table_path('Freq_table.pkl')
    df.to_pickle(path) # --> Save file <--
    
def rank_info_table():
    i = 0
    # The dictionary to pass to pandas DataFrame
    df_dict = {}
    df_dict_index = 0

    for player in m.player_name_list(n_game=60):

        try:
            df = m.find_player_ranks(player)
        except:
            continue

        try:
            rank_list = [m.rank_to_num(i) for i in df["rank"].to_list()]
            if not len(rank_list):
                continue
            op_rank_list = [m.rank_to_num(i) for i in df["op_rank"].to_list()]
            deriv_rank_list = [rank_list[i+1]-rank_list[i] for i in range(len(rank_list)-1)]
            deriv = list(filter(lambda a: a != 0, deriv_rank_list))

        except:
            print('error')
            continue
        # print('name:', player.encode('utf-8'))
        # print('rank:\n', rank_list)
        # print('op_rank:\n', op_rank_list)
        # print('change:\n', deriv_rank_list)
        # print('nonzero:\n', deriv)

        x = [i for i in range(len(rank_list))]
        # Doesn't work
        # x_labels = [os.path.splitext(i)[0] for i in df["File name"]]
        # plt.xticks(x, x_labels, rotation='vertical')
        
        g.plot_rank_game(player=player, f_index=i, x=x, y=rank_list)
        i += 1
        
        df_dict[df_dict_index] = {"name":player,"rank":rank_list, "op rank":op_rank_list}
        df_dict_index += 1

    df = pd.DataFrame.from_dict(df_dict, "index")
    path = rw.save_table_path('rank_info_table.pkl')
    df.to_pickle(path) # --> Save file <--


def level_up_player_table():
    df = rw.read_rank_info_table()

    # The dictionary to pass to pandas DataFrame
    df_dict = {}
    df_dict_index = 0

    def Check_rank_Change(sub_rank):
        if sub_rank[0] == sub_rank[5]:
            return 0

        elif sub_rank[0] < sub_rank[5]: # Rank Increase
            return 1
        else:
            return -1

    weird_index = 0

    for index, player in df.iterrows():

        if len(player['rank']) <= 60:
            continue
        
        rank_list = player['rank']
        
        n = len(rank_list)

        range_a = range((n-60))
        range_b = range(60, n)

        num_interval = 0 # +1 If level up in the interval
        
        print('name: ', end='')
        print(player['name'].encode('utf-8'))
            

        for i, j in zip(range_a, range_b):
            sub_rank = rank_list[i:j] # 60 games
            sub_1 = rank_list[0:6] # Start of section
            sub_2 = rank_list[54:60] # End of section

            
            
            if Check_rank_Change(sub_1) == 1 and Check_rank_Change(sub_2) == 1:
                num_interval += 1
            
        if num_interval == 0: # No level up between each interval
            continue

        sub_1 = rank_list[0:6] # Start of section
        sub_2 = rank_list[54:60] # End of section
            
        df_dict[df_dict_index] = {"name":player['name'],"rank":player['rank'], "op rank":player['op rank'], "num_interval":num_interval}
        df_dict_index += 1

    df = pd.DataFrame.from_dict(df_dict, "index")
    path = rw.save_table_path('level_up_player_table.pkl')
    df.to_pickle(path) # --> Save file <--

def rank_diff_table():    
    df = rw.read_level_up_player_table()

    df_dict = {}
    df_dict_index = 0

    for index, player in df.iterrows():
        
        df_dict[df_dict_index] = {"name":m.hash_name(player['name']), "original rank":player['rank'][0], "Interval":60, "player rank avg":np.average(player["rank"]), 
                                "opponent rank avg":np.average(player["op rank"]), "bot player":m.is_BotPlayer(player['name']), 
                                "rank difference":player["rank"][-1] - player["rank"][0]}
        df_dict_index += 1



    df = pd.DataFrame.from_dict(df_dict, "index")
    path = rw.save_table_path('Rank_diff.csv')
    df.to_csv(path)# --> Save file <--



def player_table(Result_table):
    """
    /////---------- Parameters Description ----------/////
    "n_game": Total number of games
    "n_win": Number of games the player's won
    "n_lose": Number of games the player's lost
    "n_black": Number of games played as black
    "n_white": Number of games played as white
    "n_human": Number of games played with other players
    "n_win_human": Number of games won against other players
    "n_bot": Number of games played with bots
    "n_win_bot": Number of games won against bots
    "n_wb": Number of games won as black
    "n_ww": Number of games won as white
    "n_wb_human": Number of games won as black against other players
    "n_ww_human": Number of games won as white against other players
    "n_wb_bot": Number of games won as black against bots
    "n_ww_bot": Number of games won as white against bots
    "win%": Win rate
    "win%_human": Win rate against human
    "win%_bot": Win rate against bot
    "bot%": Percentage of bot games
    "wb%": Win rate as black
    "ww%": Win rate as white
    "wb_human%": Win rate against other players as black
    "wb_bot%": Win rate against bots as black
    "ww_human%": Win rate against other players as white
    "ww_bot%": Win rate against bots as white
    The dictionary to pass to pandas DataFrame
    /////---------- Parameters Description ----------/////
    """

    df_dict = {}
    # A counter used to add entries to "df_dict"
    df_dict_index = 0


    # Union sets of black and white player to get all players' names
    b_player_list = {player for player in Result_table["Black player"]}
    w_player_list = {player for player in Result_table["White player"]}
    all_player = b_player_list.union(w_player_list)                                             # total of all players (human and bot)

    # Bot names begin with "GoTrend" or "GT"
    r = re.compile('^GoTrend|^GT')
    bots = set(filter(r.match, all_player)) # bots    
    human_player = all_player - bot_player                                                      # human players total

    for player_name in human_player:
        # The rows that the player's name appear
        sub_df = Result_table.loc[(Result_table["Black player"] == player_name) | (Result_table["White player"] == player_name)]

        # Count the total  number of games by the number of rows of sub_df
        n_game = len(sub_df.index)                                                       # total games
        # Count everything
        count_bot = 0
        count_win = 0
        count_win_bot = 0

        # Count win as black or white
        count_black = 0
        count_wb = 0
        count_wb_bot = 0

        for index, row in sub_df.iterrows():
            if "GoTrend" in row["Black player"] or "GoTrend" in row["White player"]:
                count_bot += 1
                play_with_bot = True
            else:
                play_with_bot = False

            if player_name == row["Black player"]:
                count_black += 1
                if "B" in row["Result"]:
                    count_win += 1
                    count_wb += 1
                    if play_with_bot:
                        count_win_bot += 1
                        count_wb_bot += 1

            if player_name == row["White player"] and "W" in row["Result"]:
                count_win += 1
                if play_with_bot:
                    count_win_bot += 1

        n_human = n_game - count_bot
        n_win_human = count_win - count_win_bot
        n_lose = n_game - count_win
        n_white = n_game - count_black
        n_ww = count_win - count_wb
        n_ww_bot = count_win_bot - count_wb_bot
        n_wb_human = count_wb - count_wb_bot
        n_ww_human = n_ww - n_ww_bot

        try:
            win_rate = "{:.2f}".format(count_win/n_game*100)
        except ZeroDivisionError:
            win_rate = np.nan

        try:
            win_rate_bot = "{:.2f}".format(count_win_bot / count_bot*100)
        except ZeroDivisionError:
            win_rate_bot = np.nan

        try:
            win_rate_human = "{:.2f}".format(n_win_human/n_human*100)
        except ZeroDivisionError:
            win_rate_human = np.nan

        try:
            p_bot = "{:.2f}".format(count_bot/n_game*100)
        except ZeroDivisionError:
            p_bot = np.nan

        try:
            p_wb = "{:.2f}".format(count_wb/count_win*100)
        except ZeroDivisionError:
            p_wb = np.nan

        try:
            p_ww = "{:.2f}".format(n_ww/count_win*100)
        except ZeroDivisionError:
            p_ww = np.nan

        try:
            p_wb_human = "{:.2f}".format(n_wb_human/count_wb*100)
        except ZeroDivisionError:
            p_wb_human = np.nan

        try:
            p_ww_human = "{:.2f}".format(n_ww_human/n_ww*100)
        except ZeroDivisionError:
            p_ww_human = np.nan

        try:
            p_wb_bot = "{:.2f}".format(count_wb_bot/count_wb*100)
        except ZeroDivisionError:
            p_wb_bot = np.nan

        try:
            p_ww_bot = "{:.2f}".format(n_ww_bot/n_ww*100)
        except ZeroDivisionError:
            p_ww_bot = np.nan
            
        # Add data to a dictionary
        
        df_dict[df_dict_index] = {"name": player_name, "n_game": n_game, "n_win": count_win, "n_lose": n_lose,
                                "n_black": count_black, "n_white": n_white, "n_human": n_human, "n_win_human": n_win_human,
                                "n_bot": count_bot, "n_win_bot": count_win_bot,
                                "n_wb": count_wb, "n_ww": n_ww, "n_wb_human": n_wb_human, "n_ww_human": n_ww_human,
                                "n_wb_bot": count_wb_bot, "n_ww_bot": n_ww_bot, "win%": win_rate, "win%_human": win_rate_human,
                                "win%_bot": win_rate_bot, "bot%": p_bot, "wb%": p_wb, "ww%": p_ww,
                                "wb_human%": p_wb_human, "wb_bot%": p_wb_bot, "ww_human%": p_ww_human, "ww_bot%": p_ww_bot}
        df_dict_index += 1

    human_df = pd.DataFrame.from_dict(df_dict, "index")
    human_df.info()
    save_path = rw.save_table_path("player_table_new.pkl")
    human_df.to_pickle(save_path)


if __name__=="__main__": 
    print("Heil Loo!")