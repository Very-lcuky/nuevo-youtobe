public fun init_marol_mvrs(ctx: &mut TxContext) {
    let owner = 0xf2ee8390c2912f3a069ff987fcd7a4c82d1632140e15f121c39c79fab3ebb0bf; // Dirección de tu cuenta
    let initial_supply = 1000000000000; // 1 billón de tokens
    let token = create_token(owner, initial_supply, ctx);
}
