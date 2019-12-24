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
            "read_permissions": res.read_permissions,
            "write_permissions": res.write_permissions,
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
            "permissions": res.permissions,
            "level": res.level,
            }


def get_all(function, res, error_message):
    response = []
    for each in res:
        response.append(function(each))
    if response:
        return response
    abort(code=HTTPStatus.NOT_FOUND.value,
          error="ERROR-404", message=error_message)


def get_proofs_db(community_id, proof_type, error_message):
    res = models.Proof.select().where(
        models.Proof.type == proof_type if proof_type else True,
        models.Proof.community_id == community_id).execute()
    return get_all(get_proof, res, error_message)


def get_wallet_db(community_id, wallet, active=True):
    try:
        user = models.User.get(models.User.community_id == community_id,
                               models.User.wallet == wallet,
                               models.User.active if active else True)
        return get_wallet(user)
    except peewee.DoesNotExist:
        abort(code=HTTPStatus.FORBIDDEN.value,
              error="ERROR-403", message="Not a Community Wallet")


def ack_proof(community_id, type, payload, signature):
    ack = sign(get_account(WALLET, PASSWORD), payload)
    models.Proof.create(community_id=community_id,
                        type=type,
                        payload=payload,
                        signature=signature,
                        ack=ack)
    return ack


def add_user(community_id, user, level, wallet, permission):
    try:
        models.User.create(community_id=community_id,
                           user=user,
                           level=level,
                           wallet=wallet,
                           permission=permission)
    except peewee.IntegrityError:
        models.db.close()
        abort(code=HTTPStatus.CONFLICT.value,
              error="ERROR-409", message="User Already Exists")
