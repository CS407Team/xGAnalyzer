import json

import mysql.connector as mariadb
from mysql.connector import errorcode

try:
    db_connection = mariadb.connect(user='root', password='V3z?RnzC', host='35.225.215.107', database='analyzer')
except mariadb.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

team_files = [
    "Manchester City",
    "FC Liverpool",
    "FC Chelsea",
    "West Ham Utd.",
    "Manchester Utd.",
    "FC Arsenal",
    "Wolverhampton",
    "Tottenham",
    "Brighton & Hove",
    "FC Southampton",
    "Leicester City",
    "Aston Villa",
    "Crystal Palace",
    "FC Brentford",
    "Leeds United",
    "FC Everton",
    "Newcastle Utd.",
    "Norwich City",
    "FC Watford",
    "FC Burnley"
]

db_cursor = db_connection.cursor()
db_cursor.execute("select * from teams")
teams = db_cursor.fetchall()
for i in range(20):
    team_id = teams[i][0]
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"select * from player where teamid = {team_id}")
    players = db_cursor.fetchall()

    team_file = open(f"{team_files[i]}_squad", "r")
    team_data = json.load(team_file)
    print(team_data)


    for player in players:
        #print(player)
        playername = player[2]
        playerid = player[0]
        if '.' in playername:
            print(playername)
            temp = playername.split()
            lName = temp[len(temp) - 1]
            print(lName)
            updated_name = ""

            for player_data in team_data['squad']:
                if lName in player_data['name']:
                    #print(player_data['name'])
                    updated_name = player_data['name']
                    db_cursor.execute(f"update player set updated_name = \"{updated_name}\" where playerid = {playerid}")
                    db_connection.commit()

            print(f"updated name: {updated_name}")
    team_file.close()