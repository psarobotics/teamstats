# VEX Robotics Team Statistics Aggregator

The python scripts below will pull data from the vexdb.io API and use pandas
to create dataframes and then pivot tables based on the teams you are looking
for.

### IMPORTANT!: Pivot tables can take a long time to create with a large dataframe.
For example StateStats for South Carolina can take an hour to run.

There are 7 different aspects that can be obtained through the API:
* Events
* Teams
* Matches
* Rankings
* Season Rankings
* Awards
* Skills

If you want to help improve these scripts checkout the issues section and 
have at it.


Below are the current scripts:

## TeamStats.py
TeamStats.py will request a team number and list all awards and tournament
stats for every team, each season the school competed.

## StateStats.py
StateStats.py will request a state and list all awards and tournament stats
for every team in the state, listing the top 25 for each category.

## States_Results_All_Teams.py, States_Results_by_Team.py
Pulls data only from State tournaments.

## Worlds_Results_All_Teams.py, Worlds_Results_by_Team.py
Pulls data only from Worlds tournaments.

## Nationals_Results_by_Team.py
Pulls data only from CREATE US Nationals tournaments.

## Teamcount.py
List all US teams and State Team Totals.

