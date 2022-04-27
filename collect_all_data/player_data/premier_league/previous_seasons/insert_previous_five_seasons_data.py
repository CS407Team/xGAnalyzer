import json
import os

import mysql.connector as mariadb
from mysql.connector import errorcode
try:
    db_connection = mariadb.connect(user='root', password='V3z?RnzC', host='35.225.215.107', database='analyzer')
except mariadb.Error as err:
    print("it dont work")

year = '2020'
files = os.listdir(year)
count = 0
for team in files:
    #print(team)
    with open(f'{year}/{team}') as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    for player in jsonObject:
        count = count + 1
        #rating = player['statistics'][0]['games']['rating']
        #print(rating)
        id = player['player']['id']
        #red = player['statistics'][0]['cards']['red']
        #yellow = player['statistics'][0]['cards']['yellow']
        #yellowred = player['statistics'][0]['cards']['yellowred']


        """ Adding yellow cards based on year
        if yellow is not None:
            db_cursor = db_connection.cursor()
            db_cursor.execute(f"update {year}ratings set yellow = {yellow} where playerid = {id}")
            db_connection.commit()
        """

        """ Adding yellow-red cards based on year
        if yellowred is not None:
            db_cursor = db_connection.cursor()
            db_cursor.execute(f"update {year}ratings set yellowred = {yellowred} where playerid = {id}")
            db_connection.commit()
        """

        """ Adding red cards based on year
        if red is not None:
            db_cursor = db_connection.cursor()
            db_cursor.execute(f"update {year}ratings set red = {red} where playerid = {id}")
            db_connection.commit()

        """

        """ Adding ratings based on year
        if rating is None:
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                f"insert into {year}ratings values ({id}, NULL)")
            db_connection.commit()
        else:
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                f"insert into {year}ratings values ({id}, {rating})")
            db_connection.commit()
        """

        #if id is None:
            #print("ID IS NONE")


print(count)