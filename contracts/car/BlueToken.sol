// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "./IToken.sol";

contract BlueToken is IToken {
    mapping(address account => uint256) private _balances;

    string private constant _name = "BlueToken";
    string private constant _symbol = "BT";

    uint256 private _totalSupply;

    constructor() {
        _totalSupply = 0;
    }

    /**
     * @dev Get the name of the token.
     */
    function name() public pure returns (string memory) {
        return _name;
    }

    /**
     * @dev Get the symbol (ticker) of the token.
     */
    function symbol() public pure returns (string memory) {
        return _symbol;
    }

    /**
     * @dev Get the current total supply of tokens in circulation.
     */
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    /**
     * @dev Get the current balance of the ``account``.
     */
    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    /**
     * @dev Creates ``amount`` of new tokens tied to the ``account`` address.
     */
    function mint(address account, uint256 amount) public {
        _totalSupply += amount;
        _balances[account] += amount;
    }

    /**
     * @dev Destroy ``amount`` of tokens for ``account`` if the account has enough
     * balance, otherwise, exits and reverts any gas costs.
     */
    function burn(address account, uint256 amount) public {
        require(_balances[account] >= amount, "BlueToken: burn amount exceeds account balance");
        _totalSupply -= amount;
        _balances[account] -= amount;
    }
}
