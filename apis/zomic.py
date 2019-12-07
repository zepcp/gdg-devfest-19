from flask import send_file, request
from flask_restplus import Namespace, Resource, inputs, reqparse
from parsers import parsers
from db_queries import queries
import models

api = Namespace("zomic", description="Zomic API")


@api.route("/status")
class Status(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        return {'status': 'OK'}


@api.route("/upload")
class Upload(Resource):
    @api.expect(parsers.get_parser_upload())
    @api.response(400, "Bad request")
    @api.response(401, "Unauthorized")
    def post(self):
        """Upload an app by file or URL for migration of its IAB system"""

        return "", 201


@api.route("/voter/<path:hash>")
class VoterInfo(Resource):
    @api.expect(parsers.get_voter_info_parser())
    def get(self, file):
        """Voter Information"""
        parser = parsers.get_voter_info_parser()
        args = parser.parse_args()

        # Check if hash is in the DB and return wrong input if not
        # Otherwise return the voter info

        try:
            voter = models.Voter.get(models.Voter.nif == args.nif_hash)
        except:
            pass
        return "", 200


@api.route("/ballot/<path:file>")
class Page(Resource):
    def get(self, file):
        """Html Page"""

        return send_file("/Users/josepereira/documents/gdg-devfest-19/web3.min.js")


@api.route("/new_voter")
class AddVoter(Resource):
    def post(self):
        """Add new_voter"""
        return {"status": "OK"}
