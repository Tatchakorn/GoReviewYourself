import pandas as pd

path = r"C:\go_concat\raw_data\raw_01.pkl"
df = pd.read_pickle(path)
# df.to_csv(r"C:\go_concat\playerT.csv")
print(df.loc[:100,:].to_string)
print(df.loc[:100,"n_game":"bot%"])
# df = df.loc[:100,:]
