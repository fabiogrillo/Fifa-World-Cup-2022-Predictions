import pandas as pd
import pickle
from scipy.stats import poisson

dict_table = pickle.load(open('./Data/dict_table','rb'))
df_historical_data = pd.read_csv('./Data/clean_fifa_worldcup_matches.csv')
df_fixture = pd.read_csv('./Data/clean_fifa_worldcup_fixture.csv')

## Calculate Team Strength

df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

#print(df_home)

df_home = df_home.rename(columns={'HomeTeam':'Team', 'HomeGoals':'GoalsScored',
                                  'AwayGoals':'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam':'Team', 'HomeGoals':'GoalsConceded',
                                  'AwayGoals':'GoalsScored'})

# Here we concatenate the same team results using groupby
df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['Team']).mean()
#print(df_team_strength)

##Now we predict points for group stage
def predict_points(home, away):
    if home in df_team_strength.index and away in df_team_strength.index:
        # goals_scored * goals_conceded
        lamb_home = df_team_strength.at[home, 'GoalsScored'] * df_team_strength.at[away, 'GoalsConceded']
        lamb_away = df_team_strength.at[away, 'GoalsScored'] * df_team_strength.at[home, 'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0, 11):  # number of goals home team
            for y in range(0, 11):  # number of goals away team
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p

        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        return (points_home, points_away)
    else:
        return (0, 0)


# testing
# print(predict_points('England', 'United States'))
# print(predict_points('Argentina', 'Mexico'))
# print(predict_points('Qatar (H)', 'Ecuador')) # we don't have historical data for qatar -> 0, 0 output, just ignore it


## Now we're going to predict the whole world cup
df_fixture_group_48 = df_fixture[:48].copy()
df_fixture_knockout = df_fixture[48:56].copy()
df_fixture_quarter = df_fixture[56:60].copy()
df_fixture_semi = df_fixture[60:62].copy()
df_fixture_final = df_fixture[62:].copy()
# print(df_fixture_final)

for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values
    df_fixture_group_6 = df_fixture_group_48[df_fixture_group_48['home'].isin(teams_in_group)]
    for index, row in df_fixture_group_6.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)


        dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] += points_home
        dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += points_away

    dict_table[group] = dict_table[group].sort_values('Pts', ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team', 'Pts']]
    dict_table[group] = dict_table[group].round(0)