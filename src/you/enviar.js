require("dotenv").config();
const { ethers } = require("ethers");

async function enviarUSDC() {
  const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

  const USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
  const CONTRACT_ADDRESS = process.env.REWARD_CONTRACT_ADDRESS; // 0x7f1672D7514648a0E7BAEe7ef52C2e4Df65184FD

  // ABI mínimo para transferir USDC
  const usdcAbi = [
    "function transfer(address to, uint256 amount) external returns (bool)",
    "function decimals() view returns (uint8)"
  ];

  const usdc = new ethers.Contract(USDC_ADDRESS, usdcAbi, wallet);

  const decimals = await usdc.decimals(); // Normalmente 6 para USDC

  const amount = ethers.utils.parseUnits("5", decimals); // 5 USDC

  console.log(`Enviando 5 USDC a contrato ${CONTRACT_ADDRESS}...`);

  const tx = await usdc.transfer(CONTRACT_ADDRESS, amount);
  await tx.wait();

  console.log("Transferencia completada.");
}

enviarUSDC().catch(console.error);
