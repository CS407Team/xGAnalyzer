import json

from user import user_utils
from data_files import database


def find_public_predictions(userid):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select player.playername, pred.yellow_cards, pred.red_cards from '
                      f'player_performance_prediction pred '
                      f' join player on player_playerid = pred.playerid'
                      f' where userid={userid}'
                      f' AND visibility=1')
    return db_cursor.fetchall()


def find_public_predictions_by_username(username):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    user = user_utils.find_by_username(username)
    userid = user[0]

    db_cursor.execute(
        f'select pred.gameid, player.playername, pred.yellow_cards, pred.red_cards from player_performance_prediction pred'
        f' join player on player.playerid = pred.playerid'
        f' where visibility=1 AND pred.userid = {userid}')
    predictions = db_cursor.fetchall()
    return predictions


def export(username):
    predictions = find_public_predictions_by_username(username)
    if len(predictions) == 0:
        return None
    predictionary = []
    for prediction in predictions:
        entry = {
            "Player": prediction[1],
            "Game: ": prediction[0],
            "Yellow Cards": prediction[2],
            "Red Cards": prediction[3]
        }
        predictionary.append(entry)

    filepath = f'exports/booking/{username}_bookings.json'
    with open(filepath, 'w') as outfile:
        json.dump(predictionary, outfile, indent=2)
    return filepath
