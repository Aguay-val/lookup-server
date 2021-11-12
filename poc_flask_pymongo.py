# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:3001/meteor"
mongo = PyMongo(app)

@app.route("/")
def hello():
    return "Flask PyMongo"


@app.route('/users', methods=['GET'])
def users():
    datas = mongo.db.users.find()
    return jsonify(list(datas))


@app.route('/user/<name>', methods=['GET'])
def user(name):
    datas = mongo.db.users.find({'username':name})
    return jsonify(list(datas))


if __name__ == "__main__":
    app.run(debug=True)
