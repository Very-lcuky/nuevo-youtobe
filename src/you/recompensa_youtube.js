require("dotenv").config();
const { ethers } = require("ethers");

const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const rewardContractAddress = process.env.REWARD_CONTRACT_ADDRESS;
const tokenAddress = process.env.TOKEN_ADDRESS;

if (!rewardContractAddress || !tokenAddress) {
  throw new Error("❌ Faltan direcciones de contrato en .env");
}

const rewardAbi = ["function rewardForView(uint256 tokenAmount) external"];
const tokenAbi = [
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function balanceOf(address account) external view returns (uint256)",
  "function decimals() view returns (uint8)"
];

async function main() {
  const rewardContract = new ethers.Contract(rewardContractAddress, rewardAbi, wallet);
  const tokenContract = new ethers.Contract(tokenAddress, tokenAbi, wallet);
  const decimals = await tokenContract.decimals();
  const rewardAmount = ethers.utils.parseUnits("10", decimals); // Ajusta la cantidad según tus necesidades

  try {
    const balance = await tokenContract.balanceOf(wallet.address);
    console.log(`💰 Token balance: ${ethers.utils.formatUnits(balance, decimals)}`);
    if (balance.lt(rewardAmount)) throw new Error("❌ No tienes suficientes tokens");

    let allowance = await tokenContract.allowance(wallet.address, rewardContractAddress);
    console.log(`🔐 Current allowance: ${ethers.utils.formatUnits(allowance, decimals)}`);
    if (allowance.lt(rewardAmount)) {
      console.log("📤 Approving tokens...");
      const approvalTx = await tokenContract.approve(rewardContractAddress, rewardAmount);
      await approvalTx.wait(); // Asegúrate de esperar la confirmación
      console.log("✅ Approved");
      
      // Esperamos un poco para que la transacción de aprobación se procese
      await new Promise(resolve => setTimeout(resolve, 2000));
    }

    console.log("🚀 Simulating transaction to get revert reason (if any)...");
    const data = rewardContract.interface.encodeFunctionData("rewardForView", [rewardAmount]);
    try {
      await provider.call({ to: rewardContractAddress, data });
      console.log("✅ Simulation passed — no revert in static call.");
    } catch (callErr) {
      const hex = (callErr.data || "").slice(138);
      const reason = ethers.utils.toUtf8String("0x" + hex).replace(/\x00/g, "");
      console.error("❌ Revert reason:", reason);
      return;
    }

    // Aumentamos el gasLimit a 2,000,000 para más seguridad
    console.log("✅ Sending actual transaction...");
    const tx = await rewardContract.rewardForView(rewardAmount, { gasLimit: 2000000 });  // Aumentado gasLimit
    const receipt = await tx.wait();
    console.log(receipt.status === 1 ? "🎉 Reward sent!" : "❌ Transaction failed on execution.");

  } catch (err) {
    console.error("❌ General error:", err);
  }
}

main();

