import functools

from sha3 import keccak_256


def compute(hash_list):
    """Recursively compute a merkle tree"""
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
