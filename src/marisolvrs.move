module marisolvrs::token {
    use iota::coin;

    // Estructura de nuestro token
    public struct Marisolvrs has store {
        value: u64,
        name: vector<u8>,
        symbol: vector<u8>,
    }

    // Función para crear el token Marisolvrs
    public fun create_token(): Marisolvrs {
        Marisolvrs {
            value: 1000000,  // 1 millón de unidades
            name: b"Marisolvrs".to_vec(),  // Nombre del token
            symbol: b"MVRS".to_vec(),  // Símbolo del token
        }
    }

    // Obtener el balance de un token
    public fun get_balance(token: &Marisolvrs): u64 {
        token.value
    }

    // Función para transferir el token
    public fun transfer(to: address, amount: u64) {
        let token = create_token();
        coin::mint(to, amount);  // Mint (crear) tokens para la dirección de destino
    }
}

