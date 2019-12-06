from flask import send_file, request
from flask_restplus import Namespace, Resource

api = Namespace("zomic", description="Zomic API")


@api.route("/status")
class Status(Resource):
    def get(self):
        """Health Check"""
        return {"status": "OK"}


@api.route("/ballot/<path:file>")
class Page(Resource):
    def get(self, file):
        """Html Page"""
        return send_file("/Users/josepereira/documents/gdg-devfest-19/file/"+file)


@api.route("/ballot_abi.js")
class Page(Resource):
    def get(self):
        """Html Page"""
        return send_file("/Users/josepereira/documents/gdg-devfest-19/ballot_abi.js")


@api.route("/web3.js")
class Page(Resource):
    def get(self):
        """Html Page"""
        return send_file("/Users/josepereira/documents/gdg-devfest-19/web3.min.js")
