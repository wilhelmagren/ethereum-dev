// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./IToken.sol";

contract CarDeal {
    address private _buyer;
    address private _seller;
    uint256 private _carId;

    uint256 private _price;
    uint256 private _depositedAmount;

    IToken private _buyerToken;
    IToken private _sellerToken;

    bool private _hasExecuted;

    event CarOwnerTransfer(address buyer, address seller, uint256 carId,
                           uint256 price);

    constructor(address buyer, address seller, uint256 carId, uint256 price, IToken
                buyerToken, IToken sellerToken) {
        _buyer = buyer;
        _seller = seller;
        _carId = carId;
        _price = price;
        _depositedAmount = 0;
        _buyerToken = buyerToken;
        _sellerToken = sellerToken;
        _hasExecuted = false;
    }

    function deposit(uint256 amount) public {
        if (!_hasExecuted) {
            _depositedAmount += amount;
            if (_dealDemands()) {
                _executeDeal();
            }
        }
    }

    function _dealDemands() private view returns (bool) {
        return _depositedAmount >= _price;
    }

    function _executeDeal() internal {
        _hasExecuted = true;

        _buyerToken.burn(_price);
        _sellerToken.mint(_price);

        emit CarOwnerTransfer(_buyer, _seller, _carId, _price);
    }
}
