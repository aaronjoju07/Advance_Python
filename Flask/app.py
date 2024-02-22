from flask import Flask, jsonify,redirect,render_template,request,url_for

app = Flask(__name__)
# Define a simple endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    response = {'message': 'Hello, this is a sample Flask API!'}
    return jsonify(response)

def about():
    return 'This isn\'t about me!!'

app.add_url_rule("/about","about",about)

@app.route('/blog/<int:postId>')
def show_blog(postId):
    return "Showing blog post number %d" % postId

@app.route('/admin')
def admin():
    return  "Admin Page!"

@app.route('/guest/<guest>')
def show_guest(guest):
    return  "Guest page for %s" % guest
@app.route('/user/<user>')
def controlUser(user):
    if user == 'admin': return  admin()
    else :return show_guest(user)


@app.route('/index')
def show_index():
    return  render_template( 'index.html' )


@app.route('/success/<int:score>')
def show_result(score):
    res = ""
    if score >=90:
        res = "Excellent!"
    elif score>=60:
        res = "Good job!"
    elif  score>=30:
        res= "You passed!"
    else :
        res = "fail"
    return  render_template( 'results.html',result = res ,percentage=score)

@app.route('/submit',methods=['GET','POST'])
def show_submit():
    total_score = 0 
    if request.method == 'POST':
        science = float(request.form['science'])
        Maths = float(request.form['maths'])
        c=float(request.form['c'])
        data_science = float(request.form['datascience'])
        total_score = (science+Maths+c+data_science)/4
    return  redirect(url_for('show_result',score=total_score))

if __name__ == '__main__':
    app.run(debug=True,port=8001)
