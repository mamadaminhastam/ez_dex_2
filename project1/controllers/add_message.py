# add_message.py

import sqlite3


def handle( body ):

    # 1. connect DB

    DATABASE_FILE = 'app.db'

    dbc = sqlite3.connect( DATABASE_FILE )

    cursor = dbc.cursor()

    # 2. execute SQL script

    message = ('ali akbari', 'ali@yahoo.com', 'سایت خالی به چه درد می خوره؟') # tupple

    scriptSQL = '''

                INSERT INTO messages(name, email, message)

                VALUES(?, ?, ?)

            '''

    cursor.execute( scriptSQL , message)

    dbc.commit()

    print('پیام با موفقیت درج شد')

    # 3. close connection

    dbc.close()