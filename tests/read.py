import time
import requests
import unittest

from utils.ewt import ewt_sign


url = 'http://localhost:5000/read'
exp_ok = int(time.time() + 100000)

args = {"community_id": "csAlS8JO",
        "proposal_id": "Lt1oUfkZ",
        "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
        "exp": exp_ok}

headers = {"Authorization": "Bearer {}".format(ewt_sign("test", args))}

args2 = {"community_id": "csAlS8JO",
         "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
         "exp": exp_ok}

headers2 = {"Authorization": "Bearer {}".format(ewt_sign("test", args2))}

args3 = {"community_id": "12345678",
         "proposal_id": "12345678",
         "iss": "0x8FA6967433B76a50E0653910798b0C3D7E96F4B4",
         "exp": exp_ok}

headers3 = {"Authorization": "Bearer {}".format(ewt_sign("test", args3))}


class TestRead(unittest.TestCase):
    def test_0_community(self):
        res = requests.get(url+"/community", headers=headers, params=args)
        self.assertEqual(res.status_code, 200)
        print(res.json())

    def test_1_proposal(self):
        res = requests.get(url+"/proposals", headers=headers, params=args)
        self.assertEqual(res.status_code, 200)
        print(res.json())

    def test_2_proposals(self):
        res = requests.get(url+"/proposals", headers=headers2, params=args2)
        self.assertEqual(res.status_code, 200)
        print(res.json())

    def test_3_votes(self):
        res = requests.get(url+"/votes", headers=headers, params=args)
        self.assertEqual(res.status_code, 200)
        print(res.json())

    def test_4_users(self):
        res = requests.get(url+"/users", headers=headers, params=args)
        self.assertEqual(res.status_code, 200)
        print(res.json())

    def test_5_no_community(self):
        res = requests.get(url+"/community", headers=headers3, params=args3)
        self.assertEqual(res.status_code, 404)

    def test_6_no_proposals(self):
        res = requests.get(url+"/proposals", headers=headers3, params=args3)
        self.assertEqual(res.status_code, 404)

    def test_7_no_votes(self):
        res = requests.get(url+"/votes", headers=headers3, params=args3)
        self.assertEqual(res.status_code, 404)

    def test_8_no_users(self):
        res = requests.get(url+"/users", headers=headers3, params=args3)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
