"""Export PSA Robotics Team data to excel file"""

import json
from urllib.request import urlopen
import pandas as pd

team_list = ['9447A', '9447B', '9447C', '9447D', '9447F', '9447G', '9447H'\
        , '9447J', '9447K', '9447S']
seasons = ['Change%20Up', 'Tower%20Takeover', 'Turning%20Point', 'In%20The%20Zone'\
        , 'Starstruck', 'Nothing%20But%20Net', 'Bridge%20Battle', 'Elevation'\
        , 'Clean%20Sweep', 'Round%20Up', 'Gateway', 'Sack%20Attack', 'Toss%20Up', 'Skyrise']

df_team = pd.DataFrame() #List of Teams
df_rank = pd.DataFrame() #Event rankings for each season/team
df_award = pd.DataFrame() #List of awards won
df_skills = pd.DataFrame() #List of skills scores
df_matches = pd.DataFrame() #Match Details
df_searank = pd.DataFrame() #Season Rankings
df_events = pd.DataFrame() #Events

#pd.set_option('display.max_rows', None)

for team in team_list:
    with urlopen(f'https://api.vexdb.io/v1/get_teams?team={team}') as resp:
        teams = resp.read()
        team_data = json.loads(teams)
        data = (team_data['result'])
        df_temp = pd.DataFrame.from_dict(data)
        df_team = df_team.append(df_temp, ignore_index=True)
df_team.drop(columns=['program', 'country', 'grade', 'is_registered'], inplace=True)

for team in team_list:
    for season in seasons:
        with urlopen(f'https://api.vexdb.io/v1/get_rankings?team={team}&season={season}') as resp:
            teams = resp.read()
            team_data = json.loads(teams)
            data = (team_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_rank = df_rank.append(df_temp, ignore_index=True)

for team in team_list:
    for season in seasons:
        with urlopen(f'https://api.vexdb.io/v1/get_awards?team={team}&season={season}') as resp:
            teams = resp.read()
            team_data = json.loads(teams)
            data = (team_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_award = df_award.append(df_temp, ignore_index=True)
df_award.drop(columns=['qualifies', 'order'], inplace=True)

for team in team_list:
    for season in seasons:
        with urlopen(f'https://api.vexdb.io/v1/get_skills?team={team}&season={season}') as resp:
            teams = resp.read()
            team_data = json.loads(teams)
            data = (team_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_skills = df_skills.append(df_temp, ignore_index=True)

for team in team_list:
    for season in seasons:
        with urlopen(f'https://api.vexdb.io/v1/get_matches?team={team}&season={season}') as resp:
            teams = resp.read()
            team_data = json.loads(teams)
            data = (team_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_matches = df_matches.append(df_temp, ignore_index=True)
df_matches.drop(columns=['instance', 'field', 'scored', 'scheduled'], inplace=True)

for team in team_list:
    for season in seasons:
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={team}&season={season}') as resp:
            teams = resp.read()
            team_data = json.loads(teams)
            data = (team_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_searank = df_searank.append(df_temp, ignore_index=True)

drop_matches = df_matches.drop_duplicates(subset=['sku'], keep='last')
sku = drop_matches['sku']
for index, value in sku.items():
    with urlopen(f'https://api.vexdb.io/v1/get_events?sku={value}') as resp:
        teams = resp.read()
        team_data = json.loads(teams)
        data = (team_data['result'])
        df_temp = pd.DataFrame.from_dict(data)
        df_events = df_events.append(df_temp, ignore_index=True)
df_events.drop(columns=['key', 'program', 'loc_address1', 'loc_address2', 'end'], inplace=True)
df_events.sort_values(by='start', ascending=False, ignore_index=True, inplace=True)

print(df_team)
print(df_events)
print(df_rank)
print(df_searank)
print(df_award)
print(df_skills)
print(df_matches)

with pd.ExcelWriter('/home/wandored/Google Drive/Vex Robotics/PSA_Robotics.xlsx') as writer: # pylint: disable=abstract-class-instantiated
    df_team.to_excel(writer, sheet_name='Teams')
    df_events.to_excel(writer, sheet_name='Events')
    df_rank.to_excel(writer, sheet_name='Rankings')
    df_searank.to_excel(writer, sheet_name='Season Rank')
    df_award.to_excel(writer, sheet_name='Awards')
    df_skills.to_excel(writer, sheet_name='Skills')
    df_matches.to_excel(writer, sheet_name='Matches')
