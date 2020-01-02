import time
import requests
import unittest
import hashlib

from models import zomic as db
from settings import DEFAULTS
from utils.ewt import ewt_sign


def clean():
    db.Community.delete().execute()
    db.User.delete().execute()
    db.Proposal.delete().execute()
    db.Vote.delete().execute()
    db.Proof.delete().execute()


create_url = 'http://localhost:5000/write/create'
edit_url = 'http://localhost:5000/write/edit'
propose_url = 'http://localhost:5000/write/propose'
vote_url = 'http://localhost:5000/write/vote'
wallet_url = 'http://localhost:5000/write/wallet'
user_url = 'http://localhost:5000/write/user'
exp_ok = int(time.time() + 100000)
founder = "founder@email.com"
user = "email@email.com"


class TestWrite(unittest.TestCase):
    create_args = {"name": "Zomic",
                   "user_info": "email@email.com",
                   "founder": "0x" + hashlib.sha256(founder.encode()).hexdigest(),
                   "levels": 0,
                   "permissions": DEFAULTS["permissions"],
                   "submission_rate": 30,
                   "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
                   "exp": exp_ok}

    create_headers = {"Authorization": "Bearer {}".format(ewt_sign("test", create_args))}

    proposal_args = {"approval_rate": DEFAULTS["approval_rate"],
                     "title": "proposal title",
                     "description": "describe proposal",
                     "type": "Type 1",
                     "deadline": exp_ok,
                     "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
                     "exp": exp_ok}

    vote_args = {"in_favor": "YES",
                 "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
                 "exp": exp_ok}

    wallet_args = {"wallet": "0x64767925A6DF9E1ac8718AdE7b347Ea0Eb9F9d46",
                   "permission": "vote",
                   "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
                   "exp": exp_ok}

    user_args = {"user": "0x" + hashlib.sha256(user.encode()).hexdigest(),
                 "wallet": "0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A",
                 "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
                 "exp": exp_ok}

    def test_00_create(self):
        clean()
        res = requests.put(create_url, headers=self.create_headers, json=self.create_args)
        self.assertEqual(res.status_code, 201)

    def test_01_duplicate(self):
        res = requests.put(create_url, headers=self.create_headers, json=self.create_args)
        self.assertEqual(res.status_code, 409)

    def test_02_edit(self):
        args = {**self.create_args, "community_id": db.Community.get().id}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(edit_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_03_propose(self):
        args = {**self.proposal_args, "community_id": db.Community.get().id}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(propose_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_04_duplicate(self):
        args = {**self.proposal_args, "community_id": db.Community.get().id}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(propose_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 409)

    def test_05_vote(self):
        args = {**self.vote_args, "community_id": db.Community.get().id,
                "proposal_id": db.Proposal.get().id}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(vote_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_06_duplicate(self):
        args = {**self.vote_args, "community_id": db.Community.get().id,
                "proposal_id": db.Proposal.get().id}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(vote_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 409)

    def test_07_add_wallet(self):
        args = {**self.wallet_args, "community_id": db.Community.get().id, "action": "add"}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(wallet_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_08_remove_wallet(self):
        args = {**self.wallet_args, "community_id": db.Community.get().id, "action": "remove"}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(wallet_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_09_add_user(self):
        args = {**self.user_args, "community_id": db.Community.get().id, "action": "add"}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(user_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)

    def test_10_remove_user(self):
        args = {**self.user_args, "community_id": db.Community.get().id, "action": "remove"}
        headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}
        res = requests.put(user_url, headers=headers, json=args)
        self.assertEqual(res.status_code, 201)


if __name__ == '__main__':
    unittest.main()
