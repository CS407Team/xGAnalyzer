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
    updated_name = db.Column(db.String(255))


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
    status = db.Column(db.Integer)
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


class SeasonTable(db.Model):
    season_table_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer)
    team_position = db.Column(db.Integer)
    team_points = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    won = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    drawn = db.Column(db.Integer)
    round_number = db.Column(db.Integer)


class Stats(db.Model):
    statsid = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.Integer)
    round = db.Column(db.Integer)
    type = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer)
    away_team_id = db.Column(db.Integer)
    away_possession = db.Column(db.Integer)
    home_possession = db.Column(db.Integer)
    away_shots = db.Column(db.Integer)
    home_shots = db.Column(db.Integer)
    home_shots_on_target = db.Column(db.Integer)
    away_shots_on_target = db.Column(db.Integer)
    home_yellow_cards = db.Column(db.Integer)
    away_yellow_cards = db.Column(db.Integer)
    home_red_cards = db.Column(db.Integer)
    away_red_cards = db.Column(db.Integer)
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)
    home_pens = db.Column(db.Integer)
    away_pens = db.Column(db.Integer)
    home_freekicks = db.Column(db.Integer)
    away_freekicks = db.Column(db.Integer)
    home_pass_total = db.Column(db.Integer)
    away_pass_total = db.Column(db.Integer)
    home_complete_passes = db.Column(db.Integer)
    away_complete_passes = db.Column(db.Integer)


class TablePredictions(db.Model):
    table_prediction_id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer)
    team_position = db.Column(db.Integer)
    team_points = db.Column(db.Integer)
    goals_for = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    season_year = db.Column(db.Integer)
    visibility = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(50))


class PlayerRatings(db.Model):
    player_rating_id = db.Column(db.Integer, primary_key=True)
    playerid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    player_rating = db.Column(db.Integer)
    visibility = db.Column(db.Integer)
    sharability = db.Column(db.Integer)


class WatchlistElements(db.Model):
    userid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)


class Watchlist(db.Model):
    watchlistid = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer)
    visible = db.Column(db.Integer)
