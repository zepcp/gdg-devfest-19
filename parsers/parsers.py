from flask_restplus import reqparse
from parsers import types


def post_vote():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "proposal_id",
        type=str.upper,
        required=True,
        help="Proposal ID"
    )
    parser.add_argument(
        "wallet",
        type=str.upper,
        required=True,
        help="Voter Wallet"
    )
    parser.add_argument(
        "signature",
        type=str.upper,
        required=True,
        help="Voter Signed Vote"
    )
    parser.add_argument(
        "in_favor",
        choices=['YES', 'NO'],
        required=True,
        help="Voter Vote"
    )

    return parser


def post_new_voter():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "nif_hash",
        type=str.upper,
        required=True,
        help="Hash That Identifies User"
    )
    parser.add_argument(
        "wallet",
        type=str.upper,
        required=True,
        help="Voter Wallet"
    )
    parser.add_argument(
        "telegram",
        type=str.upper,
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