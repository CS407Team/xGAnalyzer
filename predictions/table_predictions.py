def add_prediction(db_connection, tournament_id, team_position, team_points, goals_for, goals_against, team_id,
                         season_year, userid,
                         visibility):
    db_cursor = db_connection.cursor()
    db_cursor.execute('select max(table_prediction_id) as maximum from table_predictions')
    fetch_result = db_cursor.fetchone()[0]
    if fetch_result is None:
        prediction_id = 0
    else:
        prediction_id = fetch_result + 1
    db_cursor.execute(
        f'INSERT INTO table_predictions values ({prediction_id}, {tournament_id}, {team_position}, {team_points}, {goals_for}, {goals_against}, {team_id}, {season_year}, {visibility}, "{userid}");')
    db_connection.commit()


def find_public_predictions(db_connection, userid):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where userid={userid}'
                      f' AND visibility="true"')
    return db_cursor


def find_all_public_predictions(db_connection):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where visibility="true"')
    return db_cursor


def find_prediction_by_column(db_connection, column_name, value):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from table_predictions'
                      f' where {column_name}={value}'
                      f' AND visibility="true"')
    return db_cursor
