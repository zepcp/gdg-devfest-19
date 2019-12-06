import argparse
from utils.blockchain import Contract, get_account, decrypt_keystore, read_keystore, sign, verify
from utils.types import string_to_bytes, string_to_unixtimestamp
from settings import BALLOT_ADDRESS, BALLOT_ABI, DATE

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    args = parser.parse_args()

    ballot = Contract(BALLOT_ABI, BALLOT_ADDRESS)

    # print(ballot.read("owner"))
    # print(ballot.read('eligible', '0x66B655a4CE711F00b570f9801c498071e9A15045'))
    # print(ballot.read('voterData', '0x66B655a4CE711F00b570f9801c498071e9A15045').decode("utf-8"))
    # print(ballot.read('proposalDeadline', 'test'))
    # print(ballot.read('votesInFavor', 'test'))
    # print(ballot.read('votesAgainst', 'test'))
    # print(ballot.read('voted', 'test', '0x66B655a4CE711F00b570f9801c498071e9A15045'))

    sender = get_account(args.wallet, args.password)
    # print(sender.address)

    # print(ballot.write('addVoter', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045', string_to_bytes('data')))
    # print(ballot.write('removeVoter', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045'))
    # print(ballot.write('propose', sender, 'test', string_to_unixtimestamp("2020-01-01", DATE)))
    # print(ballot.write('vote', sender, 'test', True))
    # print(ballot.write('transferOwnership', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045'))

    #signature = sign(sender, "test")
    #print(signature)

    #verified = verify(sender.address, "test", signature)
    #print(verified)

    message = {
        "proposal": "test",
        "vote": True,
        "wallet": sender.address
    }
    print(message)

    signature = sign(sender, str(message))
    print(signature)

    verified = verify(sender.address, str(message), signature)
    print(verified)

    user_data = {
        "cc": "123456789",
        "username": "baraberto",
        "wallet": sender.address
    }
    print(user_data)

    signature = sign(sender, str(user_data))
    print(signature)

    verified = verify(sender.address, str(user_data), signature)
    print(verified)
