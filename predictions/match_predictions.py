import json

from predictions import stats_predictions
from user import user_utils
from data_files import database

def add_prediction(db_connection):
    db_cursor = db_connection.cursor()
    #Implement adding match predictions


def find_public_predictions(userid):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    print(userid)
    db_cursor.execute(f'select tournaments.name, home_team.team_name, away_team.team_name, pred.name, '
                      f'pred.stats_predictions_id from game_predictions pred join games on games.gameid = pred.gameid '
                      f'join tournaments on tournaments.tournament_id = games.tournament_id join teams home_team on '
                      f'home_team.team_id = pred.home_team_id join teams away_team on away_team.team_id = '
                      f'pred.away_team_id where pred.userid = {userid} '
                      f'and pred.visibility = 1')
    predictions = db_cursor.fetchall()
    print(predictions)
    return predictions


def find_all_public_predictions():
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from game_predictions'
                      f' where (visibility="true" or visibility=1 or visibility="public")')
    predictions = db_cursor.fetchall()
    return predictions


def find_all_predictions_by_userid(userid):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    print(userid)
    db_cursor.execute(f'select tournaments.name, home_team.team_name, away_team.team_name, pred.name, '
                      f'pred.stats_predictions_id from game_predictions pred join games on games.gameid = pred.gameid '
                      f'join tournaments on tournaments.tournament_id = games.tournament_id join teams home_team on '
                      f'home_team.team_id = pred.home_team_id join teams away_team on away_team.team_id = '
                      f'pred.away_team_id where pred.userid = {userid}')
    predictions = db_cursor.fetchall()
    return predictions


def find_prediction_by_column(column_name, value):
    # Need to implement type checking for value
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from game_predictions'
                      f' where {column_name}={value}'
                      f' AND visibility="true"')
    predictions = db_cursor.fetchall()
    return predictions


def find_prediction_by_username_and_name(username, prediction_name):
    user = user_utils.find_by_username(username)
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select tournaments.name, home_team.team_name, away_team.team_name, pred.name, '
                      f'pred.stats_predictions_id from game_predictions pred join games on games.gameid = pred.gameid '
                      f'join tournaments on tournaments.tournament_id = games.tournament_id join teams home_team on '
                      f'home_team.team_id = pred.home_team_id join teams away_team on away_team.team_id = '
                      f'pred.away_team_id where pred.userid = {user[0]} '
                      f'and (visibility = 1 or visibility="public") '
                      f'and pred.name="{prediction_name}"')
    prediction = db_cursor.fetchone()
    return prediction


def export(username, prediction_name):
    prediction = find_prediction_by_username_and_name(username, prediction_name)
    if prediction is None:
        return None
    stats = stats_predictions.find_stats(prediction[4])
    home_stats = [f'{prediction[0]} (Home)']
    for item in stats[5:29:2]:
        home_stats.append(item)
    away_stats = [f'{prediction[1]} (Away)']
    for item in stats[6:29:2]:
        away_stats.append(item)
    teams = [away_stats, home_stats]
    predictionary = []
    for team in teams:
        entry = {
            "Team": team[0],
            "Possessions": team[1],
            "Shots": team[2],
            "Shots on Target": team[3],
            "Yellow Cards": team[4],
            "Red Cards": team[5],
            "Subs": team[6],
            "Corners": team[7],
            "Goals": team[8],
            "Pens": team[9],
            "Free Kicks": team[10],
            "Total Passes": team[11],
            "Competed Passes": team[12]
        }
        predictionary.append(entry)
    filepath = f'exports\\match\\{username}_{prediction_name}.json'
    with open(f'app/exports/match/{username}_{prediction_name}.json', 'w') as outfile:
        json.dump(predictionary, outfile, indent=2)
    return filepath




