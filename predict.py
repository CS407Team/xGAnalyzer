from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from app import functions
from app import modules
from os import walk
import numpy as np
from sklearn import linear_model
from sklearn import svm

"""from statsbombpy import sb

sb.competitions()"""

"""X1 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/astonvilla-tottenham.png", 1.6)
X2 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/astonvilla-tottenham.png", 1.6,"blue")
X3 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/leicester-tottenham.png", 4.5)
X4 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/southampton-tottenham.png", 3.0)
X5 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/westham-tottenham.png", 1.8)
X6 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-brentford.png", 2.5,"blue")
X7 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-crystalpalace.png", 3.0,"blue")
X8 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-liverpool.png", 3.0,"blue")
X9 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-southampton.png", 1.80,"blue")
X10 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-watford.png", 1.0,"blue")
X11 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/arsenal-tottenham.png", 1.6,"blue")
X12 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/chelsea-tottenham.png", 1.2,"blue")
X13 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/leicester-tottenham.png", 4.5,"blue")
X14 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/southampton-tottenham.png", 3.0,"blue")
X15 = functions.getXgDataBlue("https://storage.googleapis.com/xganalyzer_exports/games/westham-tottenham.png", 1.8,"blue")
X16 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-brentford.png", 2.5,"blue")
X17 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-crystalpalace.png", 3.0)
X18 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-liverpool.png", 3)
X19 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-southampton.png", 1.8)
X20 = functions.getXgDataYellow("https://storage.googleapis.com/xganalyzer_exports/games/tottenham-watford.png", 1)
print("X1 is " + str(X1))
x = [X1, X2, X8, X4, X5, X6, X7, X9, X10]
y = [1, 0, 2, 1, 0, 2, 3, 2, 1]
model = LogisticRegression(solver='lbfgs')
model.fit(x, y)
new_input = [X3]
new_output = model.predict(new_input)
X = [X11, X12, X8, X14, X15, X16, X17, X19, X20]
Y = [3, 2, 2, 1, 1, 0, 0, 3, 0]
mod = LogisticRegression(solver='lbfgs')
mod.fit(X, Y)
inp = [X13]
output = mod.predict(inp)"""


def predictRes(teamNextXG, teamPrevXG, teamRes):
    model = LogisticRegression(solver='lbfgs', max_iter=2500)
    print(str(teamPrevXG) + " model with " + str(teamRes))
    model.fit(teamPrevXG, teamRes)
    teamFinal = model.predict(teamNextXG)
    print("result " + str(teamFinal))
    return teamFinal


def getPrevxG(teamname, filenames, scoreOrCon):
    teamXG = []
    for team in filenames:
        col = "yellow"
        if scoreOrCon == "conceive":
            col = "blue"
        if team.find(teamname) < team.find("-"):
            col = "blue"
            if scoreOrCon == "conceive":
                col = "yellow"
        teamXG.append(functions.getXgData(team, float(team.split("-")[2].replace(".png", "")), teamname, col, "predict"))
    print("prev xG " + str(teamXG))
    return teamXG


def getNextxG(teamXG, teamname):
    teamNext = []
    teamRes = []
    teamFinal = []
    print("team XG " + str(teamXG))
    for j in range(18):
        for i in range(0, 5):
            teamNext.append([int(teamXG[i][j] * 100), int(teamXG[i + 1][j] * 100), int(teamXG[i + 2][j] * 100),
                             int(teamXG[i + 3][j] * 100), int(teamXG[i + 4][j] * 100)])
            teamRes.append(int(teamXG[i + 5][j] * 100))
        model = LogisticRegression(solver='lbfgs', max_iter=2500)
        print(str(teamNext) + " models with " + str(teamRes) + " " + str(teamname))
        if teamRes[0] == teamRes[1] == teamRes[2] == teamRes[3] == teamRes[4]:
            teamRes[4] += 1
        model.fit(teamNext, teamRes)
        teamGuess = [[int(teamXG[5][j] * 100), int(teamXG[6][j] * 100), int(teamXG[7][j] * 100),
                      int(teamXG[8][j] * 100), int(teamXG[9][j] * 100)]]
        teamFinal.append(float(model.predict(teamGuess)) / 100)
        teamNext = []
        teamRes = []
    print("team final " + str(teamFinal))
    return teamFinal


