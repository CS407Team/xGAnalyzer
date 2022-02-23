import json
import mysql.connector as mariadb
from mysql.connector import errorcode

# +-----------------+----------+------+-----+---------+----------------+
# | Field           | Type     | Null | Key | Default | Extra          |
# +-----------------+----------+------+-----+---------+----------------+
# | gameid          | int      | NO   | PRI | NULL    | auto_increment |
# | tournament_id   | int      | YES  |     | NULL    |                |
# | hometeam_id     | int      | YES  |     | NULL    |                |
# | awayteam_id     | int      | YES  |     | NULL    |                |
# | stats_id        | int      | YES  |     | NULL    |                |
# | winner_id       | int      | YES  |     | NULL    |                |
# | location_id     | int      | YES  |     | NULL    |                |
# | prediction_name | char(20) | YES  |     | NULL    |                |
# | location        | char(20) | YES  |     | NULL    |                |
# | status          | char(20) | YES  |     | NULL    |                |
# | round_number    | int      | YES  |     | NULL    |                |
# +-----------------+----------+------+-----+---------+----------------+

with open("match_data") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

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

url = "https://api-football-v1.p.rapidapi.com/v3/teams"


for index in jsonObject:
    home = str(index['HomeTeam'])
    if(home == "Man Utd"):
        home = "Manchester United"
    elif (home == "Man City"):
        home = "Manchester City"
    elif (home == "Spurs"):
        home = "Tottenham"
    
    away = str(index['AwayTeam'])
    if(away == "Man Utd"):
            away = "Manchester United"
    elif (away == "Man City"):
        away = "Manchester City"
    elif (away == "Spurs"):
        away = "Tottenham"

    id = index["MatchNumber"]
    tourny = "39"
    home_team_id = teams[home]
    away_team_id = teams[away]
    location = str(index['Location'])
    home_score = (index['HomeTeamScore'])
    away_score = (index['AwayTeamScore'])
    winner = "0"
    status = "not_played"
    if(home_score != None):
        if(home_score > away_score):
            winner = home_team_id       
        elif away_score > home_score:
            winner = away_team_id
        status = "played"
    else:
        home_score = -1
        away_score = -1 
    
    round_number = (index['RoundNumber'])
    match_number = (index['MatchNumber'])
    print(home, " ", away, " ", location, " ", home_score ," ", away_score ," ", round_number)
    
    try:
            db_connection = mariadb.connect(user = 'root', password='V3z?RnzC', host='localhost', database = 'analyzer', port='3306')
            db_cursor = db_connection.cursor()
            insert_stmt = ("INSERT INTO games(gameid, tournament_id, hometeam_id, awayteam_id, stats_id, winner_id,location, status, round_number)" "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)")
            data = (match_number,tourny, home_team_id,away_team_id,id,winner, location, status,round_number)
            db_cursor.execute(insert_stmt, data)

        except mariadb.Error as err:
            print("Something went wrong: {}".format(err))
        else:
            db_connection.commit()
            print("Done");
            db_connection.close()