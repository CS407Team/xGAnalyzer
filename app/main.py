import json

from flask import Flask, send_file, Blueprint, session
from flask import render_template, request, redirect
from flask_login import LoginManager, current_user, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from app import create_app
from app.models import GamePredictions, SeasonTable, Teams, Games, Stats, TablePredictions, User, \
    PlayerRatings, Player, Watchlist, StatsPredictions
from user import user_utils
from data_files import database

from predictions import table_predictions, booking_predictions, match_predictions, stats_predictions, \
    app_generated_predictions, player_rating

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
    orig_home = home_team
    orig_away = away_team
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
    else:
        predictions = None

    return render_template('matchpage.html', home_team_name=home_team_name, away_team_name=away_team_name, game=game,
                           stats=stats, winner=winner, predictions=predictions, current_user=current_user, orig_home=orig_home, orig_away=orig_away)


@main.route('/match/<home_team>-v-<away_team>-<round_number>/compare-<prediction_name>')
def compare_match(home_team, away_team, round_number, prediction_name):
    home_team_name = home_team.replace('-', ' ')
    away_team_name = away_team.replace('-', ' ')
    orig_home = home_team
    orig_away = away_team
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


    orig_pred_name = prediction_name
    prediction_name = prediction_name.replace('-', ' ')
    pred = GamePredictions.query.filter_by(userid=current_user.userid, name=prediction_name).first()
    if pred is None:
        return redirect(f'/match/{home_team}-v-{away_team}-{round_number}')

    print(pred.stats_predictions_id)
    userpred = StatsPredictions.query.filter_by(statsid=pred.stats_predictions_id).first()

    #stats = Stats.query.filter_by(home_team_id=home_team.team_id, away_team_id=away_team.team_id, round=round_number).first()
    stats = Stats.query.filter_by(statsid=game.stats_id).first()
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
        predictions = GamePredictions.query.filter_by(userid=current_user.userid, home_team_id=home_team.team_id,
                                                      away_team_id=away_team.team_id, round_number=round_number).all()
    else:
        predictions = None
    return render_template('matchpage.html', home_team_name=home_team_name, away_team_name=away_team_name, game=game,
                           stats=stats, winner=winner, predictions=predictions, current_user=current_user,
                           orig_home=orig_home, orig_away=orig_away, userpred=userpred)



@main.route('/match/<home_team>-v-<away_team>-<round_number>/download')
def download_match(home_team, away_team, round_number):
    orig_home = home_team
    orig_away = away_team
    home_team_name = home_team.replace('-', ' ')
    away_team_name = away_team.replace('-', ' ')
    home_team = Teams.query.filter(Teams.team_name.ilike(home_team_name)).first()
    away_team = Teams.query.filter(Teams.team_name.ilike(away_team_name)).first()

    game = Games.query.filter_by(hometeam_id=home_team.team_id, awayteam_id=away_team.team_id,
                                 round_number=round_number).first()

    if home_team.team_id == game.winner_id:
        winner = home_team_name
    elif away_team.team_id == game.winner_id:
        winner = away_team_name
    else:
        winner = "Neither"

    predictionary = {
        "Home Team": home_team_name,
        "Away Team": away_team_name,
        "Round Number": round_number,
        "Predicted Winner": winner
    }


    filepath = f'exports\\game\\{orig_home}-v-{orig_away}-{round_number}.json'
    with open(f'app/exports/game/{orig_home}-v-{orig_away}-{round_number}.json', "w") as outfile:
        json.dump(predictionary, outfile, indent=2)
    return send_file(filepath, as_attachment=True)


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
    orig_pred_name = prediction_name
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
    else:
        predictions = None

    return render_template('application_table_pred.html', team_data=data, current_user=current_user,
                           team_names=team_names, predictions=predictions, prediction=pred,
                           prediction_team=prediction_team, test=test, orig_pred_name=orig_pred_name)


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


@main.route('/player_prediction', methods=["POST", "GET"])
def player_prediction():
    if request.method == "GET":
        return render_template('search_player_rating.html')
    else:
        data = request.form
        # print(data)

        player = Player.query.filter_by(playername=data['player_name'], teamid=data['home_team']).first()
        team = Teams.query.filter_by(team_id=data['home_team']).first()

        # print(team.team_name)

        if player is not None:
            return render_template('player_rating_pred.html', playername=player.playername, team_name=team.team_name,
                                   playerid=player.playerid, team_id=team.team_id)
        else:
            return redirect('/player_prediction')


