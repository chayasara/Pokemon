import pymysql

def connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        db="pokemon",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )