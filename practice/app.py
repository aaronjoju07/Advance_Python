from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

def create_users_table():
    con = sql.connect('db_web.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    UID INTEGER PRIMARY KEY AUTOINCREMENT,
                    UNAME TEXT,
                    CONTACT TEXT
                    )''')
    con.commit()
    con.close()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        create_users_table()  # Ensure the 'users' table exists

        con = sql.connect('db_web.db')
        cur = con.cursor()

        # Fetch data before closing the connection
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()

        con.close()
        return render_template('index.html', datas=data)

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']

        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users(UNAME, CONTACT) VALUES (?, ?)", (uname, contact))
        con.commit()
        flash('User Added', 'success')
        return redirect(url_for("index"))

    return render_template("add.html")

if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\nZCld231EoP9H]t0sBNaI'
    app.run(debug=True, port=8000)
