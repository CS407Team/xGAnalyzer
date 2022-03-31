from . import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    email_address = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def is_authenticated(self):
        return None

    def is_active(self):
        return None

    def get_id(self):
        return self.userid

    def is_anonymous(self):
        return None

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Player(db.Model):
    playerid = db.Column(db.Integer, primary_key=True)
    teamid = db.Column(db.Integer)
    playername = db.Column(db.String(50))
    position = db.Column(db.String(20))
    player_age = db.Column(db.Integer)


class GamePredictions(db.Model):
    game_prediction_id = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer)
    away_team_id = db.Column(db.Integer)
    stats_predictions_id = db.Column(db.Integer)
    visibility = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(50))
    location = db.Column(db.String(20))
    status = db.Column(db.String(20))
    round_number = db.Column(db.Integer)
    winner = db.Column(db.Integer)


class Games(db.Model):
    gameid = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer)
    hometeam_id = db.Column(db.Integer)
    awayteam_id = db.Column(db.Integer)
    stats_id = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    prediction_name = db.Column(db.String(20))
    location = db.Column(db.String(20))
    status = db.Column(db.String(20))
    round_number = db.Column(db.Integer)
    xG_graph = db.Column(db.String(256))


class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer)
    team_name = db.Column(db.String(50))
    home_stadium = db.Column(db.String(50))

