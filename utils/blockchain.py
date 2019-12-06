from os.path import join
from web3 import Web3, HTTPProvider
from eth_account.messages import defunct_hash_message
from eth_account import Account
from settings import KEYSTORE_PATH, WEB3_PROVIDER, DEPLOY_GAS_LIMIT,\
    DEFAULT_GAS_LIMIT, DEFAULT_GAS_PRICE

WEB3 = Web3(HTTPProvider(WEB3_PROVIDER))


def read_keystore(wallet):
    with open(join(KEYSTORE_PATH, wallet[2:].lower()), "r") as f:
        keystore = f.read()
    return keystore


def decrypt_keystore(keystore, password):
    return Account.decrypt(keystore.replace("'", '"'), password).hex()


def encrypt_privkey(private_key, password):
    return Account.encrypt(private_key, password)


def get_account(wallet, password, private_key=None):
    if not private_key:
        private_key = decrypt_keystore(read_keystore(wallet), password)
    return WEB3.eth.account.from_key(private_key)  # .privateKeyToAccount(private_key)


def launch_tx(transaction, private_key):
    signed_txn = WEB3.eth.account.signTransaction(transaction, private_key=private_key)
    return WEB3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()


def get_receipt(txid):
    return WEB3.eth.waitForTransactionReceipt(txid)


def send_eth(account, to, amount, gas_price=1):
    transaction = {
        'to': to,
        'from': account.address,
        'value': Web3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': Web3.toWei(gas_price, 'gwei'),
        'nonce': WEB3.eth.getTransactionCount(account.address)
        }
    return launch_tx(transaction, account.privateKey.hex())


def sign(account, message):
    message_hash = defunct_hash_message(text=message)
    return WEB3.eth.account.signHash(message_hash, account.privateKey).signature.hex()


def verify(wallet, message, signature):
    message_hash = defunct_hash_message(text=message)
    signer = WEB3.eth.account.recoverHash(message_hash,
                                          signature=bytes.fromhex(signature[2:]))
    return signer.lower() == wallet.lower()


class Contract:
    def __init__(self, abi_file, contract_address=False,
                 gas_price=DEFAULT_GAS_PRICE, gas=DEFAULT_GAS_LIMIT):
        with open(abi_file, "r") as f:
            self.abi = f.read()
        self.gas_price = Web3.toWei(gas_price, "gwei")
        self.gas = gas if contract_address else DEPLOY_GAS_LIMIT
        if contract_address:
            self.contract = WEB3.eth.contract(
                address=contract_address,
                abi=self.abi
            )

    def deploy(self, account, bytecode_file):
        with open(bytecode_file, "r") as f:
            bytecode = f.read()

        contract = WEB3.eth.contract(abi=self.abi, bytecode=bytecode)

        transaction = contract.constructor().buildTransaction({
            "gas": self.gas,
            "gasPrice": self.gas_price,
            "nonce": WEB3.eth.getTransactionCount(account.address)
        })
        return launch_tx(transaction, account.privateKey)

    def write(self, func, account, *args):
        transaction = self.contract.functions.__dict__[func](*args).buildTransaction({
            "gas": self.gas,
            "gasPrice": self.gas_price,
            "nonce": WEB3.eth.getTransactionCount(account.address)
        })
        return launch_tx(transaction, account.privateKey)

    def read(self, func, *args):
        return self.contract.functions.__dict__[func](*args).call()
