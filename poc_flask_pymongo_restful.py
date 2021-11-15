# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:3001/meteor"
mongo = PyMongo(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return "Flask Mongo RestFul"
        
        
class Users(Resource):
    def get(self):
        # users?search=searchstring
        searchstring = request.args.get('search')
        if searchstring:
            datas = mongo.db.users.find({'$or':[
                { 'emails': {'$elemMatch': {'address': { '$regex': f".*{searchstring}.*", '$options': 'i' }}}},
                {'username': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
                {'lastName': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
                {'firstName': { '$regex': f".*{searchstring}.*", '$options': 'i' }}
            ]}
            )
        else:
            datas = mongo.db.users.find()
        return jsonify(list(datas))
        
        
class User(Resource):
    def get(self, name):
        datas = mongo.db.users.find({'username':name})
        return jsonify(list(datas))

api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
