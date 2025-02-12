// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;


/**
 * @dev Interface for a barebones ERC20 style token, but without support
 * for transfering tokens between two accounts. You can create (mint) new
 * tokens or destroy (burn) existing tokens for an account (wallet address).
 */
interface IToken {
    /**
     * @dev Get the balance of the ``account`` address.
     */
    function balanceOf(address account) external view returns (uint256);
    /**
     * @dev Create ``amount`` of new tokens and add them to the ``account`` balances.
     */
    function mint(address account, uint256 amount) external;

    /**
     * @dev Destroy ``amount`` of tokens and remove them from the ``account`` balances.
     */
    function burn(address account, uint256 amount) external;
}
