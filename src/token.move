module marisolmvrs::token {
    use std::vector;
    use iota::types;

    // Definición de la estructura de un Token
    public struct Token has store {
        owner: address,
        balance: u64,
    }

    // Crear el token MarisolMVRS con un suministro inicial de 1 billón de tokens
    public fun create_token(owner: address, initial_supply: u64, ctx: &mut TxContext): Token {
        let new_token = Token {
            owner: owner,
            balance: initial_supply,
        };
        // Registrar el token en el contrato
        object::new(ctx, new_token)
    }

    // Función para transferir el token
    public fun transfer_token(
        from: address, 
        to: address, 
        amount: u64, 
        ctx: &mut TxContext
    ) {
        // Verificar si el balance es suficiente
        let sender = borrow_global_mut<Token>(from);
        assert!(sender.balance >= amount, 0);
        sender.balance = sender.balance - amount;
        
        let receiver = borrow_global_mut<Token>(to);
        receiver.balance = receiver.balance + amount;
    }

    // Función para verificar el saldo de un usuario
    public fun get_balance(staker: address): u64 {
        let token = borrow_global<Token>(staker);
        token.balance
    }

    // Función para permitir staking de tokens
    public fun stake_token(
        staker: address, 
        amount: u64, 
        ctx: &mut TxContext
    ) {
        let token = borrow_global_mut<Token>(staker);
        assert!(token.balance >= amount, 0);
        token.balance = token.balance - amount;

        // Lógica de staking (se puede agregar recompensas aquí)
    }
}
