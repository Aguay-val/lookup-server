#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return "Flask Mongo RestFul"
