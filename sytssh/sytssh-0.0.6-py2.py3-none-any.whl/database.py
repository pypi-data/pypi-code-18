import sqlite3

con = sqlite3.connect('/tmp/sytssh.db')

con.isolation_level = 'EXCLUSIVE'
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS control (instance INTEGER, time TEXT)")

def execute(command, args=[]):
    return cur.execute(command, args)
