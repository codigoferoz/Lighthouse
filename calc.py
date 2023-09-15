import sqlite3

def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
