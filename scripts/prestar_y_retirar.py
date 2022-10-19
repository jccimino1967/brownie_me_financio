from brownie import Me_Financio

from scripts.helpful_scripts import obtener_cuenta


def main():
    depositar()
    retirar()


def depositar():
    me_financio = Me_Financio[-1]
    cuenta = obtener_cuenta()
    fee_entrada = me_financio.getEntranceFee()

    # print(f"Precio del Ether : { precioEth }")
    # print(f"Precio minimo : { minimo } / 50 dolares")
    # print(f"Precision : { precision } / 18 ceros")
    print(f"La tarifa actual de estarda es : { fee_entrada }")
    print("Depositando....")
    me_financio.fund({"from": cuenta, "value": fee_entrada})


def retirar():
    me_financio = Me_Financio[-1]
    cuenta = obtener_cuenta()
    print("Retirando....")
    me_financio.retiro({"from": cuenta, "gas_limit": 1200000, "allow_revert": True})
