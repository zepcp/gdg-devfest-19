from safe import WALLET, PASSWORD

from settings import PROOFS_ABI, PROOFS_ADDRESS

from utils.blockchain import Contract, get_account


def get_contract():
    return Contract(PROOFS_ABI, PROOFS_ADDRESS)


def get_owner():
    return get_contract().read("owner")


def get_result(proposal_id):
    return get_contract().read("passed", proposal_id)


def get_proof(proposal_id):
    return get_contract().read("proofHash", proposal_id)


def get_votes(proposal_id):
    proofs = get_contract()
    return proofs.read("votesInFavor", proposal_id),\
        proofs.read("votesAgainst", proposal_id)


def submit_proposal(proposal_id, passed, in_favor, against, proof):
    sender = get_account(WALLET, PASSWORD)
    return get_contract().write('submitProposal', sender, str(proposal_id), passed, in_favor, against, proof)
