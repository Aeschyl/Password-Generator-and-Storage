import sqlite3

connection = sqlite3.connect('passwords.db')

cursor = connection.cursor()

cursor.execute("""CREATE TABLE Passwords (
            place text,
            password text
            )""")

connection.commit()

connection.close()