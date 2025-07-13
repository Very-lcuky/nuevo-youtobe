// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VideoViewToken is ERC20 {

    address public owner;

    // Precio por visualización (en tokens)
    uint256 public pricePerView = 10 * 10**18;  // 10 Tokens por visualización

    constructor() ERC20("VideoViewToken", "VVT") {
        owner = msg.sender;
        _mint(owner, 1000000 * 10**18);  // Mint inicial para el propietario
    }

    // Función para pagar por ver un video
    function payForView(address viewer) public payable {
        require(msg.value == pricePerView, "Cantidad incorrecta de Ether enviada.");
        // Transferir tokens al propietario del contrato
        _transfer(owner, viewer, pricePerView);  // El propietario recibe el pago
    }
}

