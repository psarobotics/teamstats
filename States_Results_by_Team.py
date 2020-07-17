"""Retrieve VEX Robotics Team data from vexdb.io and export to excel file"""

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
team_input = input(
    "Enter the team number (Do not add letter)  ")
for let in letr_list:
    with urlopen(f'https://api.vexdb.io/v1/get_teams?team={team_input}{let}') as resp:
        db = resp.read()
        db_data = json.loads(db)
        data = (db_data['result'])
        df_temp = pd.DataFrame.from_dict(data)
        df_team = df_team.append(df_temp, ignore_index=True)
df_team.drop(columns=['program', 'country'], inplace=True)
df_team.rename(columns={'region': 'state'}, inplace=True)
os.system('clear')
print(df_team)
print()

team_list = df_team['number']

season_list = ['Bridge%20Battle', 'Elevation', 'Clean%20Sweep', 'Round%20Up', 'Gateway', 'Sack%20Attack', 'Toss%20Up',
               'Skyrise', 'Nothing%20But%20Net', 'Starstruck', 'In%20The%20Zone', 'Turning%20Point', 'Tower%20Takeover', 'Change%20Up']

# List of seasons with start and end dates
S = {'season': ['Bridge Battle', 'Elevation', 'Clean Sweep', 'Round Up', 'Gateway', 'Sack Attack', 'Toss Up', 'Skyrise', 'Nothing But Net', 'Starstruck', 'In The Zone', 'Turning Point', 'Tower Takeover', 'Change Up'], 'start date': [
    '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'], 'end date': ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']}
#  List of awards with display order
A = {'award': ['Excellence Award', 'Tournament Champions', 'Tournament Finalists', 'Design Award', 'Judges Award', 'Robot Skills Champion', 'Amaze Award', 'Think Award', 'Innovate Award', 'Build Award', 'Create Award',
               'Online Challenge', 'Energy Award', 'Inspire Award', 'Service Award', 'Sportsmanship Award'], 'order': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']}
states_list = ['RE-VRC-10-3486', 'RE-VRC-11-6463', 'RE-VRC-13-9325', 'RE-VRC-14-0671', 'RE-VRC-15-1909', 'RE-VRC-16-3836',
               'RE-VRC-16-4303', 'RE-VRC-16-1501', 'RE-VRC-17-1912', 'RE-VRC-17-3161', 'RE-VRC-18-5973', 'RE-VRC-19-9740']

df_seasons = pd.DataFrame(data=S)
df_awardlist = pd.DataFrame(data=A)


def fetch_data(get):
    df_new = pd.DataFrame()
    print(f'fetching {get} data')
    for season in season_list:
        for team in team_list:
            with urlopen(f'https://api.vexdb.io/v1/{get}?team={team}&season={season}') as resp:
                db = resp.read()
                db_data = json.loads(db)
                data = (db_data['result'])
                df_temp = pd.DataFrame.from_dict(data)
                df_new = df_new.append(df_temp, ignore_index=True)
            print('.', end='', flush=True)
        print('.')
    return df_new


df_events = pd.DataFrame()
for state in states_list:
    for team in team_list:
        with urlopen(f'https://api.vexdb.io/v1/get_events?team={team}&sku={state}') as resp:
            db = resp.read()
            db_data = json.loads(db)
            data = (db_data['result'])
            df_temp = pd.DataFrame.from_dict(data)
            df_events = df_events.append(df_temp, ignore_index=True)

print('working.', end=' ')
#   Event list for each team
# df_events = fetch_data('get_events')
df_events[['start', 'delete']] = df_events['start'].str.split('T', expand=True)
df_events.drop(columns=['key', 'program', 'loc_address1', 'loc_address2',
                        'loc_postcode', 'loc_country', 'end', 'divisions', 'delete'], inplace=True)
df_events.rename(columns={'name': 'event', 'loc_venue': 'venue', 'loc_city': 'city',
                          'loc_region': 'state'}, inplace=True)
df_events.sort_values(by='start', ignore_index=True, inplace=True)
df_events.drop_duplicates(keep='first', inplace=True)

#  Rank for each event
df_rank = fetch_data('get_rankings')
df_rank.drop(columns=['division'], inplace=True)
df_rank.rename(columns={'team': 'number',
                        'rank': 'qualifying_rank'}, inplace=True)

#   Awards won at each event
df_award = fetch_data('get_awards')
df_award.rename(columns={'name': 'award', 'team': 'number'}, inplace=True)
#  Cleans up the award names and removes trailing space in award colunm
df_award[['award', 'vrc']] = df_award['award'].str.split('(', expand=True)
df_award = df_award.stack().str.rstrip().unstack()
df_award.drop(columns=['qualifies', 'order', 'vrc'], inplace=True)

#  Skills rankings for each event
df_skills = fetch_data('get_skills')
df_skills.rename(columns={'rank': 'skills_rank'}, inplace=True)
df_skills.drop(columns=['program'], inplace=True)
df_skills.replace({'type': {0: 'Driver', 1: 'Programming',
                               2: 'Combined'}}, inplace=True)
df_skills.rename(columns={'team': 'number'}, inplace=True)

#  Match detail for each event
# df_matches = fetch_data('get_matches')
# df_matches.drop(columns=['field', 'scored', 'scheduled'], inplace=True)
#   print(df_matches)

#    V-ranking for each season
df_vranking = fetch_data('get_season_rankings')
df_vranking.rename(columns={'team': 'number'}, inplace=True)

############################# DataFrame Merge ##################################

df_award = pd.merge(df_events, df_award, on='sku', how='left', sort=False)

df_vranking = pd.merge(df_vranking, df_team,
                       on='number', how='left', sort=False)
df_vranking = pd.merge(df_seasons, df_vranking,
                       on='season', how='left', sort=False)

# df_skills = pd.merge(df_skills, df_team, on='number',
#                     how='left', sort=False)  # merge dataframes
df_skills = pd.merge(df_events, df_skills, on='sku', how='left', sort=False)

df_results = pd.merge(df_events, df_rank, on='sku', how='left', sort=False)

############################# Column Names #####################################

# print('team: ', list(df_team))
# print('events: ', list(df_events))
# print('rank: ', list(df_rank))
# print('seasons: ', list(df_seasons))
# print('award list: ', list(df_awardlist))
# print()
# print('vranking: ', list(df_vranking))
# print('matches: ', list(df_matches))
# print('awards: ', list(df_award))
# print('skills: ', list(df_skills))
# print('results: ', list(df_results))

############################# Export to Excel ##################################

# with pd.ExcelWriter('/home/wandored/Google Drive/Vex Robotics/PSA_Robotics.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
#    df_results.to_excel(writer, sheet_name='Event Results', index=False)
#    df_award.to_excel(writer, sheet_name='Awards', index=False)
#    df_skills.to_excel(writer, sheet_name='Skills', index=False)
#    df_vranking.to_excel(writer, sheet_name='V-ranking', index=False)
#    df_matches.to_excel(writer, sheet_name='Matches', index=False)
#    df_team.to_excel(writer, sheet_name='Teams', index=False)
#    df_events.to_excel(writer, sheet_name='Events', index=False)
#    df_seasons.to_excel(writer, sheet_name='Seasons', index=False)
#    df_awardlist.to_excel(writer, sheet_name='Award List', index=False)

############################# Program Tables ###################################

input('Press Enter to continue...')
os.system('clear')
print('List of Awards and Program Totals')
award_table3 = pd.pivot_table(
    df_award, index=['award'], aggfunc={'award': len})
award_table3.index.names = ['Awards']
print(award_table3.sort_values(by='award', ascending=False))
print()

award_table = pd.pivot_table(
    df_award, index=['number'], aggfunc={'award': len})
if not award_table.empty:
    print('Awards won per Team')
    print(award_table.sort_values(by='award', ascending=False))
    print()

print('Program V-Rating - All Teams All Seasons')
vrank_table = pd.pivot_table(df_vranking, index=['organisation'], values={
    'vrating', 'vrating_rank'})
print(vrank_table.sort_values(by='vrating', ascending=False))
print()

print('Average V-Rating per Team All Seasons')
vrank_table = pd.pivot_table(df_vranking, index=['number'], values={
    'vrating', 'vrating_rank'})
print(vrank_table.sort_values(by='vrating', ascending=False))
print()

print('Average V-Rating per Season - All Teams')
vrank_table = pd.pivot_table(df_vranking, index=['season'], values={
    'vrating', 'vrating_rank'})
print(vrank_table.sort_values(by='vrating', ascending=False))
print()

################### Team Tables ################################################

for team in team_list:
    input('Press Enter to continue...')
    os.system('clear')
    print(f'######################## {team} #########################')
    filtered = df_award[df_award['number'] == f'{team}']
    award_table2 = pd.pivot_table(
        filtered, index=['award'], aggfunc={'award': len})
    award_table2.index.names = [f'{team}']
    if not award_table2.empty:
        print('Total Awards Won')
        print(award_table2.sort_values(by='award', ascending=False))
        print()

    filtered = df_award[df_award['number'] == f'{team}']
    award_table = pd.pivot_table(
        filtered, index=['season'], aggfunc={'award': len})
    if not award_table.empty:
        print('Awards Won per Season')
        print(award_table.sort_values(by='award', ascending=False))
        print()

    filtered = df_results[df_results['number'] == f'{team}']
    results_table1 = pd.pivot_table(
        filtered, index=['season'], values=['qualifying_rank'], aggfunc=np.mean)
    if not results_table1.empty:
        print('Average Qualifying Rank per Season')
        print(results_table1.sort_values(by='qualifying_rank'))
        print()

    filtered = df_results[df_results['number'] == f'{team}']
    results_table2 = pd.pivot_table(filtered, index=['season'], values=[
                                    'wins', 'losses', 'ties'], aggfunc=np.sum)
    if not results_table1.empty:
        print('Total Wins-Loss-Ties per Season')
        print(results_table2.sort_values(by='wins', ascending=False))
        print()

    filtered = df_results[df_results['number'] == f'{team}']
    results_table3 = pd.pivot_table(
        filtered, index=['season'], values=['wp', 'ap', 'sp'], aggfunc=np.mean)
    if not results_table1.empty:
        print('Average WP-AP-SP per Season')
        print(results_table3)
        print()

    filtered = df_results[df_results['number'] == f'{team}']
    results_table4 = pd.pivot_table(
        filtered, index=['season'], values=['opr', 'dpr', 'ccwm'], aggfunc=np.mean)
    if not results_table1.empty:
        print('Average opr-dpr-ccwm per Season')
        print(results_table4.sort_values(by='ccwm', ascending=False))
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
        print(award_table.sort_values(by='award', ascending=False))
        print()

    filtered = df_award[df_award['season'] == f'{season}']
    award_table = pd.pivot_table(
        filtered, index=['number'], aggfunc={'award': len})
    if not award_table.empty:
        print('Awards won per Team')
        print(award_table.sort_values(by='award', ascending=False))
        print()

    filtered = df_vranking[df_vranking['season'] == f'{season}']
    vrank_table = pd.pivot_table(filtered, index=['number'], values=[
        'vrating', 'vrating_rank'])
    if not vrank_table.empty:
        print('Rank by season V-Rating')
        print(vrank_table.sort_values(by='vrating', ascending=False))
        print()

    filtered = df_skills[df_skills['season'] == f'{season}']
    skills_table = pd.pivot_table(
        filtered, index=['number'], values=['score'], columns=['type'], aggfunc=np.max)
    if not skills_table.empty:
        print('Max Skills score per Team')
        print(skills_table)
        print()

    filtered = df_results[df_results['season'] == f'{season}']
    results_table1 = pd.pivot_table(
        filtered, index=['number'], values=['qualifying_rank'], aggfunc=np.mean)
    if not results_table1.empty:
        print('Season Average Qualifying Rank per Team')
        print(results_table1.sort_values(by='qualifying_rank'))
        print()

    filtered = df_results[df_results['season'] == f'{season}']
    results_table2 = pd.pivot_table(filtered, index=['number'], values=[
                                    'wins', 'losses', 'ties'], aggfunc=np.sum)
    if not results_table2.empty:
        print('Total Wins-Loss-Ties per Team')
        print(results_table2.sort_values(by='wins', ascending=False))
        print()

    filtered = df_results[df_results['season'] == f'{season}']
    results_table3 = pd.pivot_table(
        filtered, index=['number'], values=['wp', 'ap', 'sp'], aggfunc=np.mean)
    if not results_table3.empty:
        print('Average WP-AP-SP per Team')
        print(results_table3)
        print()

    filtered = df_results[df_results['season'] == f'{season}']
    results_table4 = pd.pivot_table(
        filtered, index=['number'], values=['opr', 'dpr', 'ccwm'], aggfunc=np.mean)
    if not results_table4.empty:
        print('Average opr-dpr-ccwm per Team')
        print(results_table4.sort_values(by='ccwm', ascending=False))
        print()

################################################################################

# with pd.ExcelWriter('/home/wandored/Google Drive/Vex Robotics/PSA_Tables.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
#    vrank_table.to_excel(writer, sheet_name='Vrank')
#    award_table.to_excel(writer, sheet_name='award')
#    award_table2.to_excel(writer, sheet_name='award2')
#    award_table3.to_excel(writer, sheet_name='award3')
#    skills_table.to_excel(writer, sheet_name='skills')
#    results_table1.to_excel(writer, sheet_name='results1')
#    results_table2.to_excel(writer, sheet_name='results2')
#    results_table3.to_excel(writer, sheet_name='results3')
#    results_table4.to_excel(writer, sheet_name='results4')
