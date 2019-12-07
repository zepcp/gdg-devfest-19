import requests
import argparse
from utils.blockchain import get_account, sign, checksum

"""
python3 -m modify_key -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -n "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46"
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    parser.add_argument("--new_wallet", '-n', type=str, help="New Wallet Address")
    args = parser.parse_args()

    sender = get_account(checksum(args.wallet), args.password)

    signature = sign(sender, str(checksum(args.new_wallet)))

    #print(signature)
    #print(checksum(args.new_wallet))


    res = requests.post("http://localhost:5000/zomic/user/modify_key",
                        params={
                            "old_wallet": args.wallet,
                            "new_wallet": args.new_wallet,
                            "signature": signature,
                        })

    print(res.status_code)
    print(res.json())
