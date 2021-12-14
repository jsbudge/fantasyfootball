import numpy as np
import pandas as pd
from os.path import exists

fnme = './data.csv'
t_fnme = './tdata.csv'

if exists(fnme):
    df = pd.read_csv(fnme)
    df = df.set_index(['season', 'team_name'])
    # Take the stats for each player, add the other fantasy ones
    df['fantasy_points'] = df['pass_yards'] / 25 + df['rush_yards'] / 10 + 1 * df['receptions'] + 6 * df['touchdowns'] + \
                           df['extra_points'] - 2 * df['fumbles'] - 2 * df['interceptions']
if exists(t_fnme):
    tdf = pd.read_csv(t_fnme)
    tdf = tdf.set_index(['season', 'team_name'])

# Get the play-by-play data ready
for season in np.arange(2013, 2022):
    # Some unfortunate formatting means we have to clean the file
    pbp_fnme = './pbp_data/pbp-{}.csv'.format(season)
    pbp_clean_fnme = './pbp_data/pbp_{}.csv'.format(season)
    if not exists(pbp_clean_fnme):
        with open(pbp_clean_fnme, 'w') as wf:
            with open(pbp_fnme, 'r') as f:
                ln = f.readlines()
                for l in ln:
                    lc = l.replace('\\"', "|")
                    wf.write(lc)
    else:
        pbp_df = pd.read_csv(pbp_clean_fnme, sep=None, on_bad_lines='warn')
        # Fix some of the data with nans
        pbp_df = pbp_df.fillna(0)
        for col in pbp_df.columns:
            if 'Unnamed' in col:
                pbp_df = pbp_df.drop([col])

