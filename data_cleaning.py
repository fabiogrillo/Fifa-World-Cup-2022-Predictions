import pandas as pd

# Data Cleaning

df_historical_data = pd.read_csv('./Data/fifa_worldcup_historical_data.csv')
df_fixture = pd.read_csv('./Data/fifa_worldcup_fixture.csv')
df_missing_data = pd.read_csv('./Data/fifa_worldcup_missing_data.csv')

# print(df_fixture)

## first we have to clean the data
# delete white spaces
df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

## cleaning df_missing_:data and adding it to df_historical_data
#print(df_missing_data[df_missing_data['home'].isnull()])
df_missing_data.dropna(inplace=True)
df_historical_data = pd.concat([df_historical_data, df_missing_data], ignore_index=True)
df_historical_data.drop_duplicates(inplace=True)
df_historical_data.sort_values('year', inplace=True)
# print(df_historical_data)

## Cleaning historical data
# first we delete match with walk over
delete_index = df_historical_data[df_historical_data['home'].str.contains('Sweden') &
                                  df_historical_data['away'].str.contains('Austria')].index

df_historical_data.drop(index=delete_index, inplace=True)

# cleanning score and home/away columns
df_historical_data['score'] = df_historical_data['score'].str.replace('[^\d–]', '', regex=True)
df_historical_data['home'] = df_historical_data['home'].str.strip() # clean blank spaces: Yugoslavia twice
df_historical_data['away'] = df_historical_data['away'].str.strip()

# splitting score columns into home and away goals and dropping score column
df_historical_data[['HomeGoals', 'AwayGoals']] = df_historical_data['score'].str.split('–', expand=True)
df_historical_data.drop('score', axis=1, inplace=True)

#renaming columns and changing data types
df_historical_data.rename(columns={'home':'HomeTeam', 'away':'AwayTeam', 'year':'Year'}, inplace=True)
df_historical_data = df_historical_data.astype({'HomeGoals': int, 'AwayGoals': int, 'Year': int})

#creating new column "totalgoals"
df_historical_data['TotalGoals'] = df_historical_data['HomeGoals'] + df_historical_data['AwayGoals']

# print(df_historical_data)