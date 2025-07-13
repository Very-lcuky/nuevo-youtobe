require("dotenv").config();
const { ethers } = require("ethers");

async function revisarBalance() {
  const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);

  const USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
  const CONTRACT_ADDRESS = process.env.REWARD_CONTRACT_ADDRESS;

  const usdcAbi = [
    "function balanceOf(address account) view returns (uint256)",
    "function decimals() view returns (uint8)"
  ];

  const usdc = new ethers.Contract(USDC_ADDRESS, usdcAbi, provider);

  const balance = await usdc.balanceOf(CONTRACT_ADDRESS);
  const decimals = await usdc.decimals();

  console.log(`Balance USDC del contrato: ${ethers.utils.formatUnits(balance, decimals)} USDC`);
}

revisarBalance().catch(console.error);
