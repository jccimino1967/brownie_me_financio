from brownie import Me_Financio, network, config, MockV3Aggregator
from eth_typing import Address
from scripts.helpful_scripts import (
    despliego_imitador,
    obtener_cuenta,
    ENTORNO_LOCAL_BLOCKCHAIN,
)
from web3 import Web3


def despliego_meFinancio():
    cuenta = obtener_cuenta()
    # Paso la direccion del alimentador de precio a nuestro contrato MeFinancio
    # Paso la address desde el despliegue de Python a MeFinancio de Solidity

    # Esto si estoy en una red persistente como Goerli, uso la direccion asociada,
    # sino, despliego un Mock
    if network.show_active() not in ENTORNO_LOCAL_BLOCKCHAIN:
        direccionAlimentador = config["networks"][network.show_active()][
            "eth_usd_alimentador"
        ]
    else:
        despliego_imitador()
        direccionAlimentador = MockV3Aggregator[-1].address
    meFinancio = Me_Financio.deploy(
        direccionAlimentador,
        {"from": cuenta},
        publish_source=config["networks"][network.show_active()].get("verifica"),
    )

    print(f"Contrato desplegado en la direccion {meFinancio}")
    print(f"Contrato desplegado en la direccion {meFinancio.address}")

    return meFinancio


def main():
    despliego_meFinancio()
