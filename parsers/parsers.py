from flask_restplus import reqparse, inputs

import settings
from parsers import types


def parse_newsletter():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email",
        type=types.email,
        required=True,
        help="Receiver Email"
    )
    return parser


def add_voter():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_hash",
        type=str.upper,
        required=True,
        help="Hash That Identifies User"
    )
    parser.add_argument(
        "wallet",
        type=types.wallet,
        required=True,
        help="Voter Wallet"
    )
    parser.add_argument(
        "telegram_id",
        type=int,
        required=False,
        help="Voter Telegram"
    )
    parser.add_argument(
        "email",
        type=types.email,
        required=False,
        help="Voter Email"
    )
    return parser


def delete_voter():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_hash",
        type=str.upper,
        required=True,
        help="Hash That Identifies User"
    )
    return parser


def get_parser_upload():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url",
        type=types.email,
        help="Direct APK download URL",
    )
    parser.add_argument(
        "priority",
        type=str.upper,
        choices=["YES", "NO"],
        default="YES",
        help="Priority of the associated Jira issue"
    )


def parser_proposal_post():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "topic",
        choices=settings.TOPICS,
        required=True,
        help="Proposal Topic",
    )
    parser.add_argument(
        "deadline",
        type=inputs.datetime_from_iso8601,
        required=True,
        help="Proposal Deadline"
    )
    parser.add_argument(
        "title",
        type=str,
        required=True,
        help="Proposal Title"
    )
    parser.add_argument(
        "description",
        type=str,
        required=True,
        help="Proposal Description"
    ),
    parser.add_argument(
        "wallet",
        type=types.wallet,
        help="Proposals Wallet"
    )

    return parser


def parser_proposal_get():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "id",
        type=int,
        required=True,
        help="Proposal ID"
    )
    return parser


def modify_voter():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "old_wallet",
        type=types.wallet,
        required=True,
        help="Old Voter Wallet"
    )
    parser.add_argument(
        "new_wallet",
        type=types.wallet,
        required=True,
        help="New Voter Wallet"
    )
    parser.add_argument(
        "signature",
        type=str,
        required=True,
        help="New Wallet Signed By Old Wallet"
    )
    return parser


def post_vote():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "proposal_id",
        type=int,
        required=True,
        help="Proposal ID"
    )
    parser.add_argument(
        "wallet",
        type=types.wallet,
        required=True,
        help="Voter Wallet"
    )
    parser.add_argument(
        "signature",
        type=str,
        required=True,
        help="New Wallet Signed By Old Wallet"
    )
    parser.add_argument(
        "in_favor",
        choices=["YES", "NO"],
        required=True,
        help="Voter Vote"
    )
    parser.add_argument(
        "timestamp",
        type=int,
        required=True,
        help="Vote Unix Timestamp"
    )

    return parser
