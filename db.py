import sqlite3

DB_NAME = 'db/composers.sqlite'

def get_connection():
    return sqlite3.connect(DB_NAME)