from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from data_files import database
from .models import User, Player, Teams
from . import db

players = Blueprint('players', __name__)


@players.route('/players')
def match_history():
    playersList = Player.query.all()
    for person in playersList:
        print(person.playername)
    return 'Test'


@players.route('/player/<playername>')
def player_page(playername):
    # Kevin Long
    # Jack Butland
    playername = playername.replace('-', ' ')
    player = Player.query.filter_by(playername=playername).first()
    if player is None:
        return 'Player not found'
    ratings = {}

    db_connection = database.connect()
    db_cursor = db_connection.cursor()

    for i in range(2016, 2021):
        year = f'{i}'
        db_cursor.execute(f'select {year}rating from {year}ratings where playerid={player.playerid}')
        data = db_cursor.fetchone()
        if data is None:
            ratings[year] = "N/A"
        else:
            ratings[year] = data[0]

    for item in ratings:
        print(ratings[item])
    team = Teams.query.filter_by(team_id=player.teamid).first()
    return render_template("playerpage.html", player=player, ratings=ratings, team=team)