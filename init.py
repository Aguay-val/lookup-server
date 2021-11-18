#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo
from os import environ

app = Flask(__name__)
print("MONGO_URI = ", environ['MONGO_URI'])
app.config["MONGO_URI"] = environ['MONGO_URI']
mongo = PyMongo(app)