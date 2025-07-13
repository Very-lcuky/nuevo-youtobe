// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./AdvancedERC20.sol";

contract TokenFactory {
    address[] public allTokens;

    event TokenCreated(address indexed tokenAddress, string name, string symbol);

    function createMVRS(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply,
        uint256 _maxSupply,
        uint256 _maxWalletLimit,
        address _marketingWallet,
        address _liquidityWallet,
        uint256 _marketingFee, // en base 10000 (ej. 200 = 2%)
        uint256 _liquidityFee  // en base 10000 (ej. 300 = 3%)
    ) external {
        AdvancedERC20 token = new AdvancedERC20(
            _name,
            _symbol,
            _initialSupply,
            _maxSupply,
            _maxWalletLimit,
            msg.sender,          // owner
            _marketingWallet,
            _liquidityWallet,
            _marketingFee,
            _liquidityFee
        );

        allTokens.push(address(token));
        emit TokenCreated(address(token), _name, _symbol);
    }

    function getAllTokens() external view returns (address[] memory) {
        return allTokens;
    }
}

