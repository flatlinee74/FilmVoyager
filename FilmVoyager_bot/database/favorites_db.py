import sqlite3

def get_favorites_connection():
    return sqlite3.connect("favorites.db")