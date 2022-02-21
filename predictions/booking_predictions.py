def add_prediction(db_connection):
    db_cursor = db_connection.cursor()
    # Implement adding booking predictions


def find_public_predictions(db_connection, userid):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from booking_predictions'
                      f' where userid={userid}'
                      f' AND visibility="true"')
    return db_cursor


def find_all_public_predictions(db_connection):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from booking_predictions'
                      f' where visibility="true"')
    return db_cursor


def find_prediction_by_column(db_connection, column_name, value):
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from booking_predictions'
                      f' where {column_name}={value}'
                      f' AND visibility="true"')
    return db_cursor
