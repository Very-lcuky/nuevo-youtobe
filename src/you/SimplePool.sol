// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address from, address to, uint amount) external returns (bool);
    function transfer(address to, uint amount) external returns (bool);
    function balanceOf(address account) external view returns (uint);
}

contract SimplePool {
    IERC20 public token;
    IERC20 public stable;

    uint public reserveToken;
    uint public reserveStable;

    constructor() {
        token = IERC20(0x7f1672D7514648a0E7BAEe7ef52C2e4Df65184FD); // Tu token
        stable = IERC20(0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913); // USDC Base
    }

    function addLiquidity(uint tokenAmount, uint stableAmount) external {
        require(token.transferFrom(msg.sender, address(this), tokenAmount), "Token transfer failed");
        require(stable.transferFrom(msg.sender, address(this), stableAmount), "Stable transfer failed");

        reserveToken += tokenAmount;
        reserveStable += stableAmount;
    }

    function swapStableForToken(uint stableAmountIn) external {
        require(stable.transferFrom(msg.sender, address(this), stableAmountIn), "Stable transfer failed");

        uint tokenOut = getAmountOut(stableAmountIn, reserveStable, reserveToken);
        require(token.transfer(msg.sender, tokenOut), "Token transfer failed");

        reserveStable += stableAmountIn;
        reserveToken -= tokenOut;
    }

    function swapTokenForStable(uint tokenAmountIn) external {
        require(token.transferFrom(msg.sender, address(this), tokenAmountIn), "Token transfer failed");

        uint stableOut = getAmountOut(tokenAmountIn, reserveToken, reserveStable);
        require(stable.transfer(msg.sender, stableOut), "Stable transfer failed");

        reserveToken += tokenAmountIn;
        reserveStable -= stableOut;
    }

    function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) public pure returns (uint) {
        require(amountIn > 0, "amountIn must be > 0");
        require(reserveIn > 0 && reserveOut > 0, "invalid reserves");

        uint amountInWithFee = amountIn * 997;
        uint numerator = amountInWithFee * reserveOut;
        uint denominator = (reserveIn * 1000) + amountInWithFee;
        return numerator / denominator;
    }
}

