import json
import mysql.connector as mariadb
from mysql.connector import errorcode

#   `team_id` int(11) NOT NULL AUTO_INCREMENT,
#   `tournament_id` int(11) DEFAULT NULL,
#   `team_name` char(50) DEFAULT NULL,
#   `home_stadium` char(50) DEFAULT NULL,

file = open("team_data","r")
lines = file.readlines()

count = 0
index = 0
for line in lines:
    count+= 1
    index+= 1
    data = json.loads(line.strip())
    team_name = data["team"]["name"]
    print(team_name)
    team_home = data["venue"]["name"]
    tournament = 1
    team_id = index
    # try:
    #     db_connection = mariadb.connect(user = 'newuser', password='test', host='localhost', database = 'analyzer', port='3306')
    #     db_cursor = db_connection.cursor()
    #     insert_stmt = ("INSERT INTO teams(team_id, tournament_id, team_name, home_stadium)" "VALUES (%s, %s, %s, %s)")
    #     data = (team_id, tournament, team_name, team_home)
    #     db_cursor.execute(insert_stmt, data)
   
    # except mariadb.Error as err:
    #         print("Something went wrong: {}".format(err))
    # else:
    #     db_connection.commit()
    #     print("Done");
    #     db_connection.close()

    
    