import requests
import argparse
from utils.blockchain import get_account, sign, checksum

"""
python3 -m modify_key -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -n "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46"

export MODIFY1="python3 -m modify_key -w 0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46 -p test -n 0x64767925a6df9e1ac8718ade7b347ea0eb9f9d47"
export MODIFY2="python3 -m modify_key -w 0x8fa6967433b76a50e0653910798b0c3d7e96f4b4 -p test -n 0x8fa6967433b76a50e0653910798b0c3d7e96f4b5"
export MODIFY3="python3 -m modify_key -w 0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A -p test -n 0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49B"
export MODIFY4="python3 -m modify_key -w 0x0aa704E5c55792698c8f72418d35Af2C6f521caa -p test -n 0x0aa704E5c55792698c8f72418d35Af2C6f521cab"

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
