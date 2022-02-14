import json
import mysql.connector as mariadb
from mysql.connector import errorcode

# | season_table_id | int(11) | NO   | PRI | NULL    |       |
# | team_id         | int(11) | YES  |     | NULL    |       |
# | tournament_id   | int(11) | YES  |     | NULL    |       |
# | team_position   | int(11) | YES  |     | NULL    |       |
# | team_points     | int(11) | YES  |     | NULL    |       |
# | goals_for       | int(11) | YES  |     | NULL    |       |
# | goals_against   | int(11) | YES  |     | NULL    |       |
# | season_year     | int(11) | YES  |     | NULL    |       |
# | games_played    | int(11) | YES  |     | NULL    |       |
# | won             | int(11) | YES  |     | NULL    |       |
# | lost            | int(11) | YES  |     | NULL    |       |
# +-----------------+---------+------+-----+---------+-------+

with open("team_standings") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

index = 0
print(jsonObject[0]['all']["goals"]["for"])
for object in jsonObject:
    index+=1
    team_id = index
    tournament = 1
    team_position = index+1
    team_points = object["points"]
    goals_for = object['all']["goals"]["for"]
    goals_against = object['all']["goals"]["against"]
    played = object['all']['played']
    won = object['all']['win']
    lost = played - won
    season = 2022
    try:
        db_connection = mariadb.connect(user = 'newuser', password='test', host='localhost', database = 'analyzer', port='3306')
        db_cursor = db_connection.cursor()
        insert_stmt = ("INSERT INTO season_table(season_table_id, team_id, tournament_id, team_position, team_points, goals_for, goals_against, season_year, games_played, won, lost)" "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (index, team_id, tournament, team_position, team_points,goals_for, goals_against, season, played, won, lost)
        db_cursor.execute(insert_stmt, data)

    except mariadb.Error as err:
        print("Something went wrong: {}".format(err))
    else:
        db_connection.commit()
        print("Done");
        db_connection.close()
    