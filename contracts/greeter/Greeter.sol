// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

contract Greeter {
    string greeting;

    constructor() {
        greeting = "Hello jockeboiiii";
    }

    function setGreeting(string memory _greeting) public {
        greeting=_greeting;
    }

    function greet() public view returns (string memory) {
        return greeting;
    }
}
