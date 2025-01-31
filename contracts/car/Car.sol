// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

contract Car {
    string private _name;
    uint256 private _age;
    uint256 private _id;
    address private _owner;

    constructor(string name, uint256 age, uint256 id, address owner) {
        _name = name;
        _age = age;
        _id = id;
        _owner = owner;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function age() public view returns (uint256) {
        return _age;
    }

    function id() public view returns (uint256) {
        return _id;
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function setOwner(address newOwner) public {
        _owner = newOwner;
    }
}
