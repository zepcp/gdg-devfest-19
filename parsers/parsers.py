from flask_restplus import reqparse
from parsers import types


def get_voter_info_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "nif_hash",
        type=str.upper,
        required=True,
        help="Hash That Identifies User")

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