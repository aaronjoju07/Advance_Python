from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        if uname == 'admin' and password == 'admin':
            flash('User Logged in', 'success')
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/index")
def index():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from inventory")
    data = cur.fetchall()
    return render_template("index.html", datas=data)

@app.route("/add_inventory", methods=['POST', 'GET'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("insert into inventory(INAME,COUNT) values (?,?)", (name, count))
        con.commit()
        flash('Item Added', 'success')
        return redirect(url_for("index"))
    return render_template("add_inventory.html")

@app.route("/edit_inventory/<string:id>", methods=['POST', 'GET'])
def edit_inventory(id):
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("update inventory set INAME=?, COUNT=? where ID=?", (name, count, id))
        con.commit()
        flash('User Updated', 'success')
        return redirect(url_for("index"))
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from inventory where ID=?", (id,))
    data = cur.fetchone()
    return render_template("edit_inventory.html", datas=data)

@app.route("/delete_user/<string:id>", methods=['GET'])
def delete_user(id):
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("delete from inventory where ID=?", (id,))
    con.commit()
    flash('Item Deleted', 'warning')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = '24ergergeq3q'
    app.run(debug=True, port=5001)
