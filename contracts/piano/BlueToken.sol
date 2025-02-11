// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./IToken.sol";

contract BlueToken is IToken {
    mapping(address account => uint256) private _balances;

    uint256 private _totalSupply;

    string private constant _name = "BlueToken";
    string private constant _symbol = "BT";

    constructor() {
        _totalSupply = 0;
    }

    function name() public pure returns (string memory) {
        return _name;
    }

    function symbol() public pure returns (string memory) {
        return _symbol;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function mint(address account, uint256 amount) public {
        _totalSupply += amount;
        _balances[account] += amount;
    }

    function burn(address account, uint256 amount) public {
        require(_balances[account] >= amount, "BlueToken: burn amount exceeds balance");
        _totalSupply -= amount;
        _balances[account] -= amount;
    }
}