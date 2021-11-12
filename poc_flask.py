# -*- coding: utf-8 -*-

import pymongo
from flask import Flask, jsonify

#init base de données
client = pymongo.MongoClient("localhost", 3001)
mydb = client["meteor"]
mycol = mydb["users"]

app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask"


#API
@app.route('/users', methods=['GET'])
def users():
    data = mycol.find()
    data2 = []
    for x in data:
        data2.append(x)
    return jsonify(data2)


@app.route('/user/<name>', methods=['GET'])
def user(name):
    data = mycol.find({'username':name})
    data2 = []
    for x in data:
        data2.append(x)
    return jsonify(data2)


if __name__ == "__main__":
    app.run(debug=True)
