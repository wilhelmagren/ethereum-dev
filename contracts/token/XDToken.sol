// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC20.sol";

contract XDToken is ERC20 {
    constructor() ERC20("XDToken", "XD") {
        _mint(msg.sender, 0);
    }
}
