const { ethers } = require("ethers");

console.log("ethers.providers:", ethers.providers);

const provider = new ethers.providers.JsonRpcProvider("https://mainnet.infura.io/v3/TU_INFURA_ID");

console.log("Provider creado:", provider.connection);
