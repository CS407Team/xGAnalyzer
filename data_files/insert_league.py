import mysql.connector as mariadb
from mysql.connector import errorcode

try:
    db_connection = mariadb.connect(user = 'newuser', password='test', host='localhost', database = 'analyzer', port='3306')
    db_cursor = db_connection.cursor()
    sql = """insert into tournaments (name,total_teams, country, num_previous_seasons)values('Premier League', 20, 'England',5)"""
    db_cursor.execute(sql)

except mariadb.Error as err:
	print("Something went wrong: {}".format(err))
else:
    db_connection.commit()
    print("Done");
    db_connection.close()
    
    
