import numpy as np
from PIL import Image
import requests
from io import BytesIO


def getXgData(xGFile, maxXG, teamname, col, kind):
    maxX = 1490
    maxY = 90
    xGData = []
    a = None
    if kind == "predict":
        response = requests.get(xGFile)
        if response is None:
            xGFile = "https://storage.googleapis.com/xganalyzer_exports/games/tottenham-liverpool-3.0.png"
            response = requests.get(xGFile)
        a = Image.open(BytesIO(response.content))
    elif kind == "upload":
        a = xGFile
    if a is None:
        xGFile = "https://storage.googleapis.com/xganalyzer_exports/games/tottenham-liverpool-3.0.png"
        response = requests.get(xGFile)
        if kind == "predict":
            a = Image.open(BytesIO(response.content))
        elif kind == "upload":
            a = xGFile
    response = requests.get(xGFile)
    c = Image.open(BytesIO(response.content))
    temp = np.asarray(c)
    print("temp is " + str(temp))
    for i in range(1, 19):
        xG = -1
        if col == "blue":
            if kind == "predict":
                b = xGFile.replace("https://storage.googleapis.com/xganalyzer_exports/games/", "").split("-")
                xGFile = "https://storage.googleapis.com/xganalyzer_exports/games/" + teamname + "-" + b[1] + "-" + b[2]
            for j in range(860, maxY, -1):
                if tuple(temp[j, 180 + round(i * (maxX - 180) / 18)]) == (0, 188, 212):
                    xG = maxXG * (860 - j) / (860 - maxY)
            if xG == -1:
                xG = findTillFound(maxXG, maxX, maxY, xGData, temp, i, "blue")
            xGData.append(round(xG, 2))
        elif col == "yellow":
            if kind == "predict":
                b = xGFile.replace("https://storage.googleapis.com/xganalyzer_exports/games/", "").split("-")
                xGFile = "https://storage.googleapis.com/xganalyzer_exports/games/" + b[0] + "-" + teamname + "-" + b[2]
            for j in range(860, maxY, -1):
                if tuple(temp[j, 180 + round(i * (maxX - 180) / 18)]) == (255, 235, 59) \
                        or tuple(temp[j, 180 + round(i * (maxX - 180) / 18)]) == (229, 230, 75):
                    xG = maxXG * (860 - j) / (860 - maxY)
            if xG == -1:
                xG = findTillFound(maxXG, maxX, maxY, xGData, temp, i, "yellow")
            xGData.append(round(xG, 2))
    return xGData


def findTillFound(maxXG, maxX, maxY, xGData, temp, min, col):
    xG = -1
    xGLeft = -1
    xGRight = -1
    left = 0
    right = 0
    start = 180
    end = maxX
    if round((maxX - 180) / 18) + 180 > round((maxX - 180) / 6):
        start = round((maxX - 180) / 18) + 180 - round((maxX - 180) / 6)
    if round((maxX - 180) / 18) + round((maxX - 180) / 6) + 180 < maxX:
        end = round((maxX - 180) / 18) + round((maxX - 180) / 6) + 180
    for i in range(180 + round((maxX - 180) / 18), start, -2):
        left = left + 1
        for j in range(860, maxY, -1):
            if col == "blue":
                if tuple(temp[j, i]) == (0, 188, 212):
                    xGLeft = maxXG * (860 - j) / (860 - maxY)
                    break
            elif col == "yellow":
                if tuple(temp[j, i]) == (255, 235, 59) or tuple(temp[j, i]) == (229, 230, 75):
                    xGLeft = maxXG * (860 - j) / (860 - maxY)
                    break
    if xGLeft == -1:
        xGLeft = 0.01
    if min == 18:
        if xGData[15] == 0.01:
            xG = xGData[16]
        elif xGData[16] == 0.01:
            xG = 0.01
        else:
            xG = xGData[16] * xGData[16] / xGData[15]
    else:
        for i in range(180 + round((maxX - 180) / 18), end, 2):
            right = right + 1
            for j in range(860, maxY, -1):
                if col == "blue":
                    if tuple(temp[j, i]) == (0, 188, 212):
                        xGRight = maxXG * (860 - j) / (860 - maxY)
                        break
                elif col == "yellow":
                    if tuple(temp[j, i]) == (255, 235, 59) or tuple(temp[j, i]) == (229, 230, 75):
                        xGRight = maxXG * (860 - j) / (860 - maxY)
                        break
        if xGRight == -1:
            xG = xGLeft
        else:
            xG = (xGLeft * right + xGRight * left) / (right + left)
    return xG
