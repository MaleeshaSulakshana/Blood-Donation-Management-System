import mysql.connector


def db_connector():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="blood_donation"
    )

    return conn
