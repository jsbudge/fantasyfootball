import numpy as np
import pandas as pd
import seaborn as sns
from re import search, findall
import matplotlib.pyplot as plt

RE_PNAME_PATTERN = '[0-9]{0,3}-.[.][A-Z-]+'
PASS_TYPES = ['DEEP_LEFT', '']

d_fnme = './pbp_data/pbp_2013.csv'
p_fnme = './pbp_data/pdata_2013.csv'

data = pd.read_csv(d_fnme, sep=None, on_bad_lines='warn')
data = data.fillna(0)
for col in data.columns:
    if 'Unnamed' in col:
        data = data.drop(columns=[col])

pdata = pd.read_csv(p_fnme)

data = data.loc[data['OffenseTeam'] == 'JAX']
id_cols = ['GameId', 'GameDate', 'OffenseTeam', 'DefenseTeam', 'SeasonYear', 'Description', 'PlayType', 'PenaltyType',
           'PenaltyYards', 'SeriesFirstDown', 'NextScore', 'TeamWin', 'Challenger', 'YardLineFixed',
           'YardLineDirection', 'PenaltyTeam'] + [col for col in data.columns if col[:2] == 'Is']
id_df = data[id_cols]
data = data.drop(columns=id_cols)
pass_df = data.loc[id_df['IsPass'] == 1].drop(columns=['RushDirection'])
run_df = data.loc[id_df['IsRush'] == 1].drop(columns=['PassType'])

pass_df['QB'] = 0
pass_df['R'] = 0
for idx, row in pass_df.iterrows():
    p_inv = findall(RE_PNAME_PATTERN, id_df.loc[idx, 'Description'])
    if len(p_inv) > 1:
        pass_df.loc[idx, ['QB', 'R']] = [p_inv[0], p_inv[1]]
    else:
        pass_df.loc[idx, 'QB'] = p_inv[0]

run_df['RB'] = 0
run_df.loc[run_df['RushDirection'] == 0, 'RushDirection'] = 'SCRAMBLE'
for idx, row in run_df.iterrows():
    p_inv = findall(RE_PNAME_PATTERN, id_df.loc[idx, 'Description'])
    run_df.loc[idx, 'RB'] = p_inv[0]

chenne = pass_df.loc[pass_df['QB'] == '7-C.HENNE']
mjdrew = run_df.loc[run_df['RB'] == '32-M.JONES-DREW']

plt.figure()
colors = ['red', 'blue', 'yellow', 'green', 'orange', 'black', 'cyan']
grp_idx = 0
for ptype, grp in chenne.groupby(['PassType']):
    if 'RIGHT' in ptype:
        for idx, row in grp.iterrows():
            plt.plot([0, 1 + np.random.rand() * .5 - .25], [np.random.rand(), row['Yards']], c=colors[grp_idx])
    elif 'LEFT' in ptype:
        for idx, row in grp.iterrows():
            plt.plot([0, -1 + np.random.rand() * .5 - .25], [np.random.rand(), row['Yards']], c=colors[grp_idx])
    else:
        for idx, row in grp.iterrows():
            plt.plot([0, np.random.rand() * .5 - .25], [np.random.rand(), row['Yards']], c=colors[grp_idx])
    grp_idx += 1

plt.figure()
colors = ['red', 'blue', 'yellow', 'green', 'orange', 'black', 'cyan', 'magenta']
grp_idx = 0
for ptype, grp in mjdrew.groupby(['RushDirection']):
    if 'RIGHT' in ptype:
        direction = 1
    elif 'LEFT' in ptype:
        direction = -1
    else:
        direction = 0
    if 'END' in ptype:
        direction *= 3
    elif 'GUARD' in ptype:
        direction *= 2
    for idx, row in grp.iterrows():
        plt.plot([0, direction + np.random.rand() * .5 - .25], [np.random.rand(), row['Yards']], c=colors[grp_idx])
    grp_idx += 1




