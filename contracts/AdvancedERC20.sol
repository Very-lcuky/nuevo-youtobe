// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title marisolvrs - Token ERC20 con parámetros personalizados
contract AdvancedERC20 {
    string public name = "marisolvrs";
    string public symbol = "MVRS";
    uint8 public decimals = 18;

    uint256 public totalSupply;
    uint256 public immutable maxSupply = 1_000_000_000 * 10 ** 18;  // 1 billón
    uint256 public maxWalletLimit;

    address public owner;
    address public marketingWallet;
    address public liquidityWallet;

    uint256 public marketingFee;  // en base 10000 (ej. 200 = 2%)
    uint256 public liquidityFee;  // en base 10000 (ej. 300 = 3%)

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        uint256 _initialSupply,
        uint256 _maxWalletLimit,
        address _owner,
        address _marketingWallet,
        address _liquidityWallet,
        uint256 _marketingFee,
        uint256 _liquidityFee
    ) {
        require(_initialSupply <= maxSupply, "Suministro inicial supera el maximo");

        totalSupply = _initialSupply;
        maxWalletLimit = _maxWalletLimit;
        owner = _owner;
        marketingWallet = _marketingWallet;
        liquidityWallet = _liquidityWallet;
        marketingFee = _marketingFee;
        liquidityFee = _liquidityFee;

        balanceOf[_owner] = _initialSupply;
        emit Transfer(address(0), _owner, _initialSupply);
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Saldo insuficiente");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;

        require(balanceOf[_to] <= maxWalletLimit, "Supera limite por wallet");

        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}

