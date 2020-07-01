import os
import re
import json
import ctypes
from ethsnarks.verifier import Proof, VerifyingKey

from ethsnarks.field import FQ
from ethsnarks.mimc import mimc_hash
from ethsnarks.utils import native_lib_path
from ethsnarks.merkletree import MerkleTree


class Miximus(object):
    def __init__(self, native_library_path, vk, pk_file=None):
        if pk_file:
            if not os.path.exists(pk_file):
                raise RuntimeError("Proving key file doesnt exist: " + pk_file)
        self._pk_file = pk_file

        if not isinstance(vk, VerifyingKey):
            if isinstance(vk, dict):
                vk = VerifyingKey.from_dict(vk)
            elif os.path.exists(vk):
                vk = VerifyingKey.from_file(vk)
            else:
                vk = VerifyingKey.from_json(vk)
        if not isinstance(vk, VerifyingKey):
            raise TypeError("Invalid vk type")
        self._vk = vk

        lib = ctypes.cdll.LoadLibrary(native_library_path)

        lib_tree_depth = lib.miximus_tree_depth
        lib_tree_depth.restype = ctypes.c_size_t
        self.tree_depth = lib_tree_depth()
        assert self.tree_depth > 0
        assert self.tree_depth <= 32

        lib_prove = lib.miximus_prove
        lib_prove.argtypes = ([ctypes.c_char_p] * 5) + [(ctypes.c_char_p * self.tree_depth)]
        lib_prove.restype = ctypes.c_char_p
        self._prove = lib_prove

        lib_prove_json = lib.miximus_prove_json
        lib_prove_json.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib_prove_json.restype = ctypes.c_char_p
        self._prove_json = lib_prove_json

        lib_verify = lib.miximus_verify
        lib_verify.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib_verify.restype = ctypes.c_bool
        self._verify = lib_verify

        lib_nullifier = lib.miximus_nullifier
        lib_nullifier.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib_nullifier.restype = ctypes.c_char_p
        self._nullifier = lib_nullifier

    def nullifier(self, secret, leaf_index):
        assert isinstance(secret, int)
        assert isinstance(leaf_index, int)
        secret = ctypes.c_char_p(str(secret).encode('ascii'))
        leaf_index = ctypes.c_char_p(str(leaf_index).encode('ascii'))
        return int(self._nullifier(secret, leaf_index))

    def prove(self, root, spend_preimage, exthash, address_bits, path, pk_file=None):
        assert isinstance(path, (list, tuple))
        assert len(path) == self.tree_depth
        if isinstance(address_bits, (tuple, list)):
            address_bits = ''.join([str(_) for _ in address_bits])
        assert re.match(r'^[01]+$', address_bits)
        assert len(address_bits) == self.tree_depth
        assert isinstance(root, int)
        assert isinstance(spend_preimage, int)
        assert isinstance(exthash, int)
        # TODO: require root, nullifier, spend_preimage and exthash are ints within curve order range

        if pk_file is None:
            pk_file = self._pk_file
        if pk_file is None:
            raise RuntimeError("No proving key file")

        args_dict = dict(
            root=hex(root),
            exthash=hex(exthash),
            secret=hex(spend_preimage),
            address=sum([(1<<i)*int(_) for i, _ in enumerate(address_bits)]),
            path=[hex(_) for _ in path]
        )
        args_json = json.dumps(args_dict).encode('ascii')
        args_json_cstr = ctypes.c_char_p(args_json)

        pk_file_cstr = ctypes.c_char_p(pk_file.encode('ascii'))

        data = self._prove_json(pk_file_cstr, args_json_cstr)
        if data is None:
            raise RuntimeError("Could not prove!")
        return Proof.from_json(data)

    def verify(self, proof):
        if not isinstance(proof, Proof):
            raise TypeError("Invalid proof type")

        vk_cstr = ctypes.c_char_p(self._vk.to_json().encode('ascii'))
        proof_cstr = ctypes.c_char_p(proof.to_json().encode('ascii'))

        return self._verify( vk_cstr, proof_cstr )


n_items = 2 << 28
tree = MerkleTree(n_items)
for n in range(0, 2):
    tree.append(int(FQ.random()))

exthash = int(FQ.random())
secret = int(FQ.random())

leaf_hash = mimc_hash([secret])
leaf_idx = tree.append(leaf_hash)
if leaf_idx != tree.index(leaf_hash):
    print('ERROR 1')

# Verify it exists in true
leaf_proof = tree.proof(leaf_idx)
if not leaf_proof.verify(tree.root):
    print('ERROR 2')

NATIVE_LIB_PATH = native_lib_path('.build/libmiximus')

VK_PATH = '.keys/miximus.vk.json'
PK_PATH = '.keys/miximus.pk.raw'

wrapper = Miximus(NATIVE_LIB_PATH, VK_PATH, PK_PATH)
tree_depth = wrapper.tree_depth
snark_proof = wrapper.prove(
    tree.root,
    secret,
    exthash,
    leaf_proof.address,
    leaf_proof.path)

if not wrapper.verify(snark_proof):
    print('ERROR 3')

wrapper.nullifier(secret, leaf_idx)
