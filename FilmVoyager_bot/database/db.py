import sqlite3

def get_movies_connection():
    return sqlite3.connect("movies.db")