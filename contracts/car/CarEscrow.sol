// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./IToken.sol";

/**
 * @dev Implementation of an escrow smart contract that enables ``_buyer`` and ``_seller`
 * to transfer ownership of a car in exchange of ``_price`` amount of tokens.
 *
 * This escrow contract only works under the following assumptions:
 * 1) the ``_buyerToken`` and ``_sellerToken`` are traded at exactly a 1:1 ratio.
 * 2) the contract itself has a monetary value equal to the deposit amount.
 *
 */
contract CarEscrow {
    address private immutable _buyer;
    address private immutable _seller;
    uint256 private immutable _price;
    uint256 private immutable _carId;

    uint256 private _deposit;
    uint256 private immutable _depositReleaseDate;

    IToken private immutable _buyerToken;
    IToken private immutable _sellerToken;

    bool private _executed;

    event CarOwnerTransfer(address buyer, address seller, uint256 carId, uint256 price);
    event WithdrawnDeposit(address buyer, uint256 amount);

    /**
     * @dev Function modifier which makes it so that only the ``_buyer`` can call the function.
     */
    modifier onlyBuyer() {
        require(
            msg.sender == _buyer,
            "CarEscrow: only the buyer of the car is allowed to call this function"
        );
        _;
    }

    /**
     * @dev Function modifier which makes it so that the function is only callable if the
     * ``_buyer`` has a balance of at least the amount that is to be deposited.
     */
    modifier hasSufficientBalance(uint256 amount) {
        require(
            _buyerToken.balanceOf(_buyer) >= amount,
            "CarEscrow: the buyer does not have succifient balance of tokens to make deposit"
        );
        _;
    }

    /**
     * @dev Initializes the escrow contract with the agreed upon terms of the deal.
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

        _executed = false;
    }

    /**
     * @dev The agreed upon terms for the deal.
     */
    function _demands() internal view returns (bool) {
        return (block.timestamp <= _depositReleaseDate) && (_deposit >= _price);
    }

    /**
     * @dev Execute the deal that was agreed upon.
     */
    function _executeDeal() internal {
        _executed = true;

        _sellerToken.mint(_seller, _price);

        // We need to mint some tokens for the buyer since they deposited too much.
        if (_deposit > _price) {
            _buyerToken.mint(_buyer, _deposit - _price);
        }

        _deposit = 0;

        emit CarOwnerTransfer(_buyer, _seller, _carId, _price);
    }

    /**
     * @dev Get status on whether or not the deal has expired.
     */
    function _hasExpired() internal view returns (bool) {
        return block.timestamp > _depositReleaseDate;
    }

    /**
     * @dev Make a deposit of an amount of tokens to the escrow contract.
     * Only callable by the buyer account that is specified in the terms of the deal. 
     */
    function deposit(uint256 amount) external onlyBuyer hasSufficientBalance(amount) {
        require(!_executed, "CarEscrow: the deal has already been executed");
        require(!_hasExpired(), "CarEscrow: the deal has already expired");

        _deposit += amount;
        _buyerToken.burn(_buyer, amount);

        if(_demands()) {
            _executeDeal();
        }
    }

    /**
     * @dev Get the amount of money that has been deposited.
     */
    function depositedAmount() external view returns (uint256) {
        return _deposit;
    }

    /**
     * @dev Attempt to withdraw the deposit from the contract.
     * This is possible if:
     *  - the deal has not already been executed, and
     *  - the deal has reached its expiry date.
     */
    function withdrawDeposit() external onlyBuyer {
        require(!_executed, "CarEscrow: the deal has already been executed");
        require(_hasExpired(), "CarEscrow: the deal has not yet expired");

        _buyerToken.mint(_buyer, _deposit);
        _deposit = 0;

        emit WithdrawnDeposit(_buyer, _deposit); 
    }
}
