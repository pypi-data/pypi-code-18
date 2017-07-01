import sqlite3

def connect_to_db(db_file):
    db_connection = sqlite3.connect(db_file)
    with db_connection:
        db_connection.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL UNIQUE
        )''')

    return db_connection

def insert_in_db(db_connection, text):
    with db_connection:
        db_connection.execute('INSERT INTO notes(text) VALUES(?)', (text,))

def exists_in_db(db_connection, text):
    (counter,) = db_connection \
        .execute('SELECT count(*) FROM notes WHERE text=?', (text,)) \
        .fetchone()

    return bool(counter)
