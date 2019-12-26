import re
import time

from settings import ACTIONS
from web3 import Web3


def is_timestamp(my_timestamp):
    try:
        return int(my_timestamp) >= time.time()
    except ValueError:
        return False


def is_email(my_email):
    return re.fullmatch(r"[a-zA-Z0-9_.+-]{1,64}"
                        r"@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
                        my_email) is not None and len(my_email) <= 320


def is_wallet(my_wallet):
    return re.fullmatch(r"0x[0-9a-f]{40}", my_wallet.lower()) is not None


def is_hash(my_hash):
    return re.fullmatch(r"0x[0-9a-f]{64}", my_hash.lower()) is not None


def is_signature(my_signature):
    return re.fullmatch(r"0x[0-9a-f]{130}", my_signature.lower()) is not None


def is_telegram_token(my_token):
    return re.fullmatch(r"[0-9]{9}:[0-9a-z_]{35}", my_token.lower()) is not None


def is_id(my_id):
    return re.fullmatch(r"[0-9a-z]{8}", my_id.lower()) is not None


def is_action(my_action):
    return True if my_action.lower() in ACTIONS else None


def is_ewt(my_ewt):
    return True if len(my_ewt.split(".")) == 3 else None


def is_approval_rate(my_rate):
    try:
        return 0 < int(my_rate) <= 100
    except ValueError:
        return False


def timestamp(value):
    if is_timestamp(value):
        return int(value)
    else:
        raise ValueError("Not a valid timestamp")


def email(value):
    if is_email(value):
        username, domain = value.split("@")
        return "@".join([username, domain.lower()])
    else:
        raise ValueError("Not an email address")


def wallet(value):
    if is_wallet(value):
        return Web3.toChecksumAddress(value)
    else:
        raise ValueError("Not a valid wallet address")


def user(value):
    if is_hash(value):
        return value
    else:
        raise ValueError("Not a valid user")


def transaction(value):
    if is_hash(value):
        return value
    else:
        raise ValueError("Not a valid transaction")


def signature(value):
    if is_signature(value):
        return value
    else:
        raise ValueError("Not a valid signature")


def telegram_token(value):
    if is_telegram_token(value):
        return value
    else:
        raise ValueError("Not a valid telegram token")


def community_id(value):
    if is_id(value):
        return value
    else:
        raise ValueError("Not a valid community ID")


def proposal_id(value):
    if is_id(value):
        return value
    else:
        raise ValueError("Not a valid proposal ID")


def action(value):
    if is_action(value):
        return value.lower()
    else:
        raise ValueError("Not a valid proposal")


def ewt(value):
    if is_ewt(value):
        return value
    else:
        raise ValueError("Not a valid EWT")


def approval_rate(value):
    if is_approval_rate(value):
        return value
    else:
        raise ValueError("Not a valid Approval Rate")
