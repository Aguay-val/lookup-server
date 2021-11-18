#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask_restful import Resource
import datetime
import copy
from init import mongo


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
            resDict = copy.deepcopy(resSingleUser)
            resDict['message']['data']['federationId'] = f"{u['username']}@{u['nclocator']}"
            resDict['message']['data']['name'] = f"{u['firstName']}@{u['lastName']}"
            resDict['message']['data']['email'] = f"{u['emails'][0]['address']}"
            resDict['message']['timestamp'] = int(datetime.datetime.now().timestamp())
            res.append(resDict)
        return jsonify(res)