from flask import Flask
from flask_restful import Resource, Api


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world from resource"}

    def post(self):
        return {"Post": "Response comming from post request handler"}


class SectionResource(Resource):
    pass
