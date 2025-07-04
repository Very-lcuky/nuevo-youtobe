// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VideoViewToken is ERC20 {
    address public owner;

    constructor() ERC20("VideoViewToken", "VVT") {
        owner = msg.sender;
        _mint(owner, 1_000_000 * 10 ** decimals());  // 1 millón de tokens al dueño
    }
}
