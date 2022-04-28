from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from . import database
from flask_login import LoginManager, login_manager
import mysql.connector as connector
import decimal
import subprocess as sub
import nltk
from . import database
import sys
from statsbombpy import sb

app = Flask(__name__, template_folder='../html')

db_connection = None
db_cursor = None

try:
    db_connection = connector.connect(user=database.user,
                                      password=database.password,
                                      host=database.host,
                                      database=database.name)
except connector.Error as err:
    print("ERROR")

db_cursor = db_connection.cursor(buffered=True)

get_user_sql = "SELECT username, userid FROM users WHERE username = %s AND password = %s"
get_league_sql = "SELECT name, tournament_id FROM tournaments"
get_team_sql = "SELECT team_name, team_id FROM teams WHERE tournament_id = %s"
get_result_sql = "SELECT home_goals,away_goals FROM new_stats WHERE (home_team_id = %s AND away_team_id = %s) OR " \
                 " (away_team_id = %s AND home_team_id  = %s) AND season = 2020"
get_record_sql = "SELECT hometeam_id, awayteam_id, xG_graph FROM new_games WHERE hometeam_id = %s OR awayteam_id = %s"
get_game2_sql = "SELECT * FROM new_stats WHERE (home_team_id = %s OR away_team_id = %s) AND season = %s limit 10"
get_fav_team_sql = "select team_ids from favorites where userid = %s"
get_fav_pos_sql = "select position from positions where teamid = %s and season = %s"
insert_fav_team_sql = "insert into favorites(userid,team_ids) values (%s,%s)"
get_team_avg = "select avg(position) from positions where teamid = %s group by teamid"
get_user_info_sql = "SELECT * from users u join favorites f on u.userid = f.userid join game_predictions g" \
                    " on u.userid = g.userid join table_predictions t on u.userid = t.userid where u.userid = %s"
get_notice_sql = "SELECT * FROM notification where userid = %s"
get_player_sql = "select * from player_performance_prediction where userid = %s"
get_follower_sql = "select count(*) from followers where userid = %s"
get_following_sql = "select count(*) from followings where userid = %s"
get_prediction_sql = "SELECT * FROM prediction WHERE homeid = %s and awayid = %s"
insert_prediction_sql = "INSERT INTO prediction(homeid, awayid, homegoals, awaygoals, homeanal, awayanal) " \
                        "values (%s,%s,%s,%s,%s,%s)"
set_noti_sql = "DELETE FROM notification where notid = %s"
set_permission_sql = "UPDATE permision SET permision = %d WHERE itemid = %s"
get_users_sql = "select userid, username from users where username like "
get_follow_sql = "select count(followers), count(followings) from follow where userid=%s and " \
                 "followers >= 0 and followings >= 0"


def get_user(a, b):
    db_cursor.execute(get_user_sql, (a, b))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append([res[1], res[0]])
    return result


def get_users(a):
    get_users_full = get_users_sql + "'%" + str(a) + "%'"
    db_cursor.execute(get_users_full)
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append({"userid": res[0], "username": res[1]})
    return result


def get_players(a):
    db_cursor.execute(get_player_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append({"game": res[2], "name": res[1], "tackles": res[3], "ctack": res[4], "yellows": res[5],
                       "reds": res[6], "shots": res[8], "target": res[9], "goals": res[7], "passes": res[10],
                       "cpass": res[11], "saves": res[12], "assists": res[15], "concede": res[16],
                       "visibility": res[17]})
    return result


def get_follower(a):
    db_cursor.execute(get_follower_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res)
    return result


def get_following(a):
    db_cursor.execute(get_following_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res)
    return result


def accept_noti(a, b):
    db_cursor.execute(set_noti_sql, (a,))
    db_cursor.execute(set_permission_sql, (1, b))
    db_connection.commit()


def decline_noti(a, b):
    db_cursor.execute(set_noti_sql, (a,))
    db_cursor.execute(set_permission_sql, (0, b))
    db_connection.commit()


def get_notice(a):
    db_cursor.execute(get_notice_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res)
    return result


def insert_prediction(homeid, awayid, homegoals, awaygoals, homestr, awaystr):
    db_cursor.execute(insert_prediction_sql, (homeid, awayid, homegoals, awaygoals, homestr, awaystr))
    db_connection.commit()


def get_stat(a, b):
    db_cursor.execute(get_game2_sql, (a, a, b))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append([res[1], res[2], res[3], res[4], res[5]])
    return result


def get_userinfo(a):
    db_cursor.execute(get_user_info_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append([res[1], res[2], res[3], res[4], res[5]])
    return result


def get_fav_team(a):
    db_cursor.execute(get_fav_team_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res[0])
    return result


def get_fav_pos(a, b):
    db_cursor.execute(get_fav_pos_sql, (a, b))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res[0])
    return result


def get_avg(a):
    db_cursor.execute(get_team_avg, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res[0])
    return result


def insert_fav_team(a, b):
    db_cursor.execute(insert_fav_team_sql, (a, b))
    db_connection.commit()
    return 1


def get_league():
    db_cursor.execute(get_league_sql)
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append({"leagueid": res[1], "name": res[0]})
    return result


def get_team(a):
    db_cursor.execute(get_team_sql, (a,))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append({"teamid": res[1], "name": res[0]})
    return result


def get_record(a):
    db_cursor.execute(get_record_sql, (a, a))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append([res[0], res[1], res[2]])
    return result


def get_result(a, b):
    db_cursor.execute(get_result_sql, (a, b, a, b))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append([res[0], res[1]])
    return result


def get_prediction(homeid, awayid):
    db_cursor.execute(get_prediction_sql, (homeid, awayid))
    result = []
    for res in db_cursor.fetchall():
        if res is None:
            return None
        result.append(res)
    return result
