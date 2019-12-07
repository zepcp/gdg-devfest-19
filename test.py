import argparse
from utils.blockchain import Contract, get_account, sign, verify
from settings import BALLOT_ADDRESS, BALLOT_ABI, PROOFS_ABI, PROOFS_ADDRESS, DATE

from utils.types import string_to_unixtimestamp

"""
python3 -m vote -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -l 1
python3 -m vote -w "0x8fa6967433b76a50e0653910798b0c3d7e96f4b4" -p "test" -l 1
python3 -m vote -w "0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A" -p "test" -l 1
python3 -m vote -w "0x0aa704E5c55792698c8f72418d35Af2C6f521caa" -p "test" -l 1

python3 -m modify_key -w "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46" -p "test" -n "0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46"

"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", '-w', type=str, help="Wallet Address")
    parser.add_argument("--password", '-p', type=str, help="Password to unlock your keystore")
    args = parser.parse_args()

    #subject = "Test Email"
    #message = "Test Message"
    #to_address = "zepcp@hotmail.com"
    #Mail(SMTP_HOST, SMTP_USER, SMTP_PASS).send_mail(subject, message, to_address)

    #Bot().send(546114127, "text")

    # proofs = Contract(PROOFS_ABI).deploy(get_account(args.wallet,args.password), PROOFS_BYTECODE)

    #ballot = Contract(BALLOT_ABI, BALLOT_ADDRESS)
    #proofs = Contract(PROOFS_ABI, PROOFS_ADDRESS)

    #print(proofs.read("owner"))
    #print(proofs.read("passed", "test"))
    #print(proofs.read("proofHash", "test"))
    #print(proofs.read("votesInFavor", "test"))
    #print(proofs.read("votesAgainst", "test"))

    # print(ballot.read("owner"))
    # print(ballot.read('eligible', '0x66B655a4CE711F00b570f9801c498071e9A15045'))
    # print(ballot.read('voterData', '0x66B655a4CE711F00b570f9801c498071e9A15045').decode("utf-8"))
    # print(ballot.read('proposalDeadline', 'test'))
    # print(ballot.read('votesInFavor', 'test'))
    # print(ballot.read('votesAgainst', 'test'))
    # print(ballot.read('voted', 'test', '0x66B655a4CE711F00b570f9801c498071e9A15045'))

    # print(sender.address)

    # print(proofs.write('submitProposal', sender, 'test', True, 4, 0, string_to_bytes(PROOFS_ADDRESS)))

    # print(ballot.write('addVoter', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045', string_to_bytes('data')))
    # print(ballot.write('removeVoter', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045'))
    # print(ballot.write('propose', sender, 'test', string_to_unixtimestamp("2020-01-01", DATE)))
    # print(ballot.write('vote', sender, 'test', True))
    # print(ballot.write('transferOwnership', sender, '0x66B655a4CE711F00b570f9801c498071e9A15045'))

    sender = get_account(args.wallet, args.password)

    vote = {"proposal": 1,
            "wallet": "0x66B655a4CE711F00b570f9801c498071e9A15045",
            "vote": "YES",
            "timestamp": string_to_unixtimestamp("2019-12-07", DATE)}

    signature = sign(sender, str(vote))
    verified = verify(sender.address, str(vote), signature)

    print(sender.address)
    print(str(vote))
    print(signature)
    print(verified)

    signature = sign(sender, sender.address)
    verified = verify(sender.address, sender.address, signature)

    print(sender.address)
    print(signature)
    print(verified)
