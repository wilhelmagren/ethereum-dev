// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

interface BTErrors {
    /**
     * @dev Indicates an error related to the current `balance` of a `sender`, used in transfers.
     * @param sender Address whose tokens are being transferred.
     * @param balance Current balance for the interacting account.
     * @param needed Minimum amount required to perform a transfer.
     */
    error BTInsufficientBalance(address sender, uint256 balance, uint256 needed);

    /**
     * @dev Indicates a failure with the token `receiver`, used in transfers.
     * @param receiver Address to which tokens are being transferred.
     */
    error BTInvalidReceiver(address receiver);

    /**
     * @dev Indicates a failure with the token `sender`, used in transfers.
     * @param sender Address whose tokens are being transferred.
     */
    error BTInvalidSender(address sender);
}

contract BlueToken is BTErrors {
    mapping(address account => uint256) private _balances;

    uint256 private _totalSupply;

    string private _name;
    string private _symbol;

    /**
     * @dev Sets the name, symbol, and totalSupply for the token.
     * 
     * Note: this contract does not mint tokens at creation time, instead, a token is
     * minted 1:1 for each currency (SEK) that is deposited to our traditional ledger.
     */
    constructor() {
        _totalSupply = 0;
        _name = "BlueToken";
        _symbol = "BT";
    }

    /**
     * @dev Emitted when `value` tokens are moved from one account to another.
     *
     * Note that `value` may be zero.
     */
    event Transfer(address indexed from, address indexed to, uint256 value);

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
        if (account == address(0)) {
            revert BTInvalidReceiver(address(0));
        }
        _update(address(0), account, value);
    }

    function burn(address account, uint256 value) public {
        if (account == address(0)) {
            revert BTInvalidSender(address(0));
        }
        _update(account, address(0), value);
    }

    /**
     * @dev Transfers `value` amount of tokens from one address to another. If this is
     * used with the zero address `address(0)` then tokens are either minted or burned
     * depending on whether it is `from` or `to` (minted/burned).
     */
    function _update(address from, address to, uint256 value) internal {
        if (from == address(0)) {
            _totalSupply += value;
        } else {
            uint256 fromBalance = _balances[from];

            if (fromBalance < value) {
                revert BTInsufficientBalance(from, fromBalance, value);
            }

            unchecked {
                _balances[from] = fromBalance - value;
            }
        }

        if (to == address(0)) {
            unchecked {
                _totalSupply -= value;
            }
        } else {
            unchecked {
                _balances[to] += value;
            }
        }

        emit Transfer(from, to, value);
    }
}
