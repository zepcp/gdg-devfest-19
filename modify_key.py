import argparse
from utils.blockchain import get_account, sign, checksum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    parser.add_argument("--new_wallet", '-n', type=int, help="New Wallet Address")
    args = parser.parse_args()

    sender = get_account(checksum(args.wallet), args.password)

    signature = sign(sender, str(checksum(args.new_wallet)))

    print(signature)
