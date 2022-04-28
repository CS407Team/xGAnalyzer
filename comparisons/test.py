from os import lseek
import mysql.connector

mydb = mysql.connector.connect(
  host="35.225.215.107",
  user="root",
  password="V3z?RnzC",
  database="analyzer"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM games")

myresult = mycursor.fetchall()
print(myresult)

lseek