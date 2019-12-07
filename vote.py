import argparse
from utils.blockchain import get_account, sign, verify, checksum
from settings import DATE

from utils.types import string_to_unixtimestamp

"""
python3 -m vote -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -l 1 -v "YES"
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

    print(signature)
    print(string_to_unixtimestamp(args.timestamp, DATE))
