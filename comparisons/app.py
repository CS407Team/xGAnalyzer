from ast import AsyncFunctionDef
from lib2to3.pytree import convert
from flask import Flask, render_template, request, json, redirect
import random

from flaskext.mysql import MySQL
from scipy import rand

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'eliel'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'analyzer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def get_unplayed():
    cursor.execute("select gameid, hometeam_id, awayteam_id from games where status = 0")
    return cursor.fetchall()

def get_team_name(id):
    cursor.execute("select team_name from teams where team_id = %s", (id))
    return cursor.fetchall()[0][0]

def get_players(set, id, to_return):
    cursor.execute("select playerid, playername, position from team where teamid = %s",(id))
    player_list = cursor.fetchall()
    for current in set:
        for player in player_list:
            if current == int(player[0]):
                to_return.append(player[1],player[2])


@app.route("/")
def main():
	return render_template('index.html')


@app.route("/teams", methods=['GET','POST'])
def teams():
    if request.method == 'POST':
        teamDetails = request.form
        teamid = teamDetails['team']
        cursor.execute("select * from player where teamid = %s", (teamid))
        players = cursor.fetchall()
        return team_squad(players)
        # return render_template('/team_squad.html', players=players)
    return render_template('teams.html')

@app.route("/team_squad", methods=['GET','POST'])
def team_squad(players):
    return render_template("/team_squad.html", players=players)

@app.route("/make_prediction", methods=['POST','GET'])
def make_predition():
	gameid="307"
	if request.method=='POST':
		try:
			print("Hello")
			prediction_data=request.form
			prediction_id = random.randint(4000,100000)
			playerid=prediction_data["playerid"]
			num_tackles = prediction_data["total_tackles"]
			success_tackles = prediction_data["success_tackles"]
			yellow = prediction_data["yellow"]
			red = prediction_data["red"]
			goals = prediction_data["goals"]
			total_shots = prediction_data["total_shots"]
			on_target = prediction_data["on_target"]
			passes = prediction_data["total_passes"]
			complete_pass = prediction_data["complete_passes"]
			saves = prediction_data["saves"]
			conceded = prediction_data["conceded"]
			crosses = prediction_data["total_crosses"]
			complete_cross = prediction_data["complete_crosses"]
			assists = prediction_data["assists"]
			rating = prediction_data["rating"]
			visibility = prediction_data["visibility"]
			cursor.execute("insert into player_performance_prediction(performance_id,playerid,gameid,num_tackles,num_successful_tackles,yellow_cards,red_cards,goals,total_shots,shots_on_target,total_passes,complete_passes,total_saves,goals_conceded,total_crosses,complete_crosses,assists,visibility,player_rating) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(prediction_id,playerid,gameid,num_tackles,success_tackles,yellow,red,goals,total_shots,on_target,passes,complete_pass,saves,conceded,crosses,complete_cross,assists,rating,visibility))
		except conn.Error as err:
			print("Something went wrong: {}".format(err))
		else:
			conn.commit()
			print("Done")  
			return render_template("/index.html")
	return render_template("/make_prediction.html")      


@app.route("/lineups")
def lineups():
    return render_template("/lineups.html")

@app.route("/select_game", methods = ['GET','POST'])
def select_game():
	cursor.execute("select gameid, hometeam_id, awayteam_id from games where status = 0")
	matches = []
	hometeam = ""
	awayteam = ""
	games = cursor.fetchall()
	for game in games:
		id = game[0]
		home = game[1]
		away = game[2]
		cursor.execute("select team_name from teams where team_id = %s", (home))
		home_name = cursor.fetchall()[0][0]
		hometeam = home_name
		cursor.execute("select team_name from teams where team_id = %s", (away))
		away_name = cursor.fetchall()[0][0]
		awayteam = away_name
		current_fixture = (id, home_name, away_name)
		matches.append(current_fixture)
	if request.method == 'POST':
		details = request.form
		matchid = details["match_id"]
		cursor.execute("select hometeam_id, awayteam_id from games where gameid = %s", (matchid))
		teams = cursor.fetchall()
		home_id = teams[0][0]
		away_id = teams[0][1]
		cursor.execute("select playerid, playername, position from player where teamid = %s", (home_id))
		home_players = cursor.fetchall()
		cursor.execute("select playerid, playername, position from player where teamid = %s", (away_id))
		away_players = cursor.fetchall()
		return render_template("/predict_lineup.html", home_players=home_players, away_players=away_players, home = hometeam, away = awayteam, id=matchid)
		
	matches_tuple = tuple(i for i in matches)
	return render_template("/select_game.html",game_set=matches_tuple)

@app.route("/compare_lineup", methods = ['GET','POST'])
def compare_lineup():    
	cursor.execute("select gameid, hometeam_id, awayteam_id from games where status = 0")
	matches = []
	hometeam = ""
	awayteam = ""
	games = cursor.fetchall()
	for game in games:
		id = game[0]
		home = game[1]
		away = game[2]
		cursor.execute("select team_name from teams where team_id = %s", (home))
		home_name = cursor.fetchall()[0][0]
		hometeam = home_name
		cursor.execute("select team_name from teams where team_id = %s", (away))
		away_name = cursor.fetchall()[0][0]
		awayteam = away_name
		current_fixture = (id, home_name, away_name)
		matches.append(current_fixture)
	if request.method == 'POST':
		details = request.form
		matchid = details["match_id"]
		cursor.execute("select * from lineups where game_id = %s", (matchid))
		data = cursor.fetchall()
		print(data[0])
		return		
	matches_tuple = tuple(i for i in matches)
	return render_template("/compare_lineup.html",game_set=matches_tuple)

@app.route("/predict_lineup")
def predict_lineup():
    return render_template("/predict_lineup.html")



if __name__ == "__main__":
	app.run()

