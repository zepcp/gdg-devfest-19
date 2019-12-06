pragma solidity ^0.5.13;

contract BallotProof {
    address public owner;

    mapping(string => bytes) public proofHash;
    mapping(string => bool) public passed;
    mapping(string => uint) public votesInFavor;
    mapping(string => uint) public votesAgainst;

    event OwnershipTransferred(
        address previousOwner,
        address newOwner
    );

    event NewProposal(
        string name,
        bool passed,
        uint votesInFavor,
        uint votesAgainst,
        bytes proofHash
    );

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor() public
    {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public onlyOwner() {
        require(_newOwner != address(0));
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }

    function submitProposal(string memory _name, bool _passed, uint _inFavor, uint _against, bytes _proof) public onlyOwner() {
        require(votesInFavor[_name] == 0);
        require(votesAgainst[_name] == 0);
        passed[_name] = _passed;
        votesInFavor[_name] = _inFavor;
        votesAgainst[_name] = _against;
        proofHash[_name] = _proof;

        emit NewProposal(_name, _passed, _inFavor, _against, _proof);
    }

}
