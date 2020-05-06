""" Export South Carolina Robotics Teams data to excel file"""

import json
from urllib.request import urlopen
import pandas as pd

season_list = ['Bridge%20Battle', 'Elevation', 'Clean%20Sweep', 'Round%20Up', 'Gateway', 'Sack%20Attack', 'Toss%20Up',
               'Skyrise', 'Nothing%20But%20Net', 'Starstruck', 'In%20The%20Zone', 'Turning%20Point', 'Tower%20Takeover', 'Change%20Up']

# List of seasons with start and end dates
S = {'season': ['Bridge Battle', 'Elevation', 'Clean Sweep', 'Round Up', 'Gateway', 'Sack Attack', 'Toss Up', 'Skyrise', 'Nothing But Net', 'Starstruck', 'In The Zone', 'Turning Point', 'Tower Takeover', 'Change Up'], 'start date': [
    '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'], 'end date': ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']}
A = {'award': ['Excellence Award', 'Tournament Champions', 'Tournament Finalists', 'Design Award', 'Judges Award', 'Robot Skills Champion', 'Amaze Award', 'Think Award', 'Innovate Award', 'Build Award', 'Create Award',
               'Online Challenge', 'Energy Award', 'Inspire Award', 'Service Award', 'Sportsmanship Award'], 'order': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']}
df_seasons = pd.DataFrame(data=S)
df_awardlist = pd.DataFrame(data=A)

df_team = pd.DataFrame()  # List of Teams
df_rank = pd.DataFrame()  # Event rankings for each season/team
df_award = pd.DataFrame()  # List of awards won
df_skills = pd.DataFrame()  # List of skills scores
df_matches = pd.DataFrame()  # Match Details
df_vranking = pd.DataFrame()  # Season Rankings
df_events = pd.DataFrame()  # Events

# pd.set_option('display.max_rows', None)

# Teams DataFrame
with urlopen(f'https://api.vexdb.io/v1/get_teams?region=South%20Carolina&grade=High%20School') as resp:
    teams = resp.read()
    team_data = json.loads(teams)
    data = (team_data['result'])
    df_temp = pd.DataFrame.from_dict(data)
    df_team = df_team.append(df_temp, ignore_index=True)
df_team.drop(columns=['program', 'country', 'grade'], inplace=True)
df_team.rename(columns={'region': 'state'}, inplace=True)
print(df_team)

team_list = df_team['number']  # create list of SC teams

# Rank for each event
for index, value in team_list.items():
    for season in season_list:
        with urlopen(f'https://api.vexdb.io/v1/get_rankings?team={value}&season={season}') as resp:
            rank = resp.read()
            rank_data = json.loads(rank)
            data = (rank_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_rank = df_rank.append(df_temp, ignore_index=True)
df_rank.drop(columns=['division'], inplace=True)
df_rank.rename(columns={'rank': 'qualifying_rank'}, inplace=True)
print(df_rank)

# Awards won at each event
for index, value in team_list.items():
    for season in season_list:
        with urlopen(f'https://api.vexdb.io/v1/get_awards?team={value}&season={season}') as resp:
            award = resp.read()
            award_data = json.loads(award)
            data = (award_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_award = df_award.append(df_temp, ignore_index=True)
df_award.rename(columns={'name': 'award'}, inplace=True)
# Cleans up the award names and removes trailing space in award colunm
df_award[['award', 'vrc']] = df_award['award'].str.split('(', expand=True)
df_award = df_award.stack().str.rstrip().unstack()
df_award.drop(columns=['qualifies', 'order', 'vrc'], inplace=True)
print(df_award)

# Skills rankings for each event
for index, value in team_list.items():
    for season in season_list:
        with urlopen(f'https://api.vexdb.io/v1/get_skills?team={value}&season={season}') as resp:
            skill = resp.read()
            skill_data = json.loads(skill)
            data = (skill_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_skills = df_skills.append(df_temp, ignore_index=True)
df_skills.rename(columns={'rank': 'skills_rank'}, inplace=True)
df_skills.drop(columns=['program'], inplace=True)
df_skills.replace(
    {'type': {0: 'Driver', 1: 'Programming', 2: 'Combined'}}, inplace=True)
print(df_skills)

# Match detail for each event
# for index, value in team_list.items():
#    for season in season_list:
#        with urlopen(f'https://api.vexdb.io/v1/get_matches?team={value}&season={season}') as resp:
#            match = resp.read()
#            match_data = json.loads(match)
#            data = (match_data['result'])
#            df_temp = pd.DataFrame.from_dict(data)
#            df_matches = df_matches.append(df_temp, ignore_index=True)
# df_matches.drop(columns=['instance', 'field',
#                         'scored', 'scheduled'], inplace=True)
# print(df_matches)

# V-ranking for each season
for index, value in team_list.items():
    for season in season_list:
        with urlopen(f'https://api.vexdb.io/v1/get_season_rankings?team={value}&season={season}') as resp:
            rank = resp.read()
            rank_data = json.loads(rank)
            data = (rank_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_vranking = df_vranking.append(df_temp, ignore_index=True)
print(df_vranking)

# remove duplicates for events
# drop_matches = df_matches.drop_duplicates(subset=['sku'], keep='first')
# sku = drop_matches['sku']

# for index, value in sku.items():
with urlopen(f'https://api.vexdb.io/v1/get_events?program=VRC&region=South%20Carolina') as resp:
    event = resp.read()
    event_data = json.loads(event)
    data = (event_data['result'])
    df_temp = pd.DataFrame.from_dict(data)
    df_events = df_events.append(df_temp, ignore_index=True)
df_events[['start', 'delete']] = df_events['start'].str.split('T', expand=True)
df_events.drop(columns=['key', 'program', 'loc_address1', 'loc_address2',
                        'loc_postcode', 'loc_country', 'end', 'divisions', 'delete'], inplace=True)
df_events.rename(columns={'name': 'event', 'loc_venue': 'venue',
                          'loc_city': 'city', 'loc_region': 'state'}, inplace=True)
df_events.sort_values(by='start', ignore_index=True, inplace=True)

print(df_events)
df_results = pd.merge(df_events, df_rank, on='sku',
                      how='left', sort=False)  # merge dataframes
print(df_results)

# print(list(df_results))
# print(list(df_team))
# print(list(df_events))
# print(list(df_rank))
# print(list(df_vranking))
# print(list(df_award))
# print(list(df_skills))
# print(list(df_matches))
# print(list(df_seasons))
# print(list(df_awardlist))

with pd.ExcelWriter('/home/wandored/Google Drive/Vex Robotics/SC_Robotics.xlsx') as writer:
    df_results.to_excel(writer, sheet_name='Event Results', index=False)
    df_award.to_excel(writer, sheet_name='Awards', index=False)
    df_skills.to_excel(writer, sheet_name='Skills', index=False)
    df_vranking.to_excel(writer, sheet_name='Vranking', index=False)
    df_team.to_excel(writer, sheet_name='Teams', index=False)
    df_events.to_excel(writer, sheet_name='Events', index=False)
    df_seasons.to_excel(writer, sheet_name='Seasons', index=False)
    df_awardlist.to_excel(writer, sheet_name='Award List', index=False)
    df_matches.to_excel(writer, sheet_name='Matches', index=False)
