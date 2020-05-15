"""Counts the number of teams per state"""
import json
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os

df_team = pd.DataFrame()  # List of Teams

# pd.set_option('display.max_rows', None)

with urlopen(f'https://api.vexdb.io/v1/get_teams?country=united%20states&grade=High%20School') as resp:
    db = resp.read()
    db_data = json.loads(db)
    data = (db_data['result'])
    df_temp = pd.DataFrame.from_dict(data)
    df_team = df_team.append(df_temp, ignore_index=True)
df_team.rename(columns={'region': 'state'}, inplace=True)
print(df_team)

team_table = pd.pivot_table(
    df_team, index=['state', 'organisation'], aggfunc={'number': len})
print(team_table.sort_values(by='number', ascending=False))
