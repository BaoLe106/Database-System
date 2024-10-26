import mysql.connector
from mysql.connector import Error


db_config = {
    'user': 'root',
    'password': '010603', #your mysql server password
    'host': 'localhost',
    'database': 'dbsys'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)