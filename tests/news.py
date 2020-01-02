import time
import requests
import unittest
import peewee
import hashlib

from models import zomic as db
from utils.ewt import ewt_sign


def clean():
    db.NewsletterTelegram.delete().execute()
    db.NewsletterEmail.delete().execute()
    db.User.delete().where(db.User.community_id == "test1234").execute()

    try:
        db.User.create(id="0x" + hashlib.sha256("news@email.com".encode()).hexdigest(),
                           community_id="test1234",
                           level=0,
                           wallet="0x0aa704E5c55792698c8f72418d35Af2C6f521caa",
                           permission="master")
    except peewee.IntegrityError:
        pass


subscribe_url = 'http://localhost:5000/news/subscribe'
unsubscribe_url = 'http://localhost:5000/news/unsubscribe'
exp_ok = int(time.time() + 100000)
exp_ko = int(time.time() - 100000)

base_header = {}  # {"content-type": "application/json"}
base_args = {"community_id": "test1234",
             "iss": "0x0aa704E5c55792698c8f72418d35Af2C6f521caa"}

args = {**base_args, "receive_by": "telegram", "chat_id": 1234, "exp": exp_ok}
headers = {**base_header, "Authorization": "Bearer {}".format(ewt_sign("test", args))}

args_ko = {**base_args, "receive_by": "telegram", "chat_id": 1234, "exp": exp_ko}
headers_ko = {**base_header, "Authorization": "Bearer {}".format(ewt_sign("test", args_ko))}

args2 = {**base_args, "receive_by": "email", "email": "email@email.com", "exp": exp_ok}
headers2 = {**base_header, "Authorization": "Bearer {}".format(ewt_sign("test", args2))}


class TestNews(unittest.TestCase):
    def test_00_args_missing(self):
        clean()
        res = requests.get(subscribe_url, params=base_args, headers=headers)
        self.assertEqual(res.status_code, 400)

    def test_01_expired(self):
        res = requests.get(subscribe_url, params=args_ko, headers=headers_ko)
        self.assertEqual(res.status_code, 400)

    def test_02_inserted(self):
        res = requests.get(subscribe_url, params=args, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_03_duplicate(self):
        res = requests.get(subscribe_url, params=args, headers=headers)
        self.assertEqual(res.status_code, 409)

    def test_04_expired(self):
        res = requests.get(unsubscribe_url, params=args_ko, headers=headers_ko)
        self.assertEqual(res.status_code, 400)

    def test_05_removed(self):
        res = requests.get(unsubscribe_url, params=args, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_06_ewt_error(self):
        res = requests.get(subscribe_url, params=args, headers=headers_ko)
        self.assertEqual(res.status_code, 401)

    def test_07_ewt_wrong(self):
        res = requests.get(subscribe_url, params=args, headers=headers_ko)
        self.assertEqual(res.status_code, 401)

    def test_08_inserted(self):
        res = requests.get(subscribe_url, params=args2, headers=headers2)
        self.assertEqual(res.status_code, 200)

    def test_09_duplicate(self):
        res = requests.get(subscribe_url, params=args2, headers=headers2)
        self.assertEqual(res.status_code, 409)

    def test_10_removed(self):
        res = requests.get(unsubscribe_url, params=args2, headers=headers2)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
