// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

contract Car {
    address private _owner;

    string private immutable _modelName;
    string private immutable _licensePlate;

    constructor(
        address owner,
        string memory modelName_,
        string memory licensePlate_
    ) {
        _owner = owner;
        _modelName = modelName_;
        _licensePlate = licensePlate_;
    }

    function modelName() external view returns (string memory) {
        return _modelName;
    }

    function licensePlate() external view returns (string memory) {
        return _licensePlate;
    }
}
