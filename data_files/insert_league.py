import mysql.connector as mariadb
from mysql.connector import errorcode

try:
    db_connection = mariadb.connect(user = 'newuser', password='test', host='localhost', database = 'analyzer', port='3306')
    db_cursor = db_connection.cursor()
    db_cursor.execute("insert into tournaments(name,total_teams,country, num_previous_seasons) values('Premier League', '20', 'England','5')")

except mariadb.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Done");
    db_connection.close()
    
    