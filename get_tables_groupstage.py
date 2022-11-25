import pandas as pd
import pickle
from string import ascii_uppercase as alphabet

all_tables = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')

#print(all_tables[20].to_string())
# from Group A to Group H: starting from all_tables[13] incrementing +7 for 8 times -> 69

dict_talbe = {}

for letter, i in zip(alphabet, range(13, 69, 7)):
    df = all_tables[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df.pop('Qualification')
    dict_talbe[f'Group {letter}'] = df

#print(dict_talbes['Group D'])

#now we export the dictionary

with open('./Data/dict_table', 'wb') as output:
    pickle.dump(dict_talbe, output)

