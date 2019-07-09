from flask import Flask, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class UsersPing(Resource):

    @staticmethod
    def get():
        return {"status": "success", "message": "pong"}


api.add_resource(UsersPing, "/users/ping")
