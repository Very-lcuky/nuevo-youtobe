module 0x1::marisolvrs {
    use 0x1::Signer;
    use 0x1::Coin;
    use 0x1::Vector;

    // Estructura del token
    struct Token has store {
        value: u64,
        name: vector<u8>,
        symbol: vector<u8>,
    }

    // Función para crear el token
    public fun create_token(): Token {
        Token {
            value: 1000000,  // 1 millón de unidades
            name: b"marisolvrs".to_vec(),
            symbol: b"MVRS".to_vec(),
        }
    }

    // Obtener el balance del token
    public fun get_balance(token: &Token): u64 {
        token.value
    }

    // Transferir tokens
    public fun transfer(account: &signer, to: address, amount: u64) {
        let token = create_token();
        // Asegurarse de que el token sea transferido correctamente
        debug::print(&format!("Transferir {} tokens a {}", amount, to));
        Coin::mint(account, amount);
    }
}

