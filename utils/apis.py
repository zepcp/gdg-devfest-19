import json
import peewee
from http import HTTPStatus
from flask_restplus import abort

from models import zomic as db
from settings import WALLET, PASSWORD, DATE
from utils.ewt import ewt_validate
from utils.types import unixtimestamp_to_string
from utils.blockchain import sign, get_account


def authenticate(args):
    if args.iss:
        _, payload, sig = args.Authorization.split(".")
        if not ewt_validate(args, payload, sig):
            abort(code=HTTPStatus.UNAUTHORIZED.value,
                  error="ERROR-401", message="Authentication Failed")
        return payload, sig


def get_community(res):
    return {"community_id": res.id,
            "name": res.name,
            "required_info": res.required_info,
            "founder": res.founder,
            "permissions": res.permissions,
            "submission_rate": res.submission_rate,
            "timestamp": unixtimestamp_to_string(res.timestamp, DATE),
            "wallet": res.wallet,
            "signature": res.signature,
            }


def get_proposal(res):
    return {"id": res.id,
            "community_id": res.community_id,
            "approval_rate": res.approval_rate,
            "description": res.description,
            "title": res.title,
            "type": res.type,
            "deadline": unixtimestamp_to_string(res.deadline, DATE),
            "status": res.status,
            "in_favor": res.in_favor if res.status != "Open" else None,
            "against": res.against if res.status != "Open" else None,
            "timestamp": unixtimestamp_to_string(res.timestamp, DATE),
            "wallet": res.wallet,
            "signature": res.signature,
            }


def get_user(res):
    return {"community_id": res.community_id,
            "id": res.id,
            }


def get_vote(res):
    return {"community_id": res.community_id,
            "proposal_id": res.proposal_id,
            "in_favor": res.in_favor,
            "timestamp": unixtimestamp_to_string(res.timestamp, DATE),
            "wallet": res.wallet,
            "signature": res.signature,
            }


def get_proof(res):
    return {"community_id": res.community_id,
            "type": res.type,
            "payload": res.payload,
            "signature": res.signature,
            "ack": res.ack,
            "txid": res.txid,
            "db_ts": unixtimestamp_to_string(res.db_ts, DATE),
            }


def get_wallet(res):
    return {"community_id": res.community_id,
            "id": res.id,
            "admin": res.admin,
            }


def get_all(function, res, error_message):
    response = []
    for each in res:
        response.append(function(each))
    if response or not error_message:
        return response
    abort(code=HTTPStatus.NOT_FOUND.value,
          error="ERROR-404", message=error_message)


def get_community_id(res):
    try:
        return res.community_id
    except AttributeError:
        return res.id


def communities_by_wallet(wallet, error_message=None):
    res = db.User.select(db.User.community_id).distinct(db.User.community_id) \
            .where(db.User.wallet == wallet,
                   db.User.active).execute()
    return get_all(get_community_id, res, error_message)


def list_communities(wallet, error_message=None):
    res = db.Community.select(db.Community.id).distinct(db.Community.id)\
        .where((~db.Community.secret) |
               (db.Community.id in communities_by_wallet(wallet))).execute()
    return get_all(get_community_id, res, error_message)


def get_proofs_db(community_id, proof_type, error_message, user=None, wallet=None):
    res = db.Proof.select().where(
        db.Proof.type == proof_type if proof_type else True,
        db.Proof.community_id == community_id,
        db.Proof.user == user if user else True,
        db.Proof.wallet == wallet if wallet else True,
    ).execute()
    return get_all(get_proof, res, error_message)


def get_users_db(community_id, error_message):
    res = db.User.select().distinct(db.User.id).where(
        db.User.community_id == community_id if community_id else True,
        db.User.active,
    ).execute()
    return get_all(get_user, res, error_message)


def get_user_db(community_id, user, suppress=False):
    try:
        user = db.User.get(db.User.community_id == community_id,
                           db.User.id == user,
                           db.User.active)
        return get_user(user)
    except peewee.DoesNotExist:
        if not suppress:
            abort(code=HTTPStatus.FORBIDDEN.value,
                  error="ERROR-403", message="Not a Community User")
    return None


def get_wallet_db(community_id, wallet, active=True):
    try:
        user = db.User.get(db.User.community_id == community_id,
                           db.User.wallet == wallet,
                           db.User.active if active else True)
        return get_wallet(user)
    except peewee.DoesNotExist:
        abort(code=HTTPStatus.FORBIDDEN.value,
              error="ERROR-403", message="Not a Community Wallet")


def ack_proof(community_id, type, payload, signature, user=None, wallet=None):
    ack = sign(get_account(WALLET, PASSWORD), payload)
    db.Proof.create(community_id=community_id,
                    type=type,
                    user=user,
                    wallet=wallet,
                    payload=payload,
                    signature=signature,
                    ack=ack)
    return ack


def add_user(community_id, user, wallet, admin=False):
    try:
        db.User.create(id=user,
                       community_id=community_id,
                       wallet=wallet,
                       admin=admin,)
    except peewee.IntegrityError:
        db.db.close()
        abort(code=HTTPStatus.CONFLICT.value,
              error="ERROR-409", message="User Already Exists")


def remove_user(community_id, user, wallet):
    db.User.update(active=False).where(
        db.User.community_id == community_id,
        db.User.id == user if user else True,
        db.User.wallet == wallet if not user else True,
    ).execute()


def get_ongoing_requests(community_id, args):
    return get_proofs_db(community_id, args.action+"_user", None,
                         args.user, args.wallet)


def get_permissions(community_id, action):
    permissions = db.Community.get(db.Community.id == community_id).permissions
    needed_percentage = json.loads(permissions.replace("'", '"'))[action]
    for who_is_allowed in needed_percentage:
        return who_is_allowed, needed_percentage[who_is_allowed]


def last_request(community_id, wallet, args):
    who_is_allowed, needed_percentage = get_permissions(community_id, args.action)

    if who_is_allowed == "admin":
        if not get_wallet_db(community_id, wallet)["admin"]:
            abort(code=HTTPStatus.FORBIDDEN.value,
                  error="ERROR-403", message="Action Not Allowed")

    requests = len(get_ongoing_requests(community_id, args)) + 1
    users = len(get_users_db(community_id, None))

    return requests >= users * needed_percentage / 100
