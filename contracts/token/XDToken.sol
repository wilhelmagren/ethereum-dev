// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract XDToken {

    string private _name;
    string private _symbol;

    uint256 private _totalSupply;

    mapping(address account => uint256) private _balances;

    constructor() {
        _name = "XDToken";
        _symbol = "XD";
        _totalSupply = 0;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function mint(address account, uint256 value) public {
        _balances[account] += value;
        _totalSupply += value;
    }

    /**
     * @dev this is bad, we can burn more than `_totalSupply` and have underflow...
     * but we are the only ones that can interact with contract so its whatever.
     */
    function burn(address account, uint256 value) internal {
        _balances[account] -= value;
        _totalSupply -= value;
    }
}
