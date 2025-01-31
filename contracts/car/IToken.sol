// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

interface IToken {
    function mint(uint256 amount) external;
    function burn(uint256 amount) external;
}
