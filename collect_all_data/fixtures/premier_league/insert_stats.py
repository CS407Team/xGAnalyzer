import test_stats
import pandas
import mysql.connector as mysql
import json
import os


def max_key(scores):
    if(scores['home'] > scores['away'] and scores['home'] > scores['tie']):
        return "H"
    elif(scores['away'] > scores['home'] and scores['away'] > scores['tie']):
        return 'A'
    elif(scores['tie'] > scores['away'] and scores['tie'] > scores['home']):
        return 'T'
    else:
        return 'T'

def get_team(stats, team_name):
	for team in stats:
		if(team["team"] == team_name):
			return team

	return None

def read_stats():
	all_stats = []
	file = open("stats","r")
	lines = file.readlines()
	for line in lines:
		data = json.loads(line.strip())
		all_stats.append(data)

	return all_stats



def get_stats(round):

	val = test_stats.generate_stats(round)

	all_stats = read_stats()

	id_numbers = 100

	fixtures = open("fixture_results", "r")
	fixture_lines = fixtures.readlines()
	for current_team in fixture_lines:
		data = json.loads(current_team.strip())
		for result in data["results"]:
			odds = result['odds']

			home_stats = get_team(all_stats,result["teams"]["home"])
			away_stats = get_team(all_stats,result["teams"]["away"])

			home_id = int(home_stats['id'])
			away_id = int(away_stats['id'])

			home_possession = int(home_stats["possession"])
			home_total_shots = home_stats["total_shots"]
			home_on_target = home_stats["on_target"] 
			home_red_cards = home_stats["red_cards"]
			home_yellow_cards = home_stats["yellow_cards"]
			home_penalties = home_stats["penalties"]
			home_free_kicks = home_stats["freekicks"]
			home_total_passes = home_stats["total_passes"]
			home_complete_passes = home_stats["complete_passes"]

			away_possession = int(away_stats["possession"])
			away_total_shots = away_stats["total_shots"]
			away_on_target = away_stats["on_target"]
			away_red_cards = away_stats["red_cards"]
			away_yellow_cards = away_stats["yellow_cards"]
			away_penalties = away_stats["penalties"]
			away_free_kicks = away_stats["freekicks"]
			away_total_passes = away_stats["total_passes"]
			away_complete_passes = away_stats["complete_passes"]

			try:
				db_connection = mysql.connect(user = 'eliel', password='pass', host='localhost', database = 'analyzer')
				cursor = db_connection.cursor()
				#statsid, homeid, awayid , possession, shots, on target, yellow, red, freekicks, total_pass, complete_pass, penalties, 
				insert_stmt = ("INSERT INTO stats (stats_id,home_team_id,away_team_id,home_possession,away_possession,home_shots,away_shots,home_shots_on_target, away_shots_on_target,home_yellow_cards,away_yellow_cards,home_red_cards,away_red_cards,home_freekicks, away_freekicks, home_pass_total, away_pass_total, home_complete_passes, away_complete_passes, home_pens, away_pens)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
				data = (id,home_id, away_id, home_possession,away_possession,home_total_shots,away_total_shots,home_on_target,away_on_target,home_yellow_cards,away_yellow_cards, home_red_cards,away_red_cards,home_free_kicks,away_free_kicks,home_total_passes,away_total_passes,home_complete_passes,away_complete_passes,home_penalties,away_penalties)
				cursor.execute(insert_stmt, data)
				cursor.commit()

			except mysql.Error as err:
				print("Something went wrong: {}".format(err))
			else:
				db_connection.commit()
				print("Done");
				db_connection.close()

get_stats(29)

