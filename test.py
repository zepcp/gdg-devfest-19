import argparse
from utils.blockchain import Contract, get_account, decrypt_keystore, read_keystore, sign, verify
from utils.types import string_to_bytes, string_to_unixtimestamp
from settings import BALLOT_ADDRESS, BALLOT_ABI, DATE, PROOFS_ABI, PROOFS_BYTECODE, PROOFS_ADDRESS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    args = parser.parse_args()

    # proofs = Contract(PROOFS_ABI).deploy(get_account(args.wallet,args.password), PROOFS_BYTECODE)

    ballot = Contract(BALLOT_ABI, BALLOT_ADDRESS)
    proofs = Contract(PROOFS_ABI, PROOFS_ADDRESS)

    print(proofs.read("owner"))
    print(proofs.read("passed", "test"))
    print(proofs.read("proofHash", "test"))
    print(proofs.read("votesInFavor", "test"))
    print(proofs.read("votesAgainst", "test"))

    # print(ballot.read("owner"))
    # print(ballot.read('eligible', '0x66B655a4CE711F00b570f9801c498071e9A15045'))
    # print(ballot.read('voterData', '0x66B655a4CE711F00b570f9801c498071e9A15045').decode("utf-8"))
    # print(ballot.read('proposalDeadline', 'test'))
    # print(ballot.read('votesInFavor', 'test'))
    # print(ballot.read('votesAgainst', 'test'))
    # print(ballot.read('voted', 'test', '0x66B655a4CE711F00b570f9801c498071e9A15045'))

    sender = get_account(args.wallet, args.password)
    # print(sender.address)

    # print(proofs.write('submitProposal', sender, 'test', True, 4, 0, string_to_bytes(PROOFS_ADDRESS)))

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

    # insert into voters(nif, wallet, telegram_id, email) values('123456789', '0x66B655a4CE711F00b570f9801c498071e9A15045', '546114127', 'zepcp@hotmail.com');
    # insert into votes(wallet, signature, proposal_id, in_favor) values('0x66B655a4CE711F00b570f9801c498071e9A15045', '0x66B655a4CE711F00b570f9801c498071e9A15045', '12345678', True);
    # insert into votes(wallet, signature, proposal_id, in_favor) values('0x66B655a4CE711F00b570f9801c498071e9A15046', '0x66B655a4CE711F00b570f9801c498071e9A15046', '12345678', True);
    # insert into votes(wallet, signature, proposal_id, in_favor) values('0x66B655a4CE711F00b570f9801c498071e9A15047', '0x66B655a4CE711F00b570f9801c498071e9A15047', '12345678', True);
    # insert into votes(wallet, signature, proposal_id, in_favor) values('0x66B655a4CE711F00b570f9801c498071e9A15048', '0x66B655a4CE711F00b570f9801c498071e9A15048', '12345678', True);
