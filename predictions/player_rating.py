from app import db
from app.models import GamePredictions, SeasonTable, Teams, Games, Stats, TablePredictions, User, \
    PlayerRatings, Player, Watchlist, WatchlistElements
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


def get_player_list(userid):
    players = WatchlistElements.query.filter_by(userid=userid).all()
    list_of_players = []
    for player in players:
        list_of_players.append(Player.query.filter_by(playerid=player.playerid).first())

    return list_of_players


def add_player_to_watchlist(userid, playername):
    watchlist = Watchlist.query.filter_by(userid=userid).first()
    if watchlist is None:
        new_watchlist = Watchlist(userid=userid, visible=1)
        db.session.add(new_watchlist)

    player = Player.query.filter_by(playername=playername).first()
    if not player:
        return 0
    watchlist_elements = WatchlistElements(userid=userid, playerid=player.playerid)
    db.session.add(watchlist_elements)
    db.session.commit()
    return 1


def change_visibility(visibility, userid):
    db.session.query(Watchlist).filter_by(userid=userid).update({'visible': visibility})
    db.session.commit()


def find_user_watchlist(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        print("error2")
        return None

    check = Watchlist.query.filter_by(userid=user.userid).first()

    if check.visible == 1:
        visible = WatchlistElements.query.filter_by(userid=user.userid).all()
        playerlist = []
        for vis in visible:
            newplayer = Player.query.filter_by(playerid=vis.playerid).first()
            playerlist.append(newplayer)
        return playerlist
    else:
        print("error3")
        return None
