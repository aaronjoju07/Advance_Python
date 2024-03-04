import sqlite3 as sql

con = sql.connect('db_web.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS  users")
sql = '''CREATE TABLE "users" (
    "UID"   INTEGER PRIMARY KEY AUTOINCREMENT,
    "UNAME" TEXT,
    "CONTACT" TEXT) '''
cur.execute(sql)
con.commit()
con.close()