// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

contract Greeter {
    string private _greeting;

    constructor() {
        _greeting = "Hello jockeboiiii";
    }

    function setGreeting(string memory greeting) public {
        _greeting=greeting;
    }

    function greet() public view returns (string memory) {
        return _greeting;
    }
}
