from brownie import VideoViewToken, PayPerView, accounts, network, config

def main():
    print(f"Desplegando en la red: {network.show_active()}")

    if network.show_active() == "development":
        acct = accounts[0]
    else:
        acct = accounts.add(config["wallets"]["from_key"])

    fixed_gas_price = 10 * 10**9  # 10 Gwei, puedes ajustar este valor

    video_token = VideoViewToken.deploy({"from": acct, "gas_price": fixed_gas_price})
    print(f"VideoViewToken desplegado en: {video_token.address}")

    price_per_view = 1 * 10 ** 18  # ajusta este valor según tu token

    pay_per_view = PayPerView.deploy(
        video_token.address,
        price_per_view,
        {"from": acct, "gas_price": fixed_gas_price}
    )
    print(f"PayPerView desplegado en: {pay_per_view.address}")

