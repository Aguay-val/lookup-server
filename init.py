#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:3001/meteor"
mongo = PyMongo(app)