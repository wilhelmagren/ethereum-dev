// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "./ERC20.sol";

contract BlueToken is ERC20 {
    constructor() ERC20("BlueToken", "BT") {
        _mint(msg.sender, 0);
    }
}
