import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import glob

path = r"C:\go_concat\hashedName_project_table.pkl"
df = pd.DataFrame(pd.read_pickle(path))

n_game = df["n_game"].to_list()

def freq_count_(df, Range_list):
    n_game_count = []
    for i, j in Range_list:
        # i < n_game <= j 
        range_ = lambda df: (df["n_game"] > i) & (df["n_game"] < j)
        count_ = df.loc[range_].count()[0]
        n_game_count.append(count_)
    return n_game_count


# plt.style.use('seaborn')
# Range_list = [i*100 for i in range(10)]

# plt.hist(n_game, Range_list)
# plt.xlabel('number of games')
# plt.ylabel('number of players')

# path = r"C:\go_concat\graph\n_game_hist_0.png"
# plt.savefig(path)
# plt.show()

# Range_list = [i*100 for i in range(80)]

# plt.hist(n_game, Range_list)
# plt.xlabel('number of games')
# plt.ylabel('number of players')

# path = r"C:\go_concat\graph\n_game_hist_1.png"
# plt.savefig(path)
# plt.show()

# Bin size = 500 -> min = 0, max = 9000
# Range_list = [(i*500, (i+1) * 500) for i in range(18)]


# Bin size = 200 -> min = 0, max = 9000
# Range_list = [(i*200, (i+1) * 200) for i in range(45)]

# # Bin size = 100 -> min = 0, max = 9000
# Range_list = [(i*100, (i+1) * 100) for i in range(100)]
# print(freq_count_(df, Range_list))


# Bin size = 50 -> min = 0, max = 9000
# Range_list = [(i*50, (i+1) * 50) for i in range(200)]

range_ = lambda df: (df["n_game"] >= 150) & (df["n_game"] < 200)
count_ = df.loc[range_].count()[0]
print(count_)

df = df.sort_values(by="n_game")

print(df.tail().to_string())