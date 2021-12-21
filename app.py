# -*- coding: utf-8 -*-

from init import app
from flask_restful import Api
from API.helloWorld import HelloWorld
from API.users import Users
from API.user import User

api = Api(app)
api.add_resource(HelloWorld, "/")
api.add_resource(Users, "/users")
api.add_resource(User, "/user/<string:name>")


if __name__ == "__main__":
    app.run(debug=False, port=8080, host="0.0.0.0", threaded=True)
