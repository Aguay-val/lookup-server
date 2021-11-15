# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
import datetime

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
                {'emails': {'$elemMatch': {'address': { '$regex': f".*{searchstring}.*", '$options': 'i' }}}},
                {'username': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
                {'lastName': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
                {'firstName': { '$regex': f".*{searchstring}.*", '$options': 'i' }}
            ]}
            )
        else:
            datas = mongo.db.users.find()
        return self.formatUsersResult(datas)
    
    def formatUsersResult(self, datas):
        resSingleUser = {
        'message' : {
            'data' : {
            'federationId' : '',
            'name' : '',
            'email' : '',
            'address' : '',
            'website' : '',
            'twitter' : '',
            'phone' : ''
            },
            'type' : 'lookupserver-apps',
            'timestamp' : 0,
            'signer' : 'yo'
        },
            'signature' : ''
        }
        res = []
        for u in list(datas):
            resDict = resSingleUser.copy()
            resDict['message']['data']['federationId'] = f"{u['username']}@{u['nclocator']}"
            resDict['message']['data']['name'] = f"{u['firstName']}@{u['lastName']}"
            resDict['message']['data']['email'] = f"{u['emails'][0]['address']}"
            resDict['message']['timestamp'] = int(datetime.datetime.now().timestamp())
            res.append(resDict)
        return jsonify(res)
        
        
class User(Resource):
    def get(self, name):
        datas = mongo.db.users.find({'username':name})
        return self.formatUsersResult(datas)

api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
