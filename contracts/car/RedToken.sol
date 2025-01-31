// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "./IToken.sol";

contract RedToken is IToken {
    string private _name;
    string private _symbol;
    uint256 private _totalSupply;

    constructor() {
        _name = "RedToken";
        _symbol = "RT";
        _totalSupply = 0;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function mint(uint256 amount) public {
        _totalSupply += amount;
    }

    function burn(uint256 amount) public {
        _totalSupply -= amount;
    }
}
