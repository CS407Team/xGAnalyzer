import json
import os
import mysql as mysql
from flask import Flask, redirect, request, render_template, url_for, session, jsonify
from typing import List
from PIL import Image
import requests
from io import BytesIO
from app import modules as modules
from app import predict as predict
from app import teams as teams
from app import config
import app.apple as apple
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from flask.scaffold import F
from flask.wrappers import Response
import os
import re
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from mysql import connector as connector
import mysql.connector as connector
import sys
import app.database as database
import pymongo

import uuid
import base64
from os import walk

UPLOAD_FOLDER = '..\images'
app = Flask(__name__, template_folder='html', static_folder='static')
app.secret_key = 'gohoho'
app.config['HOME'] = str(os.getcwd())
app.config['UPLOAD_FOLDER'] = os.getcwd() + "/static/" + "playrs.json"
app.debug = True
leagues = modules.get_league()
leagues2 = modules.get_league()
imageExtensions = ['png', 'jpg']


@app.route("/", methods=["POST", "GET"])
def home():
    pos = []
    if request.method == "POST":
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        print(password)
        user = None
        if modules.get_user(str(username), str(password)):
            user = modules.get_user(str(username), str(password))[0]
        if user is None:
            return render_template('notfound.html', message="Username or Password not found")
        return redirect(
            url_for('userpage', userid=int(user[0]), username=str(user[1]), leagueid=1, leagueid2=1, season='2021'))
    else:
        return render_template('login.html')


@app.route("/userpage/<userid>/<username>/<leagueid>/<leagueid2>/<season>", methods=["POST", "GET"])
def userpage(userid, username, leagueid, leagueid2, season):
    tems = modules.get_team(leagueid)
    tems2 = modules.get_team(leagueid2)
    pos = []
    pos = pos.sort()
    if request.method == "POST":
        tourid = request.form.get('league')
        tourid2 = request.form.get('league')
        fav_team = request.form.get('team')
        season = str(request.form.get('season'))
        if season == '2020' and not teams.teams_2020.__contains__(teams.teams_2021[int(fav_team)]):
            return render_template('notfound.html', message="team were not there that season")
        modules.insert_fav_team(userid, fav_team)
        for league in leagues:
            if int(league['leagueid']) == int(tourid):
                leagues.remove(league)
                leagues.insert(0, league)
        for league2 in leagues2:
            if int(league2['leagueid']) == int(tourid2):
                leagues2.remove(league2)
                leagues2.insert(0, league2)
        return redirect(url_for('userpage', userid=int(userid),
                                username=str(username), leagueid=int(tourid),
                                leagueid2=int(tourid2), season=season, pos=pos))
    else:
        fav_teams = modules.get_fav_team(userid)
        favs = []
        for f in fav_teams:
            favs.append(teams.teams_2021[f])
        print(str(fav_teams))
        fav_team_res = []
        fav_team_pos = []
        print("season " + str(season))
        print("length" + str(len(fav_teams)))
        for team in fav_teams:
            fav_res = modules.get_stat(team, season)
            fav_pos = modules.get_fav_pos(team, season)
            print("favpos " + str(fav_pos))
            print(str(fav_res))
            for fav in fav_res:
                home_in = int(fav[0]) % 100 + int(fav[0]) // 10
                away_in = int(fav[1]) % 100 + int(fav[1]) // 10
                home = None
                away = None
                if str(season) == '2021':
                    home = teams.teams_2021[home_in]
                    away = teams.teams_2021[away_in]
                elif str(season) == '2020':
                    home = teams.teams_2020[home_in]
                    away = teams.teams_2020[away_in]
                elif str(season) == '2019':
                    home = teams.teams_2019[home_in]
                    away = teams.teams_2019[away_in]
                elif str(season) == '2018':
                    home = teams.teams_2018[home_in]
                    away = teams.teams_2018[away_in]
                elif str(season) == '2017':
                    home = teams.teams_2017[home_in]
                    away = teams.teams_2017[away_in]
                if int(fav[2]) != -1 and int(fav[3]) != -1:
                    fav_team_res.append([home, away, fav[2], fav[3], fav[4]])
            fav_team_pos.append(fav_pos[0])
        return render_template('userpage.html', userid=int(userid), username=str(username), leagueid=int(leagueid),
                               leagueid2=int(leagueid2),
                               season=season, pos=pos,
                               leagues=leagues, leagues2=leagues2, teams=tems, teams2=tems2, fav_team_res=fav_team_res,
                               fav_team_pos=fav_team_pos, favs=favs)


