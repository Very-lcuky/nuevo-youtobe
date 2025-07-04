// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PayPerView {
    IERC20 public token;
    address public owner;
    uint256 public pricePerView;

    event Paid(address indexed viewer, uint256 amount);

    constructor(address _tokenAddress, uint256 _pricePerView) {
        require(_tokenAddress != address(0), "Token address is zero");
        require(_pricePerView > 0, "Price per view must be greater than zero");

        token = IERC20(_tokenAddress);
        owner = msg.sender;
        pricePerView = _pricePerView;
    }

    function payForView() external {
        // El viewer debe haber aprobado previamente este contrato para gastar tokens
        bool sent = token.transferFrom(msg.sender, owner, pricePerView);
        require(sent, "Pago fallido");

        emit Paid(msg.sender, pricePerView);
    }
}

