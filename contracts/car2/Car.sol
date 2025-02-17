// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

/// @title Tokenized car
/// @author Wilhelm Ågren
/// @notice Implementation of a car with information from transportstyrelsen.
contract Car {
    uint256 private _modelName;
    uint256 private _licensePlate;
    uint256 private _manufacturedDate;
    uint256 private _uniqueId;

    uint256 private _acquisitionDate; 
    uint256 private _previousInspectionDate;

    address private _owner;
    address[] private _previousOwners;

    constructor(
        uint256 modelName_,
        uint256 licensePlate_,
        uint256 manufacturedDate_,
        uint256 uniqueId_,
        address owner_
    ) {
        _modelName = modelName_;
        _licensePlate = licensePlate_;
        _manufacturedDate = manufacturedDate_;
        _uniqueId = uniqueId_;
        _owner = owner_;
    }

    function modelName() external view returns (uint256) {
        return _modelName;
    }

    function licensePlate() external view returns (uint256) {
        return _licensePlate;
    }

    function manufacturedDate() external view returns (uint256) {
        return _manufacturedDate;
    }

    function uniqueId() external view returns (uint256) {
        return _uniqueId;
    }

    function owner() external view returns (address) {
        return _owner;
    }

    function numPreviousOwners() external view returns (uint256) {
        return _previousOwners.length;
    }

    function previousInspectionDate() external view returns (uint256){
        return _previousInspectionDate;
    }

    function acquisitionDate() external view returns (uint256) {
        return _acquisitionDate;
    }

    function setLicensePlate(uint256 licensePlate_) external {
        _licensePlate = licensePlate_;
    }

    function setPreviousInspectionDate(uint256 previousInspectionDate_) external {
        _previousInspectionDate = previousInspectionDate_;
    }

    function setAcquisitionDate(uint256 acquisitionDate_) external {
        _acquisitionDate = acquisitionDate_;
    }

    function setOwner(address owner_) external {
        _owner = owner_;
    }

    function addPreviousOwner(address previousOwner_) external {
        _previousOwners.push(previousOwner_);
    }
}
