""" Retrieve State Vex Robotics Data from vexdb.io and export to excel file"""

import json
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os

df_team = pd.DataFrame()  # List of Teams
df_rank = pd.DataFrame()  # Event rankings for each season/team
df_award = pd.DataFrame()  # List of awards won
df_skills = pd.DataFrame()  # List of skills scores
df_matches = pd.DataFrame()  # Match Details
df_vranking = pd.DataFrame()  # Season Rankings
df_events = pd.DataFrame()  # Events

# pd.set_option('display.max_rows', None)

letr_list = list(map(chr, range(65, 91)))

os.system('clear')  # use ('cls') for windows
print()
ST = [(ST) for ST in input("Enter the state you wish to check  ").split()]
if len(ST) == 2:
    f = ST.pop(0)
    l = ST.pop(0)
    with urlopen(f'https://api.vexdb.io/v1/get_teams?region={f}%20{l}&grade=High%20School') as resp:
        db = resp.read()
        db_data = json.loads(db)
        data = (db_data['result'])
        df_temp = pd.DataFrame.from_dict(data)
        df_team = df_team.append(df_temp, ignore_index=True)
    os.system('clear')
    print(df_team)
    print()
else:
    f = ST.pop(0)
    with urlopen(f'https://api.vexdb.io/v1/get_teams?region={f}&grade=High%20School') as resp:
        db = resp.read()
        db_data = json.loads(db)
        data = (db_data['result'])
        df_temp = pd.DataFrame.from_dict(data)
        df_team = df_team.append(df_temp, ignore_index=True)
    os.system('clear')
    print(df_team)
    print()
df_team.drop(columns=['program', 'country'], inplace=True)
df_team.rename(columns={'region': 'state'}, inplace=True)

team_list = df_team['number']

season_list = ['Bridge%20Battle', 'Elevation', 'Clean%20Sweep', 'Round%20Up', 'Gateway', 'Sack%20Attack', 'Toss%20Up',
               'Skyrise', 'Nothing%20But%20Net', 'Starstruck', 'In%20The%20Zone', 'Turning%20Point', 'Tower%20Takeover', 'Change%20Up']

# List of seasons with start and end dates
S = {'season': ['Bridge Battle', 'Elevation', 'Clean Sweep', 'Round Up', 'Gateway', 'Sack Attack', 'Toss Up', 'Skyrise', 'Nothing But Net', 'Starstruck', 'In The Zone', 'Turning Point', 'Tower Takeover', 'Change Up'], 'start date': [
    '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'], 'end date': ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']}
A = {'award': ['Excellence Award', 'Tournament Champions', 'Tournament Finalists', 'Design Award', 'Judges Award', 'Robot Skills Champion', 'Amaze Award', 'Think Award', 'Innovate Award', 'Build Award', 'Create Award',
               'Online Challenge', 'Energy Award', 'Inspire Award', 'Service Award', 'Sportsmanship Award'], 'order': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']}

df_seasons = pd.DataFrame(data=S)
df_awardlist = pd.DataFrame(data=A)


def fetch_data(get):
    df_new = pd.DataFrame()
    for season in season_list:
        for team in team_list:
            with urlopen(f'https://api.vexdb.io/v1/{get}?team={team}&season={season}') as resp:
                db = resp.read()
                db_data = json.loads(db)
                data = (db_data['result'])
                df_temp = pd.DataFrame.from_dict(data)
                df_new = df_new.append(df_temp, ignore_index=True)
    return df_new


#   Event list for each team
df_events = fetch_data('get_events')
df_events[['start', 'delete']] = df_events['start'].str.split('T', expand=True)
df_events.drop(columns=['key', 'program', 'loc_address1', 'loc_address2',
                        'loc_postcode', 'loc_country', 'end', 'divisions', 'delete'], inplace=True)
df_events.rename(columns={'name': 'event', 'loc_venue': 'venue', 'loc_city': 'city',
                          'loc_region': 'state'}, inplace=True)
df_events.sort_values(by='start', ignore_index=True, inplace=True)
df_events.drop_duplicates(keep='first', inplace=True)

#   Awards won at each event
df_award = fetch_data('get_awards')
df_award.rename(columns={'name': 'award', 'team': 'number'}, inplace=True)
#  Cleans up the award names and removes trailing space in award colunm
df_award[['award', 'vrc']] = df_award['award'].str.split('(', expand=True)
df_award = df_award.stack().str.rstrip().unstack()
df_award.drop(columns=['qualifies', 'order', 'vrc'], inplace=True)

df_award = pd.merge(df_events, df_award, on='sku', how='left', sort=False)
df_award = pd.merge(df_award, df_team, on='number', how='left', sort=False)

input('Press Enter to continue...')
os.system('clear')
print('List of all Awards Won by all Schools')
award_table3 = pd.pivot_table(
    df_award, index=['award'], aggfunc={'award': len})
award_table3.index.names = ['Awards']
print(award_table3.sort_values(by='award', ascending=False))
print()

print('List of all Awards Won by all Schools')
award_table = pd.pivot_table(
    df_award, index=['award'], columns=['organisation'], aggfunc={'award': len})
award_table.index.names = ['Awards']
print(award_table.sort_values(by='award', ascending=False).head(10))
print()

award_table = pd.pivot_table(
    df_award, index=['organisation'], aggfunc={'award': len})
if not award_table.empty:
    print('Awards won per School')
    print(award_table.sort_values(by='award', ascending=False).head(25))
    print()

award_table = pd.pivot_table(
    df_award, index=['number'], aggfunc={'award': len})
if not award_table.empty:
    print('Awards won per Team')
    print(award_table.sort_values(by='award', ascending=False).head(25))
    print()

################### Season Results #############################################
seasons = df_seasons['season']

for season in seasons:
    input('Press Enter to continue...')
    os.system('clear')
    print(f'######################## {season} #########################')
    filtered = df_award[df_award['season'] == f'{season}']
    award_table = pd.pivot_table(
        filtered, index=['award'], aggfunc={'award': len})
    award_table.index.names = ['Awards']
    if not award_table.empty:
        print(f'Awards won - {season}')
        print(award_table.sort_values(by='award', ascending=False).head(25))
        print()

    filtered = df_award[df_award['season'] == f'{season}']
    award_table = pd.pivot_table(
        filtered, index=['organisation'], aggfunc={'award': len})
    if not award_table.empty:
        print('Awards won per School')
        print(award_table.sort_values(by='award', ascending=False).head(25))
        print()

    filtered = df_award[df_award['season'] == f'{season}']
    award_table = pd.pivot_table(
        filtered, index=['number'], aggfunc={'award': len})
    if not award_table.empty:
        print('Awards won per Team')
        print(award_table.sort_values(by='award', ascending=False).head(25))
        print()