@app.route("/useraccount/accept/<notid>/<item>/<userid>/<username>/<targetid>/<leagueid>/<leagueid2>/<season>")
def accept(notid, item, userid, username, targetid, leagueid, leagueid2, season):
    modules.accept_noti(notid, item)
    players = modules.get_players(targetid)
    return redirect(url_for('useraccount', targetid=targetid, userid=userid, username=username,
                            leagueid=leagueid, leagueid2=leagueid2, players=players, season=season))


@app.route("/useraccount/decline/<notid>/<item>/<userid>/<username>/<targetid>/<leagueid>/<leagueid2>/<season>")
def decline(notid, item, userid, username, targetid, leagueid, leagueid2, season):
    modules.decline_noti(notid, item)
    players = modules.get_players(targetid)
    return redirect(url_for('useraccount', targetid=targetid, userid=userid, username=username,
                            leagueid=leagueid, leagueid2=leagueid2, players=players, season=season))


@app.route("/useraccount/<userid>/<username>/<targetid>/<leagueid>/<leagueid2>/<season>", methods=["POST", "GET"])
def useraccount(userid, username, targetid, leagueid, leagueid2, season):
    tems = modules.get_team(leagueid)
    tems2 = modules.get_team(leagueid2)
    userinfo = modules.get_userinfo(userid)
    notifications = modules.get_notice(userid)
    followers = modules.get_follower(targetid)
    followings = modules.get_following(targetid)
    players = modules.get_players(targetid)
    file = Response(players, mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=player_rating.json'})
    f = open("static/playrs.json", "a")
    json_object = json.dumps(players, indent=15)
    with open("static/playrs.json", 'w') as filetowrite:
        filetowrite.write(json_object)
    pos = []
    pos = pos.sort()
    if request.method == "POST":
        items = request.form.get('items')
        search = request.form.get('searchi')
        searchval = modules.get_users(str(search))
        return render_template('search.html', notifications=notifications, followers=followers,
                               followings=followings, links=searchval,
                               userid=int(userid), userinfo=userinfo, username=username,
                               targetid=targetid, leagueid=leagueid, leagueid2=leagueid2,
                               season=season, pos=pos)
    else:
        fav_teams = modules.get_fav_team(userid)
        favs = []
        for f in fav_teams:
            favs.append(teams.teams_2021[f])
        print(str(fav_teams))
        fav_team_res = []
        fav_team_pos = []
        for team in fav_teams:
            fav_res = modules.get_stat(team, season)
            fav_pos = modules.get_fav_pos(team, season)
            for fav in fav_res:
                home_in = int(fav[0]) % 100 + int(fav[0]) // 10
                away_in = int(fav[1]) % 100 + int(fav[1]) // 10
                home = None
                away = None
                if str(season) == '2021':
                    home = teams.teams_2021[home_in]
                    away = teams.teams_2021[away_in]
                elif str(season) == '2020':
                    home = teams.teams_2020[home_in]
                    away = teams.teams_2020[away_in]
                elif str(season) == '2019':
                    home = teams.teams_2019[home_in]
                    away = teams.teams_2019[away_in]
                elif str(season) == '2018':
                    home = teams.teams_2018[home_in]
                    away = teams.teams_2018[away_in]
                elif str(season) == '2017':
                    home = teams.teams_2017[home_in]
                    away = teams.teams_2017[away_in]
                if int(fav[2]) != -1 and int(fav[3]) != -1:
                    fav_team_res.append([home, away, fav[2], fav[3], fav[4]])
            fav_team_pos.append(fav_pos[0])
        notifications = modules.get_notice(userid)
        session['url'] = url_for('useraccount', userid=userid, username=username, targetid=targetid,
                                 leagueid=leagueid, leagueid2=leagueid2, season=season)
        return render_template('useraccount.html', followers=followers,
                               followings=followings, userid=int(userid), username=str(username),
                               leagueid=int(leagueid), targetid=int(targetid), file=file,
                               leagueid2=int(leagueid2), notifications=notifications,
                               season=season, pos=pos, players=players,
                               leagues=leagues, leagues2=leagues2, teams=tems, teams2=tems2,
                               fav_team_res=fav_team_res, fav_team_pos=fav_team_pos, favs=favs)


@app.route("/downloads/<filename>")
def download(filename):
    send_from_directory(directory=app.config['UPLOAD_FOLDER'], path="", filename=filename)
    #send_from_directory(directory=app.static_folder, path=filename, filename="playrs.json")
    return redirect(session['url'])


@app.route("/table/<userid>/<username>/<leagueid>/<pos>")
def table(userid, username, leagueid, pos):
    return render_template('table.html', userid=userid, username=username, leagueid=leagueid, pos=pos)


@app.route('/uploadpage/<userid>/<username>/<leagueid>/<leagueid2>')
def upload_page(userid, username, leagueid, leagueid2):
    teams = modules.get_team(leagueid)
    return render_template('upload.html', userid=int(userid), username=str(username), leagueid=int(leagueid),
                           leagueid2=int(leagueid2), leagues=leagues, teams=teams)


@app.route('/uploadimage/<userid>/<username>/<leagueid>', methods=['POST', 'GET'])
def upload_image(userid, username, leagueid):
    teams = modules.get_team(leagueid)
    if request.method == "POST":
        hometeam = str(request.form.get('hometeam'))
        awayteam = str(request.form.get('awayteam'))
        XGmax = str(request.form['maxXG'])
        if re.match(r'^-?\d+(?:\.\d+)$', XGmax) is None:
            return render_template('notfound.html', message="max XG does not represent a float value")
        maxXG = 0
        if 'file' not in request.files:
            return render_template('notfound.html', message="No xG graphs uploaded")
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and '.' in file.filename and imageExtensions.__contains__(file.filename.rsplit('.', 1)[1].lower()):
            filename = secure_filename(file.filename)
            if filename.__contains__(".."):
                return render_template('notfound.html', message="File name cannot contain '..' because there might be "
                                                                "a outer directory vulnerability (../)")
            # self.write("http://localhost:8080/img/"+filename)
            response = requests.get("https://storage.googleapis.com/xganalyzer_exports/games/" + filename)
            try:
                Image.open(BytesIO(response.content))
            except IOError:
                return render_template('notfound.html', message="xG graph is not a valid image file")
            if str(hometeam) != "" and str(awayteam) != "" and str(hometeam) != "None" and str(awayteam) != "None":
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = "https://storage.googleapis.com/xganalyzer_exports/games/" + filename
                homeid = hometeam.split(',')[0]
                homename = hometeam.split(',')[1]
                homelower = homename.lower().replace(" ", "")
                homelastten = getLastTen(homeid)
                homeresten = getResTen(homelastten)
                awayid = awayteam.split(',')[0]
                awayname = awayteam.split(',')[1]
                awaylower = awayname.lower().replace(" ", "")
                if not filename.split("-")[0].__contains__(homelower) or \
                        not filename.split("-")[1].__contains__(awaylower):
                    return render_template('notfound.html', message="Filename of the wrong format")
                awaylastten = getLastTen(awayid)
                awayresten = getResTen(awaylastten)
                print(str(homelastten))
                print(str(awayresten))
                prediction = predict.predctXG(homeid, awayid, homename, awayname, homelastten,
                                              awaylastten, homeresten, awayresten, filename, maxXG)
                return render_template('prediction.html',
                                       userid=int(userid), username=str(username), leagueid=int(leagueid),
                                       teams=teams, homename=homename, awayname=awayname, prediction=prediction[0],
                                       analysis=prediction[1])
            return render_template('notfound.html', message="Home or away team was not chosen")
        else:
            return render_template('notfound.html',
                                   message="For security reasons we only allow image files of type png and jpg")
    else:
        return render_template('upload.html')


@app.route("/predict/<userid>/<username>/<leagueid>/<leagueid2>", methods=["POST", "GET"])
def guess(userid, username, leagueid, leagueid2):
    teams = modules.get_team(leagueid)
    teams2 = modules.get_team(leagueid2)
    default = {"teamid": 0, "name": ""}
    teams.insert(0, default)
    if request.method == "POST":
        tourid = request.form.get('league')
        tourid2 = request.form.get('league2')
        hometeam = str(request.form.get('hometeam'))
        awayteam = str(request.form.get('awayteam'))
        if str(hometeam) != "" and str(awayteam) != "" and str(hometeam) != "None" and str(awayteam) != "None":
            print("hometeam " + str(hometeam))
            print("awayteam " + str(hometeam))
            homeid = hometeam.split(',')[0]
            homename = hometeam.split(',')[1]
            homelastten = getLastTen(homeid)
            homeresten = getResTen(homelastten)
            awayid = awayteam.split(',')[0]
            awayname = awayteam.split(',')[1]
            awaylastten = getLastTen(awayid)
            awayresten = getResTen(awaylastten)
            prediction = predict.predct(homeid, awayid, homename, awayname, homelastten,
                                        awaylastten, homeresten, awayresten)
            return render_template('prediction.html', userid=int(userid), username=str(username),
                                   leagueid=int(leagueid), leagueid2=int(leagueid2),
                                   teams=teams, homename=homename, awayname=awayname, prediction=prediction[0],
                                   analysis=prediction[1])
        for league in leagues:
            if int(league['leagueid']) == int(tourid):
                leagues.remove(league)
                leagues.insert(0, league)
        for league2 in leagues2:
            if int(league2['leagueid']) == int(tourid2):
                leagues2.remove(league2)
                leagues2.insert(0, league2)
        return redirect(url_for('guess', userid=int(userid),
                                username=str(username), leagueid=int(tourid), leagueid2=int(tourid2)))
    else:
        return render_template('predict.html', userid=int(userid), username=str(username), leagueid=int(leagueid),
                               leagueid2=int(leagueid2),
                               leagues=leagues, leagues2=leagues2, teams=teams, teams2=teams2)


def getLastTen(getid):
    getgames = modules.get_record(getid)
    getlastten = []
    for i in range(len(getgames) - 1, len(getgames) - 11, -1):
        getlastten.append(getgames[i])
    if len(getgames) < 10:
        for j in range(10 - len(getgames)):
            getlastten.append(getgames[len(getgames) - 1 - j])
    return getlastten


def getResTen(getlastten):
    results = []
    for game in getlastten:
        result = modules.get_result(game[0], game[1])[0]
        results.append(result)
    return results
    """@app.route("/", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            db_cursor.execute("SELECT userid FROM users WHERE username = %s and password = %s",
                              (username, password))
            return render_template('userpage.html')
        else:
            return render_template('login.html')

    @app.route("/", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            db_cursor.execute("SELECT userid FROM users WHERE username = %s and password = %s",
                              (username, password))
            return render_template('userpage.html')
        else:
            return render_template('login.html')

    @app.route("/", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            db_cursor.execute("SELECT userid FROM users WHERE username = %s and password = %s",
                              (username, password))
            return render_template('userpage.html')
        else:
            return render_template('login.html')"""


if __name__ == '__main__':
    """apple.getXgDataBlue('includes/newcastle-everton.png', 3.0, 1500, 140)
    apple.getXgDataYellow('includes/newcastle-everton.png', 3.0, 1500, 140)"""
    app.run(debug=True)
    # app.getXgDataBlue('includes/burnley-manchesterunited.png', 2.0, 1468, 90)
    # app.getXgDataYellow('includes/burnley-manchesterunited.png', 2.0, 1468, 90)
