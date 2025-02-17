// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./Car.sol";

/// @title Ledger for tokenized cars
/// @author Wilhelm Ågren
/// @notice Implementation of a ledger for storing tokenized cars.
contract CarLedger {
    mapping(uint256 uniqueId => address) private _cars;

    event RegisteredCar(uint256 carId, address carAddress);

    function registerCar(Car car) external {
        require(_cars[car.uniqueId()] == address(0), "The car has already been registered");

        uint256 carId = car.uniqueId();
        address carAddress = address(car);

        _cars[carId] = carAddress;
        emit RegisteredCar(carId, carAddress);
    }

    function getCarAddress(uint256 carId) external view returns (address) {
        return _cars[carId];
    }
}
