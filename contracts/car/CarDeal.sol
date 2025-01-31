// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./IToken.sol";

contract CarDeal {
    address private _buyer;
    address private _seller;
    uint256 private _carId;

    uint256 private _price;
    uint256 private _deposit;

    IToken private _buyerToken;
    IToken private _sellerToken;

    event CarOwnerTransfer(address indexed buyer, address indexed seller, uint256 carId);

    constructor(address buyer, address seller, uint256 carId, uint256 price, IToken
                buyerToken, IToken sellerToken) {
        _buyer = buyer;
        _seller = seller;
        _carId = carId;
        _price = price;
        _deposit = 0;
        _buyerToken = buyerToken;
        _sellerToken = sellerToken;
    }

    function deposit(uint256 amount) public {
        _deposit += amount;
        if (_deal_demands()) {
            _execute_deal();
        }
    }

    function _deal_demands() private view returns (bool) {
        return _deposit >= _price;
    }

    function _execute_deal() internal {
        _buyerToken.burn(_price);
        _sellerToken.mint(_price);

        emit CarOwnerTransfer(_buyer, _seller, _carId);
    }
}
