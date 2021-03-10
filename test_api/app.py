import json

from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Tomorrow Dev Training</h1><p>Enjoy with Docker! version 3.0</p>"


@app.route('/api/', methods=['GET'])
def rest():
    my_dict = {}
    my_dict = {1: 'python', 2: 'docker'}
    return my_dict


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')