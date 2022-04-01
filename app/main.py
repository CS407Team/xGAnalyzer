from flask import Flask, send_file, Blueprint, session
from flask import render_template, request, redirect
from flask_login import LoginManager, current_user, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import GamePredictions, SeasonTable, Teams, Games, Stats, TablePredictions
from user import user_utils
from data_files import database

from predictions import table_predictions, booking_predictions, match_predictions, stats_predictions, \
    app_generated_predictions

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('userpage.html', user=current_user.username)
    else:
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
        result = table_predictions.add_prediction(tournament_id, position, points, goals_for, goals_against, team_id,
                                                  season_year, current_user.userid, visibility, prediction_name)
        if result is False:
            return f"Failed to add {prediction_name} to database"
        return f"Successfully added {prediction_name} to database"
    else:
        return render_template('add_table_pred.html')


@main.route('/search_matches', methods=["POST", "GET"])
def search_matches():
    if request.method == "GET":
        return render_template('search_matches.html')
    else:
        data = request.form
        for item in data:
            print(data[item])
        home_team = Teams.query.filter_by(team_id=data['home_team']).first()
        away_team = Teams.query.filter_by(team_id=data['away_team']).first()
        home_team_name = home_team.team_name.replace(' ', '-')
        away_team_name = away_team.team_name.replace(' ', '-')
        return redirect(f'/match/{home_team_name}-v-{away_team_name}-{data["round_number"]}')
        # return 'post'


@main.route('/match/<home_team>-v-<away_team>-<round_number>')
def match_page(home_team, away_team, round_number):
    home_team_name = home_team.replace('-', ' ')
    away_team_name = away_team.replace('-', ' ')

    home_team = Teams.query.filter(Teams.team_name.ilike(home_team_name)).first()
    away_team = Teams.query.filter(Teams.team_name.ilike(away_team_name)).first()

    if home_team is None:
        return render_template('match_does_not_exist.html')
    if away_team is None:
        return render_template('match_does_not_exist.html')

    game = Games.query.filter_by(hometeam_id=home_team.team_id, awayteam_id=away_team.team_id,
                                 round_number=round_number).first()
    if game is None:
        return render_template('match_does_not_exist.html')
    print(game.gameid)

    stats = Stats.query.filter_by(gameid=game.gameid)
    # return f'{home_team} vs {away_team} on {round_number}'

    if current_user.is_authenticated:
        if request.url not in session['urls']:
            session['urls'].append(request.url)
            if (len(session['urls'])) > 10:
                session['urls'].pop(0)
            session.modified = True
    if home_team.team_id == game.winner_id:
        winner = home_team_name
    elif away_team.team_id == game.winner_id:
        winner = away_team_name
    else:
        winner = "Neither"

    if current_user.is_authenticated:
        predictions = GamePredictions.query.filter_by(userid=current_user.userid, home_team_id=home_team.team_id, away_team_id=away_team.team_id, round_number=round_number).all()

    return render_template('matchpage.html', home_team_name=home_team_name, away_team_name=away_team_name, game=game,
                           stats=stats, winner=winner, predictions=predictions, current_user=current_user)


@main.route('/table')
def application_table():
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    team_names = []
    for team in data:
        team_query = Teams.query.filter_by(team_id=team.team_id).first()
        team_names.append(team_query.team_name)
    if current_user.is_authenticated:
        predictions = table_predictions.find_all_predictions_by_userid(current_user.userid)
    return render_template('application_table_pred.html', team_data=data, current_user=current_user,
                           team_names=team_names, predictions=predictions, test=None)


@main.route('/table/compare-<prediction_name>')
def application_table_compare(prediction_name):
    prediction_name = prediction_name.replace('-', ' ')
    pred = TablePredictions.query.filter_by(userid=current_user.userid, name=prediction_name).first()
    if pred is None:
        return redirect('/table')
    prediction_team = Teams.query.filter_by(team_id=pred.team_id).first()
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    team_names = []
    test = {}
    for team in data:
        team_query = Teams.query.filter_by(team_id=team.team_id).first()
        team_names.append(team_query.team_name)
        if team.team_id == pred.team_id:
            print(team_query.team_name)
            test[f'{team_query.team_name}'] = team.team_position

    if current_user.is_authenticated:
        predictions = table_predictions.find_all_predictions_by_userid(current_user.userid)

    return render_template('application_table_pred.html', team_data=data, current_user=current_user,
                           team_names=team_names, predictions=predictions, prediction=pred,
                           prediction_team=prediction_team, test=test)


@main.route('/table/download')
def download_app_table():
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    path = app_generated_predictions.export()
    if path is None:
        return
    return send_file(path, as_attachment=True)


@main.route('/table/compare-<prediction_name>/download')
def download_app_table_compare(prediction_name):
    prediction_name = prediction_name.replace('-', ' ')
    pred = TablePredictions.query.filter_by(userid=current_user.userid, name=prediction_name).first()
    if pred is None:
        return redirect('/table')
    path = app_generated_predictions.export_with_compare(prediction_name)
    return send_file(path, as_attachment=True)
