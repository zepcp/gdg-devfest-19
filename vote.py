import requests
import argparse
from utils.blockchain import get_account, sign, verify, checksum
from settings import DATE

from utils.types import string_to_unixtimestamp

"""
python3 -m vote -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -l 1
python3 -m vote -w "0x8fa6967433b76a50e0653910798b0c3d7e96f4b4" -p "test" -l 1
python3 -m vote -w "0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A" -p "test" -l 1
python3 -m vote -w "0x0aa704E5c55792698c8f72418d35Af2C6f521caa" -p "test" -l 1

export VOTE1="python3 -m vote -w 0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46 -p test -l "
export VOTE2="python3 -m vote -w 0x8fa6967433b76a50e0653910798b0c3d7e96f4b4 -p test -l "
export VOTE3="python3 -m vote -w 0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A -p test -l "
export VOTE4="python3 -m vote -w 0x0aa704E5c55792698c8f72418d35Af2C6f521caa -p test -l "

"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    parser.add_argument("--proposal", '-l', type=int, help="Proposal")
    parser.add_argument("--vote", '-v', type=str, help="Vote", default="YES")
    parser.add_argument("--timestamp", '-t', type=str, help="Timestamp", default="2019-12-07")
    args = parser.parse_args()

    sender = get_account(checksum(args.wallet), args.password)

    vote = {"proposal": args.proposal,
            "wallet": checksum(args.wallet),
            "vote": args.vote,
            "timestamp": string_to_unixtimestamp(args.timestamp, DATE)}

    signature = sign(sender, str(vote))
    verified = verify(sender.address, str(vote), signature)

    #print(signature)
    #print(str(vote))

    res = requests.post("http://localhost:5000/zomic/user/vote",
                        params={
                            "proposal_id": args.proposal,
                            "wallet": args.wallet,
                            "signature": signature,
                            "in_favor": args.vote,
                            "timestamp": string_to_unixtimestamp(args.timestamp, DATE)
                        })

    print(res.status_code)
    print(res.json())
