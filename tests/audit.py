import time
import requests
import unittest

from models import zomic as db
from settings import PROOF_TYPES
from utils.ewt import ewt_sign

db.Proof.update(community_id="test1234").execute()

url = 'http://localhost:5000/audit/proofs'
exp_ok = int(time.time() + 100000)

args = {"community_id": "test1234",
        "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
        "exp": exp_ok}

headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}


class TestAudit(unittest.TestCase):
    def test_0_proofs(self):
        res = requests.get(url, headers=headers, params=args)
        self.assertEqual(res.status_code, 200)

    def test_1_proof_by_type(self):
        for proof_type in PROOF_TYPES:
            args2 = args
            args2["type"] = proof_type
            headers2 = {"Authorization": "Bearer {}".format(ewt_sign("test", args2))}
            res = requests.get(url, headers=headers2, params=args2)
            self.assertEqual(res.status_code, 200)

    def test_2_proofs_not_found(self):
        args2 = args
        args2["community_id"] = "12345678"
        headers2 = {"Authorization": "Bearer {}".format(ewt_sign("test", args2))}
        res = requests.get(url, headers=headers2, params=args2)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
