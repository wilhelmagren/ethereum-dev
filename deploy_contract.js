const { Web3 } = require("web3");
const fs = require("fs");

const w3 = new Web3("http://localhost:8545");
w3.eth.defaultAccount = "0x123463a4b065722e99115d6c222f267d9cabb524";
console.log("[INFO] setting default eth account to: " + w3.eth.defaultAccount);

const contractAbi = JSON.parse(fs.readFileSync("./target/XDToken.abi").toString());
const contractBytecode = "0x" + fs.readFileSync("./target/XDToken.bin").toString();

const contract = new w3.eth.Contract(contractAbi);

var deployFunction = async function() {
    await contract.deploy({
        data: contractBytecode,
    })
    .send({
        from: w3.eth.defaultAccount,
        gas: 10000000,
    })
}

(async() => {
    await deployFunction(contract);
})

