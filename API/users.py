#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, jsonify, json
from flask_restful import Resource
from init import mongo, app
import copy


class Users(Resource):
    def get(self):
        # users?search=searchstring&exact=1&keys=["email"]

        searchstring = request.args.get("search")
        if len(searchstring) < app.config["SEARCH_LIMIT"]:
            return ""

        exact = True if request.args.get("exact") == "1" else False
        keys = []
        if request.args.get("keys"):
            # keys are the fields to apply search
            keys = json.loads(request.args.get("keys"))

        query = {"$or": []}
        query_fields = {
            "email": {
                "emails": {
                    "$elemMatch": {
                        "address": {"$regex": f".*{searchstring}.*", "$options": "i"}
                    }
                }
            },
            "username": {
                "username": {"$regex": f".*{searchstring}.*", "$options": "i"}
            },
            "lastName": {
                "lastName": {"$regex": f".*{searchstring}.*", "$options": "i"}
            },
            "firstName": {
                "firstName": {"$regex": f".*{searchstring}.*", "$options": "i"}
            },
        }

        if keys:
            # search only in keys' field
            for field in keys:
                try:
                    query["$or"].append(query_fields[field])
                except:
                    # Abort with error 500
                    print(f"Field '{field}' in keys not found for query")
                    return f"Field '{field}' in keys not found for query", 500
        else:
            # no keys => search in all fields
            for field in query_fields:
                query["$or"].append(query_fields[field])

        if searchstring:
            if exact:
                # returns only one user
                if "email" in keys:
                    query_one = {"emails": {"$elemMatch": {"address": searchstring}}}
                else:
                    query_one = {"username": searchstring}

                datas = mongo.db.users.find_one(query_one)
                if datas:
                    return jsonify(self.formatUsersResult([datas])[0])
                else:
                    return ""
            else:
                # returns all users found
                datas = mongo.db.users.find(query).limit(app.config["MONGO_LIMIT"])
                return jsonify(self.formatUsersResult(list(datas)))
        else:
            # returns all users
            datas = mongo.db.users.find({}).limit(app.config["MONGO_LIMIT"])
            return jsonify(self.formatUsersResult(list(datas)))

    def formatUsersResult(self, datas):
        """Returns a table of new formatted users dict

        Args:
            datas (table of dict): users table found in mongo

        Returns:
            [table of dict]: the newly formatted users table
        """
        resSingleUser = {
            "federationId": "",
            "name": {
                "value": "",
                "verified": "1",
            },
            "email": {
                "value": "",
                "verified": "1",
            },
            "address": {
                "value": "",
                "verified": "1",
            },
            "website": {
                "value": "",
                "verified": "1",
            },
            "twitter": {
                "value": "",
                "verified": "1",
            },
            "phone": {
                "value": "",
                "verified": "1",
            },
        }
        res = []
        for u in datas:
            resDict = copy.deepcopy(resSingleUser)
            resDict["federationId"] = f"{u['username']}@{u['nclocator']}"
            resDict["name"]["value"] = f"{u['firstName']} {u['lastName']}"
            resDict["email"]["value"] = f"{u['emails'][0]['address']}"
            res.append(resDict)
        return res
