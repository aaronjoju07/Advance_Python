from flask import Flask, jsonify,redirect,render_template,request,url_for

app = Flask(__name__)

@app.route('/index')
def show_index():
    return  render_template( 'index.html' )


@app.route('/success/<int:score>')
def show_result(score):
    res = ""
    if score >=50000:
        res = "Excellent!"
    else :
        res = "Shit"
    return  render_template( 'results.html',result = res ,amount=score)

@app.route('/submit',methods=['GET','POST'])
def show_submit():
    salary = 0 
    if request.method == 'POST':
        salary = float(request.form['salary'])
    return  redirect(url_for('show_result',score=salary))

if __name__ == '__main__':
    app.run(debug=True,port=8001)
