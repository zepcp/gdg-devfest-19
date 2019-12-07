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


@api.route("/vote")
class Vote(Resource):
    @api.expect(parsers.post_vote())
    @api.response(201, "Success")
    @api.response(404, "Wallet does not exist")
    @api.response(404, "Proposal ID does not exist")
    def post(self):
        """Add New Vote"""

        parser = parsers.post_vote()
        args = parser.parse_args()

        try:
            models.Proposals.get(models.Proposals.id == args.proposal_id)

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="The provided proposal ID does not exist")
        try:
            voter = models.Voter.get(models.Voter.wallet == args.wallet)

            models.Votes.create(wallet=args.wallet, proposal_id=args.proposal_id,
                                signature=args.signature, in_favor=args.in_favor,
                                nif=voter.nif)

            return {'status': 'OK', 'message': "Vote Successfully Submitted"}, 201

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="The provided wallet does not exist")


@api.route("/new_voter")
class AddVoter(Resource):
    @api.expect(parsers.post_new_voter())
    @api.response(201, "Success")
    @api.response(409, "Voter already exists")
    def post(self):
        """Add New Voter"""

        parser = parsers.post_new_voter()
        args = parser.parse_args()

        try:
            models.Voter.get(models.Voter.nif == args.nif_hash)

            abort(code=409, error="ERROR-409", status=None,
                  message="The voter with the specified identification already exists")

        except peewee.DoesNotExist:

            models.Voter.create(nif=args.nif_hash, wallet=args.wallet,
                                telegram_id=args.telegram, email=args.email)

            return {'status': 'OK', "message": "Voter Successfully Added"}, 201


@api.route("/change_wallet/<path:nif>/<path:new_wallet>")
class ChangeWallet(Resource):
    @api.response(201, "Success")
    @api.response(404, "Voter does not exist")
    @api.response(409, "Wallet can not be the same")
    def post(self, nif, new_wallet):
        """Change Voter Wallet"""

        try:
            voter = models.Voter.get(models.Voter.nif == nif)

            if voter.wallet == new_wallet:
                abort(code=409, error="ERROR-404", status=None,
                      message="The new wallet must be different from the current one")

            voter.update(wallet=new_wallet).where(voter.nif == nif)

            return {'status': 'OK', 'message': "Wallet successfully replaced"}, 201

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="No voter found for the provided encrypted identification")


@api.route("/subscribe/<path:email>")
class SubscribeNewsletter(Resource):
    @api.response(201, "Success")
    @api.response(404, "Email does not exist")
    @api.response(409, "Voter already subscribed")
    def post(self, email):
        """Subscribe to Newsletter"""

        try:
            models.Voter.get(models.Voter.email == email)

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="Voter with the specified email not found")

        try:
            models.NewsletterEmail.get(models.NewsletterEmail.email == email)

            abort(code=404, error="ERROR-409", status=None,
                  message="Voter already subscribed subscribed")

        except peewee.DoesNotExist:
            models.NewsletterEmail.create(email=email)

            return {'status': 'OK', 'message': "Successfully Subscribed"}, 201


@api.route("/unsubscribe/<path:email>")
class UnsubscribeNewsletter(Resource):
    @api.response(201, "Success")
    @api.response(404, "Email does not exist")
    @api.response(409, "Voter not subscribed")
    def post(self, email):
        """Unsubscribe to Newsletter"""

        try:
            models.Voter.get(models.Voter.email == email)

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="Voter with the specified email not found")

        try:
            subscription = models.NewsletterEmail.get(models.NewsletterEmail.email == email)

            subscription.delete_instance()

            return {'status': 'OK', 'message': "Successfully Unsubscribed"}, 201

        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-409", status=None,
                  message="Voter is not subscribed")