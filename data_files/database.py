def connect():
    import mysql.connector as mariadb
    from mysql.connector import errorcode

    try:
        db_connection = mariadb.connect(user='root', password='V3z?RnzC', host='localhost', database='analyzer')
        return db_connection
    except mariadb.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def get_teams():
    db_connection = connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute("select * from teams")
    return db_cursor


def get_players():
    db_connection = connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute("select * from players")
    return db_cursor