def predct(homeid, awayid, homename, awayname, homeXGs, awayXGs, homeRes, awayRes):
    homefiles = []
    homescoreRes = []
    homeconveRes = []
    awayfiles = []
    awayscoreRes = []
    awayconveRes = []
    for i in range(len(homeXGs)):
        if homeid == homeXGs[i][1]:
            htempXG = homeXGs[i][1]
            homeXGs[i][1] = homeXGs[i][0]
            homeXGs[i][0] = htempXG
            htempRes = homeRes[i][1]
            homeRes[i][1] = homeRes[i][0]
            homeRes[i][0] = htempRes
        homefiles.append(homeXGs[i][2])
        if awayid == awayXGs[i][1]:
            atempXG = awayXGs[i][1]
            awayXGs[i][1] = awayXGs[i][0]
            awayXGs[i][0] = atempXG
            atempRes = awayRes[i][1]
            awayRes[i][1] = awayRes[i][0]
            awayRes[i][0] = atempRes
        awayfiles.append(awayXGs[i][2])
    for i in range(len(homeRes)):
        homescoreRes.append(homeRes[i][0])
        homeconveRes.append(homeRes[i][1])
        awayscoreRes.append(awayRes[i][0])
        awayconveRes.append(awayRes[i][1])
    print("homescore Res")
    print(str(homefiles))
    print(str(awayfiles))
    homePrevXG = getPrevxG(homename, homefiles, "goal")
    homeNextXG = [getNextxG(homePrevXG, homename)]
    homePrevCon = getPrevxG(homename, homefiles, "conceive")
    homeNextCon = [getNextxG(homePrevCon, homename)]
    homeXgoals = 0
    awayPrevXG = getPrevxG(awayname, awayfiles, "goal")
    awayNextXG = [getNextxG(awayPrevXG, awayname)]
    awayPrevCon = getPrevxG(awayname, awayfiles, "conceive")
    awayNextCon = [getNextxG(awayPrevCon, awayname)]
    awayXgoals = 0
    for homeXG in homeNextXG[0]:
        homeXgoals += homeXG
    for awayCon in awayNextCon[0]:
        homeXgoals += awayCon
    homeXgoals = homeXgoals / len(homeNextXG) / 2
    homeround = round(homeXgoals)
    for awayXG in awayNextXG[0]:
        awayXgoals += awayXG
    for homeCon in homeNextCon[0]:
        awayXgoals += homeCon
    awayXgoals = awayXgoals / len(awayNextXG) / 2
    awayround = round(awayXgoals)
    homegoals = int(
        (predictRes(homeNextXG, homePrevXG, homescoreRes) + predictRes(awayNextCon, awayPrevCon, awayconveRes)) / 2)
    if homeXgoals - float(int(homeXgoals)) < 0.5:
        homegoals += 1
    awaygoals = int(
        (predictRes(awayNextXG, awayPrevXG, awayscoreRes) + predictRes(homeNextCon, homePrevCon, homeconveRes)) / 2)
    if awayXgoals - float(int(awayXgoals)) < 0.5:
        awaygoals += 1
    prediction = [homegoals, awaygoals]
    analysis = []
    homestr = homename + " will score " + str(homegoals) + " goal(s) with a " + \
              str(round(100 - 100 * abs(homeXgoals - float(homeround)), 2)) + "% probability"
    awaystr = awayname + " will score " + str(awaygoals) + " goal(s) with a " + \
              str(round(100 - 100 * abs(awayXgoals - float(awayround)), 2)) + "% probability"
    analysis.append(homestr)
    analysis.append(awaystr)
    return prediction, analysis


