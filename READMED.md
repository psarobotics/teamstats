# VEX Robotics Team Statistics Aggregator

The goal of this script is to pull the requested team data from the vexdb.io database and display the stats to the user.

There are 7 different aspects that can be obtained through the API:
* Events
* Teams
* Matches
* Rankings
* Season Rankings
* Awards
* Skills

## To-Do List
[ ] User inputs team or all teams are used
[ ] User inputs State or all states are used
[ ] User inputs Season or all seasons are used
[ ] User inputs Event sku or all events are used
[X] Data retrieved from database and placed into dataframes
[ ] Pivot Tables created
    * Event Results - if multiple events/states is selected tables will list top 10
        * W-L-T
        * WP-AP-SP-TRSP
        * OPR-DPR-CCWM
    * Awards
    * Skills Results
    * V-Ranking
[ ] Pivot Tables and charts posted to display
