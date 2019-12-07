import functools

from sha3 import keccak_256

import models


def compute(hash_list):
    while True:
        hash1 = []
        pairs = [hash_list[k:k + 2] for k in range(0, len(hash_list), 2)]
        for pair in pairs:
            pair_concat = str(functools.reduce(lambda x, y: str(x) + str(y), pair))
            new_hash = '0x' + keccak_256(pair_concat.encode("utf8")).hexdigest()
            hash1.append(new_hash)
        if len(hash1) == 1:
            break
        hash_list = hash1
    return hash1[0]


def get_submission_info(proposal_id):
    votes = models.Votes.select().where(models.Votes.proposal_id == proposal_id).execute()
    hash_list = []
    in_favor, against = 0, 0
    for x in votes:
        hash_list.append(x.signature)
        if x.in_favor:
            in_favor += 1
        else:
            against += 1
    passed = True if in_favor > against else False
    return passed, in_favor, against, compute(hash_list)
