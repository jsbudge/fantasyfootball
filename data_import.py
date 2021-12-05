import numpy as np
import pandas as pd
from tqdm import tqdm
from sportsipy.nfl.boxscore import Boxscore, Boxscores
from sportsipy.nfl.teams import Teams, Roster, Team

player_df = pd.DataFrame()
team_df = pd.DataFrame()

for yr in np.arange(2000, 2021):
    print(yr)
    boxes = Boxscores(1, yr, 17)
    for wk in tqdm(boxes.games):
        for game in boxes.games[wk]:
            box = Boxscore(game['boxscore'])
            away = pd.DataFrame()
            for dt in [p.dataframe for p in box.away_players]:
                away = away.append(dt)
            home = pd.DataFrame()
            for dt in [p.dataframe for p in box.home_players]:
                home = home.append(dt)
            away[['team_name', 'season', 'game_id']] = [game['away_name'], wk[-4:], game['boxscore']]
            home[['team_name', 'season', 'game_id']] = [game['home_name'], wk[-4:], game['boxscore']]
            player_df = player_df.append(away.reset_index())
            player_df = player_df.append(home.reset_index())

player_df = player_df.rename(columns={'index': 'player_name'})
player_df = player_df.set_index(['season', 'player_name', 'game_id'])

print('Getting team stats...')
for yr in np.arange(2000, 2021):
    print(yr)
    teams = Teams(yr)
    tdf_yr = teams.dataframes
    tdf_yr['season'] = yr
    team_df = team_df.append(tdf_yr)

player_df.to_csv('./data.csv')
team_df.to_csv('./tdata.csv')


