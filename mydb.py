import mysql.connector as mysql

try:
    database = mysql.connect(
        host="localhost",
        password = "ahmad123",
        user = "root",
    )
    conn = database.cursor()
    print("Connection Successful")
except Exception as e:
    print(e)

