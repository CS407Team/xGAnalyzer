import json
import mysql.connector as mariadb
from mysql.connector import errorcode

# +------------+----------+------+-----+---------+----------------+
# | Field      | Type     | Null | Key | Default | Extra          |
# +------------+----------+------+-----+---------+----------------+
# | playerid   | int(11)  | NO   | PRI | NULL    | auto_increment |
# | teamid     | int(11)  | YES  |     | NULL    |                |
# | playername | char(50) | NO   |     | NULL    |                |
# | position   | char(20) | YES  |     | NULL    |                |
# | player_age | int(11)  | YES  |     | NULL    |                |
# +------------+----------+------+-----+---------+----------------+

file = open("player_data","r")
lines = file.readlines()

teams = {
"Manchester City":"1",
"Liverpool":"2",
"Chelsea":"3",
"West Ham":"4",
"Manchester United":"5",
"Arsenal":"6",
"Wolves":"7",
"Tottenham":"8",
"Brighton":"9",
"Southampton":"10",
"Leicester":"11",
"Aston Villa":"12",
"Crystal Palace":"13",
"Brentford":"14",
"Leeds":"15",
"Everton":"16",
"Newcastle":"17",
"Norwich":"18",
"Watford":"19",
"Burnley":"20"
}

count = 0
index = 0
for line in lines:
    count+= 1
    index+= 1
    data = json.loads(line.strip())
    # for team in teams:
    curr = data["team"][0]["name"]
    for player in data["players"]:
        team_id = teams[curr]
        player_id = player["id"]
        player_name = player["name"]
        player_position = player["position"]
        player_age = player["age"]
        try:
            db_connection = mariadb.connect(user = 'newuser', password='test', host='localhost', database = 'analyzer', port='3306')
            db_cursor = db_connection.cursor()
            insert_stmt = ("INSERT INTO player(playerid, teamid, playername, position, player_age)" "VALUES (%s, %s, %s, %s, %s)")
            data = (player_id, team_id, player_name, player_position, player_age)
            db_cursor.execute(insert_stmt, data)

        except mariadb.Error as err:
            print("Something went wrong: {}".format(err))
        else:
            db_connection.commit()
            print("Done");
            db_connection.close()
    

