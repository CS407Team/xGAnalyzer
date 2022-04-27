from app import db
from app.models import GamePredictions, SeasonTable, Teams, Games, Stats, TablePredictions, User, \
    PlayerRatings, Player
from flask_login import current_user


def edit(player_rating_id, player_rating, visibility, sharability):
    if player_rating:
        db.session.query(PlayerRatings).filter_by(player_rating_id=player_rating_id).update(
            {'player_rating': player_rating})
    if visibility:
        db.session.query(PlayerRatings).filter_by(player_rating_id=player_rating_id).update({'visibility': visibility})
    if sharability:
        db.session.query(PlayerRatings).filter_by(player_rating_id=player_rating_id).update(
            {'sharability': sharability})
    db.session.commit()


def download(pr):
    new_download = PlayerRatings(playerid=pr.playerid, userid=current_user.userid,
                                 team_id=pr.team_id, player_rating=pr.player_rating, visibility=pr.visibility,
                                 sharability=pr.sharability)
    db.session.add(new_download)
    db.session.commit()
