// Función para aprobar tokens antes de añadir liquidez
async function approveTokens(token, spenderAddress, amount) {
  const allowance = await token.allowance(wallet.address, spenderAddress);
  if (allowance.lt(amount)) {
    console.log(`Aprobando ${ethers.utils.formatUnits(amount, 18)} tokens...`);
    const tx = await token.approve(spenderAddress, amount);
    await tx.wait();
    console.log("¡Tokens aprobados!");
  } else {
    console.log("¡La aprobación ya está hecha!");
  }
}

// Función para agregar liquidez con aprobación previa
async function agregarLiquidez(tokenAmount, stableAmount) {
  try {
    // Obtener saldos de tokens y USDC
    const tokenBalance = await token.balanceOf(wallet.address);
    const stableBalance = await stable.balanceOf(wallet.address);

    console.log(`Saldo de tokens: ${ethers.utils.formatUnits(tokenBalance, 18)}`);
    console.log(`Saldo de USDC: ${ethers.utils.formatUnits(stableBalance, 18)}`);

    // Verificar si tienes suficientes fondos
    if (tokenBalance < tokenAmount || stableBalance < stableAmount) {
      throw new Error("❌ No tienes suficientes tokens o USDC para agregar liquidez.");
    }

    // Aprobar la transferencia de tokens antes de añadir liquidez
    await approveTokens(token, poolAddress, tokenAmount);
    await approveTokens(stable, poolAddress, stableAmount);

    // Aprobar la transferencia de USDC
    console.log(`Aprobación de ${ethers.utils.formatUnits(tokenAmount, 18)} tokens y ${ethers.utils.formatUnits(stableAmount, 18)} USDC...`);

    // Añadir liquidez al pool
    const tx = await pool.addLiquidity(tokenAmount, stableAmount);
    console.log(`Transacción enviada: ${tx.hash}`);

    // Esperar que la transacción sea confirmada
    const receipt = await tx.wait();
    if (receipt.status === 1) {
      console.log("🎉 ¡Liquidez agregada con éxito!");
    } else {
      console.log("❌ Error en la transacción de liquidez.");
    }
  } catch (err) {
    console.error("❌ Error:", err);
  }
}

