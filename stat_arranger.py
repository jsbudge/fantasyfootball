import numpy as np
import pandas as pd

fnme = './data.csv'
t_fnme = './tdata.csv'

df = pd.read_csv(fnme)
df = df.set_index(['season', 'team_name'])
tdf = pd.read_csv(t_fnme)
tdf = tdf.set_index(['season', 'team_name'])

# Take the stats for each player, add the other fantasy ones
df['fantasy_points'] = df['pass_yards'] / 25 + df['rush_yards'] / 10 + 1 * df['receptions'] + 6 * df['touchdowns'] + \
                       df['extra_points'] - 2 * df['fumbles'] - 2 * df['interceptions']

# Get the play-by-play data ready
for season in np.arange(2013, 2022):
    # Some unfortunate formatting means we have to clean the file
    pbp_fnme = './pbp_data/pbp-{}.csv'.format(season)
    pbp_clean_fnme = './pbp_data/pbp_{}.csv'.format(season)
    with open(pbp_clean_fnme, 'w') as wf:
        with open(pbp_fnme, 'r') as f:
            ln = f.readlines()
            for l in ln:
                lc = l.replace('\\"', "|")
                wf.write(lc)
    pbp_df = pd.read_csv(pbp_clean_fnme, sep=None, on_bad_lines='warn')
