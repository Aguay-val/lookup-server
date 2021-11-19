#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, jsonify, json
from flask_restful import Resource
import datetime
import copy
from init import mongo


class Users(Resource):
    def get(self):
        # users?search=searchstring&exact=1&keys=["email"]
        searchstring = request.args.get('search')
        exact = True if request.args.get('exact')=='1' else False
        keys=[]
        if request.args.get('keys'):
            # keys are the fields to apply search
            keys = json.loads(request.args.get('keys'))

        query = {'$or':[]}
        query_fields = {
            "email": {'emails': {'$elemMatch': {'address': { '$regex': f".*{searchstring}.*", '$options': 'i' }}}},
            "username": {'username': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
            "lastName": {'lastName': { '$regex': f".*{searchstring}.*", '$options': 'i' }},
            "firstName": {'firstName': { '$regex': f".*{searchstring}.*", '$options': 'i' }}
        }

        if keys:
            # search only in keys' field
            for field in keys:
                try:
                    query['$or'].append(query_fields[field])
                except:
                    # Abort with error 500
                    print(f"Field '{field}' in keys not found for query")
                    return f"Field '{field}' in keys not found for query", 500
        else:
            # no keys => search in all fields
            for field in query_fields:
                query['$or'].append(query_fields[field])

        if searchstring:
            datas = mongo.db.users.find(query)
        else:
            datas = mongo.db.users.find({})
            
        if exact:
            # returns only one user
            return jsonify(self.formatUsersResult(list(datas))[0])
        else:
            # returns all users found
            return jsonify(self.formatUsersResult(list(datas)))
    
    def formatUsersResult(self, datas):
        """Returns a table of new formatted users dict

        Args:
            datas (table of dict): users table found in mongo

        Returns:
            [table of dict]: the newly formatted users table
        """
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
        for u in datas:
            resDict = copy.deepcopy(resSingleUser)
            resDict['message']['data']['federationId'] = f"{u['username']}@{u['nclocator']}"
            resDict['message']['data']['name'] = f"{u['firstName']}@{u['lastName']}"
            resDict['message']['data']['email'] = f"{u['emails'][0]['address']}"
            resDict['message']['timestamp'] = int(datetime.datetime.now().timestamp())
            res.append(resDict)
        return res