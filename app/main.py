import mysql.connector as mariadb
from flask import Flask
from flask import render_template
from mysql.connector import errorcode

from predictions import table_predictions, booking_predictions

try:
    db_connection = mariadb.connect(user='root', password='V3z?RnzC', host='localhost', database='analyzer')
    db_cursor = db_connection.cursor()
    print("Successful connection")
except mariadb.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


# User Profile Page
@app.route('/profile/<username>')
def user(username):
    # Maybe optimize user checking with extra time
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()
    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        return f'{username}'


@app.route('/profile/<username>/table_predictions')
def user_table_predictions(username):
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()

    # Implement check for authentication to pass through to table_predictions.html later
    # For adding table add/edit/delete functionality.

    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        # Need to implement error checks
        db_cursor.execute(f'select * from table_predictions')

        # Pass more information if needed

        return render_template('table_predictions.html', username=username)


@app.route('/profile/<username>/booking_predictions')
def user_booking_predictions(username):
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()

    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        db_cursor.execute(f'select * from booking_predictions')
        return render_template('booking_predictions.html', username=username)


@app.route('/profile/<username>/match_predictions')
def user_match_predictions(username):
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()

    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        db_cursor.execute(f'select * from match_predictions')

        return render_template('match_predictions.html', username=username)


if __name__ == '__main__':
    app.run()
