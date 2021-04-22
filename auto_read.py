from sgfmill import sgf
import pandas as pd
import glob
import os
import read_write_path as rw


def save_table(result_dict, record_dict,save_index):
    # Save dictionary to pickle
    result_df = pd.DataFrame.from_dict(result_dict, "index")
    record_df = pd.DataFrame.from_dict(record_dict, "index")

    print('Saved: file',save_index)
    print(record_df.head(5))
    print(result_df.head(5))

    record_df.to_pickle(rw.save_table_path(f"go_record_table_new_{save_index}.pkl"))
    result_df.to_pickle(rw.save_table_path(f"go_result_table_new_{save_index}.pkl"))

path = r"/home/tatchakorn/Downloads/new gibo/"
path_list = os.listdir(path) # directory list
sgf_file_path = [os.path.join(path, _path, '*.sgf') for _path in path_list]

# generator expression for files end with '.sgf'
sgf_file_list = (glob.glob(_path) for _path in sgf_file_path)
sgf_files = (sgf_file for sgf_files in sgf_file_list for sgf_file in sgf_files)

record_dict = {} # The dictionary to pass to pandas DataFrame
result_dict = {}
dict_index = 0 # A counter used to add entries to "df_dict"
save_file_index = 0

# Extract data file sgf files
for sgf_file in sgf_files:
    try:                
        with open(sgf_file, "rb") as f:
            game = sgf.Sgf_game.from_bytes(f.read())
    except:
        # print("Read Error: at", sgf_file)
        continue

    # Get file name
    file_name = os.path.split(sgf_file)[-1]

    # Get game attributes
    b_player = game.get_player_name("b")
    w_player = game.get_player_name("w")
    
    # Ignore games without players' names   
    if b_player is None or w_player is None:
        continue
    try:
        root_node = game.get_root()
        b_rank = root_node.get("BR")
        w_rank = root_node.get("WR")
        result = root_node.get("RE")
    except:
        continue
    # List of the game sequence
    try:
        game_sequence = [node.get_move() for node in game.get_main_sequence()]
        game_sequence.pop(0)  # get rid of the first none sequence
    except ValueError:
        # print("game_sequence Error at:", sgf_file)
        continue
        
    # Append each attribute in a dictionary
    result_dict[dict_index] = {"File name": file_name,"Black player":b_player, "Black Rank":b_rank, "White player":w_player, "White Rank":w_rank, "Result":result}
    record_dict[dict_index] = {"File name": file_name,"Record":game_sequence}
    dict_index += 1
    if dict_index == 100000: # number of rows for each file
        save_table(result_dict, record_dict, save_file_index)
        
        result_dict.clear()
        record_dict.clear()
        save_file_index += 1
        dict_index = 0

if result_dict and record_dic: # if both not empty
    save_table(result_dict, record_dict, save_file_index)


