from flask import Flask, jsonify

app = Flask(__name__)
# Define a simple endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    response = {'message': 'Hello, this is a sample Flask API!'}
    return jsonify(response)

def about():
    return 'This isn\'t about me!!'
app.add_url_rule("/about","about",about)

if __name__ == '__main__':
    app.run(debug=True)
