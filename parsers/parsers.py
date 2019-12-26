from flask_restplus import reqparse

from settings import DEFAULTS, ACTIONS, WALLET_PERMISSIONS,\
    NEWS_BY, VOTE_OPTIONS, PROOF_TYPES
from parsers import types


def add_authentication(parser, location):
    parser.add_argument(
        "exp",
        location=location,
        type=types.timestamp,
        required=True,
        help="Expiration Timestamp"
    )
    parser.add_argument(
        "iss",
        location=location,
        type=types.wallet,
        required=True,
        help="Authenticated Issuer"
    )
    parser.add_argument(
        "Authorization",
        location="headers",
        type=types.ewt,
        required=True,
        help="EWT Authentication"
    )
    return parser


def parse_create():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        location="json",
        type=str,
        required=True,
        help="Community Name"
    )
    parser.add_argument(
        "user_info",
        location="json",
        type=str,
        required=True,
        help="Required User Info"
    )
    parser.add_argument(
        "founder",
        location="json",
        type=types.user,
        required=True,
        help="Founder ID"
    )
    parser.add_argument(
        "levels",
        location="json",
        type=int,
        required=True,
        default=0,
        help="Community Levels"
    )
    parser.add_argument(
        "permissions",
        location="json",
        type=str,
        required=True,
        default=DEFAULTS["permissions"],
        help="Community Permissions"
    )
    parser.add_argument(
        "telegram_token",
        location="json",
        type=types.telegram_token,
        required=False,
        help="Telegram Bot Token"
    )
    parser.add_argument(
        "submission_rate",
        location="json",
        type=int,
        required=True,
        default=30,
        help="Blockchain Submission Rate"
    )
    return add_authentication(parser, "json")


def parse_edit():
    parser = parse_create()
    parser.add_argument(
        "community_id",
        location="json",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    return parser


def parse_propose():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="json",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "approval_rate",
        location="json",
        type=types.approval_rate,
        required=True,
        default=DEFAULTS["approval_rate"],
        help="Required approval rate to pass"
    )
    parser.add_argument(
        "title",
        location="json",
        type=str,
        required=True,
        help="Proposal Title"
    )
    parser.add_argument(
        "description",
        location="json",
        type=str,
        required=True,
        help="Proposal Description"
    )
    parser.add_argument(
        "type",
        location="json",
        type=str,
        required=True,
        help="Proposal Type"
    )
    parser.add_argument(
        "deadline",
        location="json",
        type=types.timestamp,
        required=True,
        help="Deadline to submit a vote"
    )
    return add_authentication(parser, "json")


def parse_vote():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="json",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "proposal_id",
        location="json",
        type=types.proposal_id,
        required=False,
        help="Proposal ID"
    )
    parser.add_argument(
        "in_favor",
        location="json",
        choices=list(VOTE_OPTIONS),
        required=False,
        help="Your Vote"
    )
    return add_authentication(parser, "json")


def parse_wallets():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="json",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "action",
        location="json",
        choices=list(ACTIONS),
        required=True,
        help="Action to perform"
    )
    parser.add_argument(
        "wallet",
        location="json",
        type=types.wallet,
        required=True,
        help="User wallet"
    )
    parser.add_argument(
        "permission",
        location="json",
        choices=list(WALLET_PERMISSIONS),
        default="vote",
        required=True,
        help="Wallet Permissions"
    )
    return add_authentication(parser, "json")


def parse_users():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="json",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "action",
        location="json",
        choices=list(ACTIONS),
        required=True,
        help="Action to perform"
    )
    parser.add_argument(
        "user",
        location="json",
        type=types.user,
        required=True,
        help="Affected user"
    )
    parser.add_argument(
        "wallet",
        location="json",
        type=types.wallet,
        required=False,
        help="User wallet"
    )
    return add_authentication(parser, "json")


def parse_reads():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="args",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "proposal_id",
        location="args",
        type=types.proposal_id,
        required=False,
        help="Proposal ID"
    )
    return add_authentication(parser, "args")


def parse_audits():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id",
        location="args",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "type",
        location="args",
        choices=list(PROOF_TYPES),
        required=False,
        help="Proof Type"
    )
    return add_authentication(parser, "args")


def parse_news():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "receive_by",
        location="args",
        choices=list(NEWS_BY),
        required=True,
        help="Receive Method",
    )
    parser.add_argument(
        "community_id",
        location="args",
        type=types.community_id,
        required=True,
        help="Community ID"
    )
    parser.add_argument(
        "email",
        location="args",
        type=types.email,
        required=False,
        help="Receiver Email"
    )
    parser.add_argument(
        "chat_id",
        location="args",
        type=int,
        required=False,
        help="Telegram chat ID"
    )
    return add_authentication(parser, "args")
