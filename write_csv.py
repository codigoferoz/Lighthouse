import sqlite3
import csv

def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()

def SaveToCsv():
    Database()
    cursor.execute("SELECT * FROM REGISTRATION_TASK")
    with open("out.csv", 'w',newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) 
        csv_writer.writerows(cursor)
    cursor.close()
    conn.close()