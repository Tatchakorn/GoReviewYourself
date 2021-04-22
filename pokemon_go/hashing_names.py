from sgfmill import sgf
import pandas as pd
import hashlib
import os


accessThis = f'player_table.pkl'
fileLoc = os.path.join(r'C:\go_concat', accessThis)
saveLoc = r'C:\go_concat\hashedName_project_table.pkl'
df = pd.read_pickle(fileLoc)
 
print(df, "\n\n") 

hashed = df
#hashed.name = hashed['name'].apply(hash)
#hashed.sort_values(by = ['n_game'], inplace = True)

hashed['name'] = [hashlib.md5(val.encode('UTF-8')).hexdigest() for val in hashed['name']]

print(hashed)

hashed.to_pickle(saveLoc)

#hashed.name = hashed[hashlib.md5(str.encode(i)).hexdigest()]