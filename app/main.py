from flask import Flask, send_file, Blueprint
from flask import render_template, request, redirect
from flask_login import LoginManager, current_user, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import GamePredictions, SeasonTable
from user import user_utils
from data_files import database

from predictions import table_predictions, booking_predictions, match_predictions, stats_predictions, \
    app_generated_predictions

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


# User Profile Page
@main.route('/profile/<username>')
def profile(username):
    # Maybe optimize user checking with extra time
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()
    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        return render_template('profile.html', username=username)


@main.route('/profile/<username>/table_predictions')
def user_table_predictions(username):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()

    # Implement check for authentication to pass through to table_predictions.html later
    # For adding table add/edit/delete functionality.

    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        # Need to implement error checks
        user = user_utils.find_by_username(username)
        predictions = table_predictions.find_public_predictions(user[0])
        print(user)
        print(predictions)

        return render_template('table_predictions.html', username=username, predictions=predictions)


@main.route('/profile/<username>/table_predictions/<prediction_name>')
def user_selected_table_prediction(username, prediction_name):
    db_connection = database.connect()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'select * from users where username="{username}"')
    db_cursor.fetchone()

    if db_cursor.rowcount == 0:
        return "User not found"
    else:
        prediction = table_predictions.find_prediction_by_username_and_name(username, prediction_name)
        if prediction is None:
            return "Prediction does not exist"
        return render_template('show_table_pred.html', username=username, prediction_name=prediction_name,
                               prediction=prediction)


@main.route('/profile/<username>/table_predictions/<prediction_name>/download')
def download_table(username, prediction_name):
    path = table_predictions.export(username, prediction_name)
    if path is None:
        return 'Prediction does not exist'
    return send_file(path, as_attachment=True)


@main.route('/profile/<username>/booking_predictions')
def user_booking_predictions(username):
    user = user_utils.find_by_username(username)
    if user is None:
        return 'User not found'
    predictions = booking_predictions.find_public_predictions_by_username(username)
    if predictions is None:
        return "Prediction does not exist"
    return render_template('booking_predictions.html', predictions=predictions, username=username)


@main.route('/profile/<username>/booking_predictions/download')
def download_bookings(username):
    path = booking_predictions.export(username)
    if path is None:
        return "Prediction does not exist"
    return send_file(path, as_attachment=True)


@main.route('/profile/<username>/match_predictions')
def user_match_predictions(username):
    user = user_utils.find_by_username(username)
    if user is None:
        return 'User not found'

    # Check to see if we are visiting the current user's page
    if current_user.username != username:
        print("Not the same user")
        predictions = match_predictions.find_public_predictions(user[0])
    else:
        # Return all prediction
        print("All predictions")
        predictions = match_predictions.find_all_predictions_by_userid(current_user.userid)
        print(predictions)
    return render_template('match_predictions.html', username=username, predictions=predictions)


@main.route('/profile/<username>/match_predictions/<prediction_name>')
def user_selected_match_prediction(username, prediction_name):
    user = user_utils.find_by_username(username)
    if user is None:
        return 'User not found'

    prediction = match_predictions.find_prediction_by_username_and_name(username, prediction_name)
    if prediction is None:
        return "Prediction does not exist"
    stats = stats_predictions.find_stats(prediction[4])

    return render_template('show_match_pred.html', prediction_name=prediction_name, stats=stats, prediction=prediction,
                           username=username)


@main.route('/profile/<username>/match_predictions/<prediction_name>/download')
def download_match_pred(username, prediction_name):
    path = match_predictions.export(username, prediction_name)
    if path is None:
        return "Prediction does not exist"
    return send_file(path, as_attachment=True)


@main.route('/add_table_prediction', methods=["POST", "GET"])
def add_table_prediction():
    if request.method == "POST":
        data = request.form
        for item in data:
            print(item)
            if data[item] == '':
                return f"Form failure"

        tournament_id = data['tournament']
        team_id = data['team']
        position = data['team_position']
        points = data['team_points']
        goals_for = data['goals_for']
        goals_against = data['goals_against']
        season_year = data['season_year']
        prediction_name = data['prediction_name']
        print(prediction_name)
        if data['access'] == "public":
            visibility = "1"
        else:
            visibility = "0"
        result = table_predictions.add_prediction(tournament_id, position, points, goals_for, goals_against, team_id, season_year, current_user.userid, visibility, prediction_name)
        if result is False:
            return f"Failed to add {prediction_name} to database"
        return f"Successfully added {prediction_name} to database"
    else:
        return render_template('add_table_pred.html')


@main.route('/match/<home_team>-v-<away_team>-<date>')
def match_page(home_team, away_team, date):
    #TODO: String formatting from team names and dates to proper database version.




    return f'{home_team} vs {away_team} on {date}'


@main.route('/table')
def application_table():
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    for team in data:
        print(f'ID: {team.team_id}')
        print(f'pos: {team.team_position}')
    return render_template('application_table_pred.html', team_data=data)


@main.route('/table/download')
def download_app_table():
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    path = app_generated_predictions.export()
    if path is None:
        return
    return send_file(path, as_attachment=True)


"""
def download_table(username, prediction_name):
    path = table_predictions.export(username, prediction_name)
    if path is None:
        return 'Prediction does not exist'
    return send_file(path, as_attachment=True)
"""