from flask import send_file, request
from flask_restplus import Namespace, Resource
from flask_restplus import inputs, reqparse

from utils import type

api = Namespace("zomic", description="Zomic API")


def get_parser_upload():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url",
        type=type.email,
        help="Direct APK download URL",
    )
    parser.add_argument(
        "priority",
        type=str.upper,
        choices=["YES", "NO"],
        default="YES",
        help="Priority of the associated Jira issue"
    )


@api.route("/status")
class Status(Resource):
    def get(self):
        """Health Check"""
        return {"status": "OK"}


@api.route("/upload")
class Upload(Resource):
    @api.expect(get_parser_upload())
    @api.marshal_with(api, code=201, description="Successfully uploaded")
    @api.response(400, "Bad request")
    @api.response(401, "Unauthorized")
    def post(self):
        """Upload an app by file or URL for migration of its IAB system"""

        return "", 201


@api.route("/ballot/<path:file>")
class Page(Resource):
    def get(self, file):
        """Html Page"""
        return send_file("/Users/josepereira/documents/gdg-devfest-19/"+file)
