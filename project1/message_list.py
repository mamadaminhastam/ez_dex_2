import sqlite3


# 1. connect DB

DATABASE_FILE = 'project1.db'

dbc = sqlite3.connect( DATABASE_FILE )

cursor = dbc.cursor()

scriptSQL = """
    SELECT * FROM messages
"""
cursor.execute( scriptSQL )

results = cursor.fetchall()
print("all message are fetched ! ")
print(results)
# 3. close connection

dbc.close()