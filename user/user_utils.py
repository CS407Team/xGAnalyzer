from data_files import database


def find_by_email(email):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where email_address="{email}"')
    user = db_cursor.fetchone()
    return user


def find_by_id(userid):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where userid={userid}')
    user = db_cursor.fetchone()
    return user


def find_by_username(username):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where username="{username}"')
    user = db_cursor.fetchone()
    return user

