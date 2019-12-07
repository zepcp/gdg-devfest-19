import peewee
from datetime import datetime
from flask_restplus import Namespace, Resource, abort

import models
import settings
from parsers import parsers, types
from utils.types import datetime_to_string, datetime_to_unixtimestamp, unixtimestamp_to_datetime
from utils.blockchain import verify, checksum, get_account, sign
from safe import WALLET, PASSWORD

api = Namespace("zomic", description="Zomic API")


@api.route("/status")
class Status(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        return {'status': 'OK'}


@api.route("/newsletter/subscribe")
class SubscribeNewsletter(Resource):
    @api.expect(parsers.parse_newsletter())
    @api.response(201, "Success")
    @api.response(400, "Wrong Input: not an email")
    @api.response(409, "Email already subscribed")
    def post(self):
        """Subscribe to Newsletter"""
        parser = parsers.parse_newsletter()
        args = parser.parse_args()

        try:
            models.NewsletterEmail.get(models.NewsletterEmail.email == args.email)

            abort(code=409, error="ERROR-409", status=None,
                  message="Email already subscribed")

        except peewee.DoesNotExist:
            models.NewsletterEmail.create(email=args.email)

            return {'status': 'OK', 'message': "Successfully Subscribed"}, 201


@api.route("/newsletter/unsubscribe")
class UnsubscribeNewsletter(Resource):
    @api.expect(parsers.parse_newsletter())
    @api.response(201, "Success")
    @api.response(400, "Wrong Input: not an email")
    @api.response(409, "Email already subscribed")
    def post(self):
        """Unsubscribe to Newsletter"""
        parser = parsers.parse_newsletter()
        args = parser.parse_args()

        try:
            subscription = models.NewsletterEmail.get(models.NewsletterEmail.email == args.email)

            subscription.delete_instance()

            return {'status': 'OK', 'message': "Successfully Unsubscribed"}, 201

        except peewee.DoesNotExist:
            abort(code=409, error="ERROR-409", status=None,
                  message="Email is not subscribed")


@api.route("/proposal/insert")
class ProposalInsert(Resource):
    @api.expect(parsers.parser_proposal_post())
    @api.response(400, "Bad request")
    @api.response(401, "Unauthorized")
    def post(self):
        args = parsers.parser_proposal_post().parse_args()

        if args.deadline < datetime.utcnow():
            abort(code=400, error="ERROR-400", status=None,
                  message="Deadline Already Passed")

        try:
            models.Proposals.create(deadline=args.deadline,
                                    title=args.title,
                                    topic=args.topic,
                                    description=args.description,
                                    status="Aberta",
                                    wallet=args.wallet)
        except:
            models.db.close()
            abort(code=409, error="ERROR-409", status=None,
                  message="Proposal In Conflict With Existing Proposal")

        return "Your proposal was successfully submitted!", 201


@api.route("/proposal/details")
class ProposalDetails(Resource):
    @api.expect(parsers.parser_proposal_get())
    @api.response(400, "Bad request")
    @api.response(401, "Unauthorized")
    def get(self):
        try:
            args = parsers.parser_proposal_get().parse_args()

            proposal = models.Proposals.get(models.Proposals.id == args.id)

            return {
                "title": proposal.title,
                "description": proposal.description,
                "wallet": proposal.wallet,
                "status": proposal.status,
                "deadline": datetime_to_string(proposal.deadline, settings.TIMESTAMP),
                "topic": proposal.topic
            }, 200

        except peewee.DoesNotExist:
            abort(code=409, error="ERROR-409", status=None,
                  message="Proposal Does Not Exist")


@api.route("/proposal/listall")
class ProposalListAll(Resource):
    @api.response(400, "Bad request")
    @api.response(401, "Unauthorized")
    def get(self):
        proposals = models.Proposals.select().execute()

        response = []
        for proposal in proposals:
            response.append({
                "id": proposal.id,
                "title": proposal.title,
                "description": proposal.description,
                "wallet": proposal.wallet,
                "status": proposal.status,
                "deadline": datetime_to_string(proposal.deadline, settings.TIMESTAMP),
                "topic": proposal.topic
            })

        return response, 200


@api.route("/voter/add")
class AddVoter(Resource):
    @api.expect(parsers.add_voter())
    @api.response(201, "Success")
    @api.response(409, "Voter already exists")
    def post(self):
        """Add New Voter"""

        parser = parsers.add_voter()
        args = parser.parse_args()

        try:
            models.Voters.create(user_hash=args.user_hash, wallet=args.wallet,
                                telegram_id=args.telegram_id, email=args.email)

            return {'status': 'OK', "message": "Voter Successfully Added"}, 201
        except:
            models.db.close()
            abort(code=409, error="ERROR-409", status=None,
                  message="Voter already exists")


@api.route("/voter/delete")
class AddVoter(Resource):
    @api.expect(parsers.delete_voter())
    @api.response(201, "Success")
    @api.response(409, "Voter already exists")
    def post(self):
        """Delete Voter"""
        parser = parsers.delete_voter()
        args = parser.parse_args()

        try:
            subscription = models.Voters.get(models.Voters.user_hash == args.user_hash)

            subscription.delete_instance()

            return {'status': 'OK', 'message': "Voter Successfully Deleted"}, 201

        except peewee.DoesNotExist:
            abort(code=409, error="ERROR-409", status=None,
                  message="Voter already deleted")


@api.route("/user/modify_key")
class ModifyVoter(Resource):
    @api.expect(parsers.modify_voter())
    @api.response(200, "Success")
    @api.response(401, "Unauthorized")
    @api.response(404, "User Not Found")
    def get(self):
        """Modify Voter Information"""
        parser = parsers.modify_voter()
        args = parser.parse_args()

        try:
            if not verify(checksum(args.old_wallet), checksum(args.new_wallet), args.signature):
                abort(code=401, error="ERROR-401", status=None,
                      message="Unauthorized Access")

            try:
                models.Voters.update(wallet=args.new_wallet).where(models.Voters.wallet == args.old_wallet
                                                                   ).execute()

                return {'status': 'OK', "message": "Voter Successfully Updated"}, 201
            except peewee.DoesNotExist:
                abort(code=404, error="ERROR-404", status=None,
                      message="Voter Not Found")

        except:
            abort(code=401, error="ERROR-401", status=None,
                  message="Unauthorized Access")


@api.route("/user/vote")
class Vote(Resource):
    @api.expect(parsers.post_vote())
    @api.response(201, "Success")
    @api.response(401, "Unauthorized")
    @api.response(404, "User Not Found")
    @api.response(404, "Proposal Not Found Or Not Available")
    @api.response(409, "User Already Voted")
    @api.response(409, "Timestamp Cant Be In The Future")
    def post(self):
        """Add New Vote"""
        parser = parsers.post_vote()
        args = parser.parse_args()

        vote = {"proposal": args.proposal_id,
                "wallet": checksum(args.wallet),
                "vote": args.in_favor,
                "timestamp": args.timestamp}

        if not verify(checksum(args.wallet), str(vote), args.signature):
            abort(code=401, error="ERROR-401", status=None,
                  message="Unauthorized Access")

        if args.timestamp > datetime_to_unixtimestamp(datetime.utcnow()):
            abort(code=409, error="ERROR-409", status=None,
                  message="Timestamp Cant Be In The Future")

        try:
            models.Proposals.get(models.Proposals.id == args.proposal_id,
                                 models.Proposals.deadline > unixtimestamp_to_datetime(args.timestamp))
        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="Proposal Not Found Or Not Available")

        try:
            voter = models.Voters.get(models.Voters.wallet == args.wallet)
        except peewee.DoesNotExist:
            abort(code=404, error="ERROR-404", status=None,
                  message="User Not Found")

        try:
            models.Votes.get(models.Votes.user_hash == voter.user_hash)
        except peewee.DoesNotExist:
            abort(code=409, error="ERROR-409", status=None,
                  message="User Already Voted")

        models.Votes.create(proposal_id=args.proposal_id,
                            user_hash=voter.user_hash,
                            wallet=args.wallet,
                            signature=args.signature,
                            in_favor=True if args.in_favor == "YES" else False,
                            timestamp=args.timestamp)

        receipt = sign(get_account(WALLET, PASSWORD), str(vote))

        return {"validator": WALLET,
                "receipt": receipt,
                "message": "Vote Successfully Submitted"}, 201