def predctXG(homeid, awayid, homename, awayname, homeXGs, awayXGs, homeRes, awayRes, xGgraph, maxXG):
    homefiles = []
    homescoreRes = []
    homeconveRes = []
    awayfiles = []
    awayscoreRes = []
    awayconveRes = []
    for i in range(len(homeXGs)):
        if homeid == homeXGs[i][1]:
            htempXG = homeXGs[i][1]
            homeXGs[i][1] = homeXGs[i][0]
            homeXGs[i][0] = htempXG
            htempRes = homeRes[i][1]
            homeRes[i][1] = homeRes[i][0]
            homeRes[i][0] = htempRes
        homefiles.append(homeXGs[i][2])
        if awayid == awayXGs[i][1]:
            atempXG = awayXGs[i][1]
            awayXGs[i][1] = awayXGs[i][0]
            awayXGs[i][0] = atempXG
            atempRes = awayRes[i][1]
            awayRes[i][1] = awayRes[i][0]
            awayRes[i][0] = atempRes
        awayfiles.append(awayXGs[i][2])
    for i in range(len(homeRes)):
        homescoreRes.append(homeRes[i][0])
        homeconveRes.append(homeRes[i][1])
        awayscoreRes.append(awayRes[i][0])
        awayconveRes.append(awayRes[i][1])
    print("homescore Res")
    print(str(homefiles))
    print(str(awayfiles))
    homePrevXG = getPrevxG(homename, homefiles, "goal")
    homeNextXG = [functions.getXgData(xGgraph, maxXG, homename, "blue", "upload")]
    homePrevCon = getPrevxG(homename, homefiles, "conceive")
    homeNextCon = [functions.getXgData(xGgraph, maxXG, homename, "yellow", "upload")]
    homeXgoals = 0
    awayPrevXG = getPrevxG(awayname, awayfiles, "goal")
    awayNextXG = [functions.getXgData(xGgraph, maxXG, awayname, "yellow", "upload")]
    awayPrevCon = getPrevxG(awayname, awayfiles, "conceive")
    awayNextCon = [functions.getXgData(xGgraph, maxXG, awayname, "blue", "upload")]
    awayXgoals = 0
    for homeXG in homeNextXG[0]:
        homeXgoals += homeXG
    for awayCon in awayNextCon[0]:
        homeXgoals += awayCon
    homeXgoals = homeXgoals / len(homeNextXG) / 2
    homeround = round(homeXgoals)
    for awayXG in awayNextXG[0]:
        awayXgoals += awayXG
    for homeCon in homeNextCon[0]:
        awayXgoals += homeCon
    awayXgoals = awayXgoals / len(awayNextXG) / 2
    awayround = round(awayXgoals)
    homegoals = int(
        (predictRes(homeNextXG, homePrevXG, homescoreRes) + predictRes(awayNextCon, awayPrevCon, awayconveRes)) / 2)
    if homeXgoals - float(int(homeXgoals)) < 0.5:
        homegoals += 1
    awaygoals = int(
        (predictRes(awayNextXG, awayPrevXG, awayscoreRes) + predictRes(homeNextCon, homePrevCon, homeconveRes)) / 2)
    if awayXgoals - float(int(awayXgoals)) < 0.5:
        awaygoals += 1
    prediction = [homegoals, awaygoals]
    analysis = []
    homestr = homename + " will score " + str(homegoals) + " goal(s) with a " + \
              str(round(100 - 100 * abs(homeXgoals - float(homeround)), 2)) + "% probability"
    awaystr = awayname + " will score " + str(awaygoals) + " goal(s) with a " + \
              str(round(100 - 100 * abs(awayXgoals - float(awayround)), 2)) + "% probability"
    analysis.append(homestr)
    analysis.append(awaystr)
    return prediction, analysis


if __name__ == '__main__':
    liver = "https://storage.googleapis.com/xganalyzer_exports/games/chelsea-liverpool-2.5.png"
    print("hello")
