from flask import send_file
from flask_restplus import Namespace, Resource, abort
from parsers import parsers
from db_queries import queries
import models
import peewee

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


@api.route("/voter/<path:nif>/info")
class VoterInfo(Resource):
    @api.response(200, "Success")
    @api.response(404, "Voter does not exist")
    def get(self, nif):
        """Voter Information"""

        # Check if nif_hash is in the DB and return 404 if not
        # Otherwise return the voter info

        models.db.create_tables([models.Voter], safe=True)

        try:
            voter = models.Voter.get(models.Voter.nif == nif)

            return {'nif': nif,
                    'wallet': voter.wallet,
                    'telegram': voter.telegram_id,
                    'email': voter.email}

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="No voter found for the provided encrypted identification")


@api.route("/ballot/<path:file>")
class Page(Resource):
    def get(self, file):
        """Html Page"""

        return send_file("/Users/josepereira/documents/gdg-devfest-19/web3.min.js")


@api.route("/new_voter")
class AddVoter(Resource):
    @api.expect(parsers.post_new_voter())
    @api.response(200, "Success")
    @api.response(409, "Voter already exists")
    def post(self):
        """Add New Voter"""

        parser = parsers.post_new_voter()
        args = parser.parse_args()

        models.db.create_tables([models.Voter], safe=True)

        try:
            models.Voter.get(models.Voter.nif == args.nif_hash)

            abort(code=409, error="ERROR-409", status=None,
                  message="The voter with the specified identification already exists")

        except peewee.DoesNotExist:

            models.Voter.create(nif=args.nif_hash, wallet=args.wallet,
                                telegram_id=args.telegram, email=args.email)

            return {"status": "OK"}
