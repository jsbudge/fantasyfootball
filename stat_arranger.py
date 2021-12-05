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

# Get the defensive stuff from team stats
