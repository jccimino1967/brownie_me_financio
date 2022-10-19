from brownie import network, config, accounts
from brownie import MockV3Aggregator
from web3 import Web3

ENTORNO_LOCAL_BIFURCADO = ["mainnet-fork", "mainnet-fork-dev"]
ENTORNO_LOCAL_BLOCKCHAIN = ["development", "ganacheJuanca"]
decimales = 8
precioInicial = 200000000000


def obtener_cuenta():
    if (
        network.show_active() in ENTORNO_LOCAL_BLOCKCHAIN
        or network.show_active() in ENTORNO_LOCAL_BIFURCADO
    ):
        print(accounts[0])
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key1"])


# Deploy Mock es mas lindo, jaja
def despliego_imitador():

    print(f"La red activa es {network.show_active()}")
    print("Desplegando Mock...")
    # 18, 2000000000000000000000
    # Web3.toWei( 2000 , "ether") Es lo mismo
    # Chequeamos si no lo desplegamos mas de una vez
    if len(MockV3Aggregator) <= 1:
        MockV3Aggregator.deploy(
            decimales, Web3.toWei(precioInicial, "ether"), {"from": obtener_cuenta()}
        )

    print("Mock desplegado!")
