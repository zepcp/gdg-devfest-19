const Web3 = require('web3')
const provider = new Web3.providers.HttpProvider('ws://localhost:8545')//'https://ropsten.infura.io')
const web3 = new Web3(provider)

function toHex(str) {
    var hex = ''
    for(var i=0;i<str.length;i++) {
        hex += ''+str.charCodeAt(i).toString(16)
    }
    return hex
}

let addr = "0x66B655a4CE711F00b570f9801c498071e9A15045" //web3.eth.accounts[0]
let msg = 'I really did make this message'
let hashed_msg = '0x' + toHex(msg)

console.log(addr)
console.log(msg)
console.log(hashed_msg)

console.log(web3)

acc = web3.personal.newAccount("");
web3.personal.unlockAccount(acc, "");

let signature = web3.eth.sign(addr, hashed_msg)
console.log(signature)
