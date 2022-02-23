import json

from user import user_utils
from data_files import database


def add_prediction():
    # Implementation Later
    return


def find_stats(stats_id):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from stats_predictions where statsid = {stats_id}')
    prediction = db_cursor.fetchone()
    return prediction
