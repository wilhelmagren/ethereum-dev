// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./IToken.sol";

/**
 * @dev Implementation of an escrow contract for the transfer of a piano ownership.
 *
 * This is a simplified implementation which utilizes custom ERC20 tokens for the
 * buyer and seller to manage the monetary transfer of value for the piano.
 */
contract PianoEscrow {
    address private _buyer;
    address private _seller;
    uint256 private _price;
    uint256 private _carId;

    uint256 private _deposit;
    uint256 private _depositReleaseDate;

    IToken private _buyerToken;
    IToken private _sellerToken;

    bool private _contractExecuted;

    event PianoOwnerTransfer(address buyer, address seller, uint256 carId, uint256 price);
    event DepositWithdrawn(address buyer, uint256 amount);

    /**
     * @dev Sets the initial agreed upon terms for the piano deal.
     * 
     * These values are immutable - and can only be set once during construction.
     */
    constructor(
        address buyer,
        address seller,
        uint256 price,
        uint256 carId,
        uint256 depositReleaseDate,
        IToken buyerToken,
        IToken sellerToken
    ) {
        _buyer = buyer;
        _seller = seller;
        _price = price;
        _carId = carId;
        _deposit = 0;
        _depositReleaseDate = depositReleaseDate;
        _buyerToken = buyerToken;
        _sellerToken = sellerToken;
        _contractExecuted = false;
    }

    function deposit(uint256 amount) public {
        require(msg.sender == _buyer, "PianoDeal: only buyer can deposit");
        require(!_contractExecuted, "PianoDeal: contract already executed");
        require(!hasExpired(), "PianoDeal: contract expired");

        _deposit += amount;
        _buyerToken.burn(_buyer, amount);

        if (_demands()) {
            _execute();
        }
    }

    function _demands() internal view returns (bool) {
        return (block.timestamp <= _depositReleaseDate) && (_deposit >= _price);
    }

    function hasExpired() public view returns (bool) {
        return (block.timestamp > _depositReleaseDate);
    }

    function _execute() internal {
        require(_demands(), "PianoDeal: demands not met");

        _contractExecuted = true;

        _buyerToken.burn(_buyer, _price);
        _sellerToken.mint(_seller, _price);

        emit PianoOwnerTransfer(_buyer, _seller, _carId, _price);
    }

    function withdrawDeposit() public {
        require(msg.sender == _buyer, "PianoDeal: only buyer can withdraw deposit");
        require(hasExpired(), "PianoDeal: contract not expired yet");

        _buyerToken.mint(_buyer, _deposit);
        _deposit = 0;

        emit DepositWithdrawn(_buyer, _deposit);
    }
}