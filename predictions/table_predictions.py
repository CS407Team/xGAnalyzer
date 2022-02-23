import json

from user import user_utils
from data_files import database


def add_prediction(tournament_id, team_position, team_points, goals_for, goals_against, team_id,
                   season_year, userid,
                   visibility, prediction_name):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()

    # Check for duplicate names
    db_cursor.execute(f'select * from table_predictions where userid={userid} and name="{prediction_name}"')
    db_cursor.fetchall()
    if db_cursor.rowcount > 0:
        return False
    db_cursor.execute(
        f'INSERT INTO table_predictions (tournament_id, team_position, team_points, goals_for, goals_against, '
        f'team_id, season_year, visibility, userid, name) '
        f'values ({tournament_id}, {team_position}, {team_points}, {goals_for}, {goals_against}, {team_id}, {season_year}, "{visibility}", {userid}, "{prediction_name}");')
    db_connection.commit()
    return True


def find_public_predictions(userid):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where userid={userid}'
                      f' AND visibility=1')
    return db_cursor.fetchall()


def find_all_public_predictions():
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where visibility="true"')
    return db_cursor.fetchall()


def find_predictions_by_column(column_name, value):
    # Need to implement type checking for value
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where {column_name}={value}'
                      f' AND visibility="true"')
    return db_cursor.fetchall()


def find_prediction_by_username_and_name(username, prediction_name):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    user = user_utils.find_by_username(username)
    db_cursor.execute(f'select teams.team_name, tournaments.name, tp.team_position, tp.team_points, tp.goals_for, '
                      f'tp.goals_against from table_predictions tp join teams on teams.team_id = tp.team_id join '
                      f'tournaments on tp.tournament_id = tournaments.tournament_id '
                      f'join users on users.username = "{username}"'
                      f'where tp.name = "{prediction_name}"'
                      f'AND visibility=1')
    prediction = db_cursor.fetchone()
    return prediction


def export(username, prediction_name):
    prediction = find_prediction_by_username_and_name(username, prediction_name)
    if prediction is None:
        return None

    # lol
    predictionary = {
        "Team Name": prediction[0],
        "Tournament Name": prediction[1],
        "Team Position: ": prediction[2],
        "Team Points": prediction[3],
        "Team Goals For": prediction[4],
        "Team Goals Against": prediction[5]
    }
    print(type(predictionary))
    filepath = f'exports/table/{username}_{prediction_name}.json'
    with open(filepath, 'w') as outfile:
        json.dump(predictionary, outfile, indent=2)
    return filepath
