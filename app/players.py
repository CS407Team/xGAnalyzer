from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Player
from . import db


players = Blueprint('players', __name__)


@players.route('/players')
def match_history():
    playersList = Player.query.all()
    for person in playersList:
        print(person.playername)
    return 'Test'


@players.route('/player/<fName>-<lName>')
def player_page(fName, lName):
    #return f'{fName}, {lName}'
    return render_template("playerpage.html", fName=fName, lName=lName)
