import json

from predictions import stats_predictions
from user import user_utils
from data_files import database

def add_prediction(db_connection):
    db_cursor = db_connection.cursor()



def get_followers(username):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select t.follower '
                      f'from Followers t'
                      f' where t.username = {username}')
    predictions = db_cursor.fetchall()
    return predictions


def follow(username, follower):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'insert into Followers ' 
                      f'values({username}, {follower})')
    predictions = db_cursor.fetchall()
    return predictions


def follower_exist(follower):
    # Need to implement type checking for value
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from Users'
                      f' where username ={follower}')
    predictions = db_cursor.fetchall()

    if predictions is not None:
        return True
    else :
        return False



