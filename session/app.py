from flask import Flask, jsonify,redirect,render_template,request,url_for,flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if  username != 'admin' or password != 'admin':
            error = 'invalid username or password!!'
        else:
            flash('login successful!!')
            return redirect(url_for('index'))
    return  render_template('login.html',error=error)

if __name__ == '__main__':
    app.run(debug=True,port=8001)