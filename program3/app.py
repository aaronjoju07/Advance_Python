from flask import Flask,render_template,url_for,redirect,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/register',methods = [ 'POST' ,'GET'])
def refister():
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True,port=8001)