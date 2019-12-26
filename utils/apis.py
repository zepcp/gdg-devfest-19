import json
import peewee
from http import HTTPStatus
from flask_restplus import abort

import models
from settings import WALLET, PASSWORD, DATE
from utils.ewt import ewt_validate
from utils.types import datetime_to_string
from utils.blockchain import sign, get_account


def authenticate(args):
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
            "levels": res.levels,
            "permissions": res.permissions,
            "submission_rate": res.submission_rate,
            "timestamp": datetime_to_string(res.timestamp, DATE),
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
            "deadline": datetime_to_string(res.deadline, DATE),
            "status": res.status,
            "in_favor": res.in_favor,
            "against": res.against,
            "timestamp": datetime_to_string(res.timestamp, DATE),
            "wallet": res.wallet,
            "signature": res.signature,
            }


def get_user(res):
    return {"community_id": res.community_id,
            "id": res.id,
            "level": res.level,
            }


def get_vote(res):
    return {"community_id": res.community_id,
            "proposal_id": res.proposal_id,
            "in_favor": res.in_favor,
            "timestamp": datetime_to_string(res.timestamp, DATE),
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
            "db_ts": datetime_to_string(res.db_ts, DATE),
            }


def get_wallet(res):
    return {"community_id": res.community_id,
            "id": res.id,
            "permission": res.permission,
            "level": res.level,
            }


def get_all(function, res, error_message):
    response = []
    for each in res:
        response.append(function(each))
    if response or not error_message:
        return response
    abort(code=HTTPStatus.NOT_FOUND.value,
          error="ERROR-404", message=error_message)


def get_proofs_db(community_id, proof_type, error_message, user=None, level=None, wallet=None):
    res = models.Proof.select().where(
        models.Proof.type == proof_type if proof_type else True,
        models.Proof.community_id == community_id,
        models.Proof.user == user if user else True,
        models.Proof.level == level if level else True,
        models.Proof.wallet == wallet if wallet else True,
    ).execute()
    return get_all(get_proof, res, error_message)


def get_users_db(community_id, error_message, level=None):
    res = models.User.select().distinct(models.User.id).where(
        models.User.community_id == community_id,
        models.User.active,
        models.User.level >= level if level else True
    ).execute()
    return get_all(get_user, res, error_message)


def get_user_db(community_id, user, suppress=False):
    try:
        user = models.User.get(models.User.community_id == community_id,
                               models.User.id == user,
                               models.User.active)
        return get_user(user)
    except peewee.DoesNotExist:
        if not suppress:
            abort(code=HTTPStatus.FORBIDDEN.value,
                  error="ERROR-403", message="Not a Community User")
    return None


def get_wallet_db(community_id, wallet, active=True):
    try:
        user = models.User.get(models.User.community_id == community_id,
                               models.User.wallet == wallet,
                               models.User.active if active else True)
        return get_wallet(user)
    except peewee.DoesNotExist:
        abort(code=HTTPStatus.FORBIDDEN.value,
              error="ERROR-403", message="Not a Community Wallet")


def ack_proof(community_id, type, payload, signature, user=None, level=None, wallet=None):
    ack = sign(get_account(WALLET, PASSWORD), payload)
    models.Proof.create(community_id=community_id,
                        type=type,
                        user=user,
                        level=level,
                        wallet=wallet,
                        payload=payload,
                        signature=signature,
                        ack=ack)
    return ack


def add_user(community_id, user, level, wallet, permission):
    try:
        models.User.create(id=user,
                           community_id=community_id,
                           level=level,
                           wallet=wallet,
                           permission=permission)
    except peewee.IntegrityError:
        models.db.close()
        abort(code=HTTPStatus.CONFLICT.value,
              error="ERROR-409", message="User Already Exists")


def remove_user(community_id, user):
    models.User.update(active=False).where(
        models.User.community_id == community_id,
        models.User.id == user).execute()


def get_current_level(community_id, args):
    user = get_user_db(community_id, args.user, True)
    return user["level"] if user \
        else models.Community.get(models.Community.id == args.community_id).levels


def get_ongoing_requests(community_id, args):
    level = get_current_level(community_id, args)
    return get_proofs_db(community_id, args.action+"_user", None,
                         args.user, level, args.wallet)


def get_permissions(community_id, action):
    permissions = models.Community.get(models.Community.id == community_id).permissions
    needed_percentage = json.loads(permissions.replace("'", '"'))[action]
    for who_is_allowed in needed_percentage:
        return who_is_allowed, needed_percentage[who_is_allowed]


def last_request(community_id, wallet, args):
    who_is_allowed, needed_percentage = get_permissions(community_id, args.action)
    current_level = get_current_level(community_id, args)

    required_level = 0 if who_is_allowed == "top" else\
        current_level+1 if who_is_allowed == "above" else\
        current_level if who_is_allowed == "same" else None

    if required_level and required_level > wallet["level"] != 0:
        abort(code=HTTPStatus.FORBIDDEN.value,
              error="ERROR-403", message="Action Not Allowed")

    requests = len(get_ongoing_requests(community_id, args))
    users = len(get_users_db(community_id, None, required_level))

    return requests >= users * needed_percentage / 100
