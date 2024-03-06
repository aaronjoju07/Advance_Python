import sqlite3 as sql

con = sql.connect('db_web.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS  inventory")
sql = '''CREATE TABLE "inventory" (
    "ID"   INTEGER PRIMARY KEY AUTOINCREMENT,
    "INAME" TEXT,
    "COUNT" TEXT) '''
cur.execute(sql)
con.commit()
con.close()