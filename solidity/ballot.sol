pragma solidity ^0.5.13;

contract Ballot {
    address public owner;

    mapping(address => bool) public eligible;
    mapping(address => bytes) public voterData;
    mapping(string => mapping(address => bool)) public voted;
    mapping(string => uint) public votesInFavor;
    mapping(string => uint) public votesAgainst;
    mapping(string => uint) public proposalDeadline;

    event OwnershipTransferred(
        address previousOwner,
        address newOwner
    );

    event AddedVoter(
        address voter
    );

    event RemovedVoter(
        address previousOwner
    );

    event NewProposal(
        string name,
        uint deadline
    );

    event NewVote(
        string name,
        bool inFavor
    );

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier onlyEligible() {
        require(eligible[msg.sender] == true);
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

    function addVoter(address _voter, bytes memory _data) public onlyOwner() {
        require(_voter != address(0));
        require(eligible[_voter] == false);
        eligible[_voter] = true;
        voterData[_voter] = _data;
        emit AddedVoter(_voter);
    }

    function removeVoter(address _voter) public onlyOwner() {
        require(_voter != address(0));
        require(eligible[_voter] == true);
        eligible[_voter] = false;
        voterData[_voter].length = 0;
        emit RemovedVoter(_voter);
    }

    function propose(string memory _name, uint _deadline) public onlyOwner() {
        require(proposalDeadline[_name] == 0);
        proposalDeadline[_name] = _deadline;
        votesInFavor[_name] = 0;
        votesAgainst[_name] = 0;
        emit NewProposal(_name, _deadline);
    }

    function vote(string memory _name, bool _inFavor) public onlyEligible() {
        require(proposalDeadline[_name] > now);
        require(voted[_name][msg.sender] == false);
        voted[_name][msg.sender] = true;

        if (_inFavor) {
            votesInFavor[_name] += 1;
        }
        else {
            votesAgainst[_name] += 1;
        }
        emit NewVote(_name, _inFavor);
    }

}