@main.route('/player_prediction/add-<playerid>-<team_id>', methods=["POST"])
def add_prediction_rating(playerid, team_id):
    if request.method == 'POST':
        data = request.form
        db.create_all()
        prediction = PlayerRatings(playerid=playerid, userid=current_user.userid, team_id=team_id,
                                   player_rating=data['player_rating'], visibility=data["visibility"],
                                   sharability=data["sharable"])
        db.session.add(prediction)
        db.session.commit()
        return redirect('/player_prediction')


@main.route('/my_player_predictions')
def user_rating_prediction():
    predictions = PlayerRatings.query.filter_by(userid=current_user.userid).all()
    return render_template("tester.html", predictions=predictions)


@main.route(('/edit_rating-<player_rating_id>'))
def edit_rating(player_rating_id):
    player = PlayerRatings.query.filter_by(player_rating_id=player_rating_id).first()
    player_name = Player.query.filter_by(playerid=player.playerid).first()
    return render_template("edit_prediction.html", playername=player_name.playername,
                           player_rating=player.player_rating, player_rating_id=player_rating_id)


@main.route('/edit_rating-<player_rating_id>/edit', methods=["POST"])
def edit(player_rating_id):
    data = request.form
    player_rating.edit(player_rating_id, data['player_rating'], data['visibility'], data['sharable'])
    return redirect('/my_player_predictions')


@main.route('/search_user_ratings')
def follower_rating_predictions():
    return render_template("search_user_predcitions.html")


@main.route('/find_user_ratings', methods=["POST"])
def find_user_ratings():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return render_template("user_does_not_exist.html")

    ratings = PlayerRatings.query.filter_by(userid=user.userid).all()
    visible = [rating for rating in ratings if rating.visibility == 1]
    return render_template("list_user_predictions.html", predictions=visible)


@main.route('/download_rating-<player_rating_id>')
def download_rating(player_rating_id):
    return render_template("download_predictions.html", player_rating_id=player_rating_id)


@main.route('/download-<player_rating_id>')
def download(player_rating_id):
    player_rating_prediction = PlayerRatings.query.filter_by(player_rating_id=player_rating_id).first()
    player_rating.download(player_rating_prediction)
    return redirect('/search_user_ratings')


@main.route('/watchlist', methods=["GET", "POST"])
def watchlist():
    if request.method == 'GET':
        playerlist = player_rating.get_player_list(current_user.userid)
        return render_template("list_watchlist.html", playerlist=playerlist)
    else:
        data = request.form
        success = player_rating.add_player_to_watchlist(current_user.userid, data['playername'])
        return redirect('/watchlist')


@main.route('/change_visibility', methods=["POST"])
def change_visibility():
    data = request.form
    player_rating.change_visibility(data['visibility'], current_user.userid)
    return redirect('/watchlist')


@main.route('/search_user_watchlist')
def follower_watchlist():
    return render_template("search_user_watchlist.html")


@main.route('/find_user_watchlist', methods=["POST"])
def find_user_watchlist():
    data = request.form
    visible = player_rating.find_user_watchlist(data['username'])

    if visible is None:
        return render_template("watchlist_not_found.html")
    return render_template("list_user_watchlist.html", playerlist=visible)


# New Routing to link old routing
@main.route('/table_predictions')
def table_prediction_link():
    if current_user.is_authenticated:
        return redirect(f'/profile/{current_user.username}/table_predictions')
    else:
        return redirect('/')


@main.route('/match_predictions')
def match_prediction_link():
    if current_user.is_authenticated:
        return redirect(f'/profile/{current_user.username}/table_predictions')
    else:
        return redirect('/')


@main.route('/search_players', methods=["GET", "POST"])
def search_players():
    if request.method == "GET":
        return render_template('search_players.html')
    else:
        data = request.form
        for item in data:
            print(item)
        form_name = data['player_name']
        print(form_name)

        return redirect(f'/player/{form_name}')
