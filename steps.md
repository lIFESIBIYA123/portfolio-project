Steps on portfolio projects

.../portfolio-project (main) $ cd chapter3
.../chapter3 (main) $ sqlite3 fantasy_data.db
SQLite version 3.45.3 2024-04-15 13:34:05
Enter ".help" for usage hints.
sqlite>

2.Adding the dict

execute this terminal command: source ~/.bashrc.

3. creating tables

CREATE TABLE player (
player_id INTEGER NOT NULL,
gsis_id VARCHAR,
first_name VARCHAR NOT NULL,
last_name VARCHAR NOT NULL,
position VARCHAR NOT NULL,
last_changed_date DATE NOT NULL,
PRIMARY KEY (player_id)
);
CREATE TABLE performance (
performance_id INTEGER NOT NULL,
week_number VARCHAR NOT NULL,
fantasy_points FLOAT NOT NULL,
player_id INTEGER NOT NULL,
last_changed_date DATE NOT NULL,
PRIMARY KEY (performance_id),
FOREIGN KEY(player_id) REFERENCES player (player_id)
);
CREATE TABLE league (
league_id INTEGER NOT NULL,
league_name VARCHAR NOT NULL,
scoring_type VARCHAR NOT NULL,
last_changed_date DATE NOT NULL,
PRIMARY KEY (league_id)
);
CREATE TABLE team (
team_id INTEGER NOT NULL,
team_name VARCHAR NOT NULL,
league_id INTEGER NOT NULL,
last_changed_date DATE NOT NULL,
PRIMARY KEY (team_id),
FOREIGN KEY(league_id) REFERENCES league (league_id)
);
CREATE TABLE team_player (
team_id INTEGER NOT NULL,
player_id INTEGER NOT NULL,
last_changed_date DATE NOT NULL,
PRIMARY KEY (team_id, player_id),
FOREIGN KEY(team_id) REFERENCES team (team_id),
FOREIGN KEY(player_id) REFERENCES player (player_id)
);

To verify that all five tables were created, enter .tables,
resulting in the following:
sqlite> .tables
league performance player team team_player
sqlite

4. Turn on foreign key enforcement with the following
statement:
sqlite> PRAGMA foreign_keys = ON;

5. Prepare the import statement to recognize CSV format with
the following command:
sqlite> .mode csv

6. Run the following commands from the sqlite prompt to
load the data. Run them in the order shown here:
sqlite> PRAGMA foreign_keys = ON;
sqlite> .mode csv
sqlite> .import --skip 1 data/player_data.csv player
sqlite> .import --skip 1 data/performance_data.csv performance
sqlite> .import --skip 1 data/league_data.csv league
sqlite> .import --skip 1 data/team_data.csv team
sqlite> .import --skip 1 data/team_player_data.csv team_player

###########################################################
 (Clean and Correct) THE DATA
###########################################################

Here’s the exact fix, used in real AutocratTech data pipelines when a wrong import corrupts a table.

Step 1 — Drop the corrupted table:

sqlite> DROP TABLE IF EXISTS team_player;

Step 2 — Recreate the table cleanly
CREATE TABLE team_player (
   team_id INTEGER NOT NULL,
   player_id INTEGER NOT NULL,
   last_changed_date DATE NOT NULL,
   PRIMARY KEY (team_id, player_id),
   FOREIGN KEY(team_id) REFERENCES team (team_id),
   FOREIGN KEY(player_id) REFERENCES player (player_id)
);

Step 3 — Verify the correct CSV structure BEFORE importing

###########################################################
