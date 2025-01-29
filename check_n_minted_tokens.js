const { Web3 } = require("web3");
const fs = require("fs");

const w3 = new Web3("http://localhost:8545");
const account = w3.eth.accounts[0];
w3.eth.defaultAccount = account;

const contract_info = JSON.parse(fs.readFileSync("./CONTRACT_DEPLOYMENT_INFO.json").toString());
const contract_abi = contract_info["CONTRACT_ABI"];
const contract_address = contract_info["CONTRACT_ADDRESS"];

const contract = new w3.eth.Contract(contract_abi, contract_address);

async function interact() {
    const name = await contract.methods.name().call();
    console.log(name);
}

interact();
