import matplotlib.pyplot as plt
import read_write_path as rw
import map_functions as m
import pandas as pd
import numpy as np
import os
import re
import sys

'''
func(n1, n2)
return (games together)

'''
df = rw.read_level_up_player_table()

f_index = 0
for index, player in df.iterrows():
    print(player['name'])
    print(player['rank'])

    plt.title(player['name']) #.encode('utf-8')
    plt.xlabel('Game')
    plt.ylabel('Rank')
    plt.style.use('seaborn')

    x = [i for i in range(len(player['rank']))]
    y = player['rank']
    plt.plot(x, y, marker='o', color = '#88c999'           )
    path = rw.save_graph_path(f'fuck_this_shit\\rank_graph_{f_index}.png')
    f_index += 1
    plt.savefig(path)
    plt.cla()
