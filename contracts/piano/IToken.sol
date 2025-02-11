// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

interface IToken {
    function mint(address account, uint256 amount) external;
    function burn(address account, uint256 amount) external;
}