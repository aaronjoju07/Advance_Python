from flask import  Flask, request,render_template,redirect,url_for,flash
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def index():
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
    cur = con.cursor()
    data = cur.fetchall()
    return render_template('index.html',datas =data)

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db.db")
        cur = con.cursor()
        cur.execute("insert into users(UNAME,CONTACT) values (?,?)",(uname,contact))
        con.commit()
        flash('User added successfully!','success')
        return redirect(url_for('index'))
    return render_template('add_user.html')
@app.route("/update/<string:uid>", methods=['GET',"POST"])
def update(uid):    
    if request.method == 'POST':
        uname = request.form['unmae']
        contact = request.form['contact']
        con = sql.connect("db.db")
        cur = con.cursor()
        cur.execute("update users SET UNAME = ? , CONTACT =? WHERE ID=?",(uname,contact,int(uid)))
        con.commit()
        flash('Data updated Successfully !','success')
        return  redirect(url_for('index'))
    con = sql.connect("db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE ID=?",(uid,))
    row = cur.fetchone()
    return render_template('edit_user.html', datas=row)

@app.route("/delete/<string:uid>",methods = ['GET'])
def delete_user(uid):
    con = sql.connect("db.db")
    cur = con.cursor()
    cur.execute("delete from users WHERE ID=?",(int(uid),))
    con.commit()
    flash('User Deleted!!','warning')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.secret_key = 'admin123123'
    app.run(debug=True,port=5001)