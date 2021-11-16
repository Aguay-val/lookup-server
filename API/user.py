#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify
from flask_restful import Resource
import datetime
from init import mongo


class User(Resource):
    def get(self, name):
        datas = mongo.db.users.find({'username':name})
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