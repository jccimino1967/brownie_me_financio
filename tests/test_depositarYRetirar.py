from scripts.helpful_scripts import obtener_cuenta, ENTORNO_LOCAL_BLOCKCHAIN
from scripts.despliego import despliego_meFinancio
from brownie import network, accounts, exceptions
import pytest


def test_DepRet():
    cuenta = obtener_cuenta()
    deposito = despliego_meFinancio()
    print(cuenta, deposito)
    fee_entrada = deposito.getEntranceFee() + 100
    tx = deposito.fund({"from": cuenta, "value": fee_entrada})
    tx.wait(1)
    print(fee_entrada)
    assert deposito.addressToAmountFunded(cuenta.address) == fee_entrada

    tx2 = deposito.retiro({"from": cuenta, "gas_limit": 1200000, "allow_revert": True})
    tx2.wait(1)
    assert deposito.addressToAmountFunded(cuenta.address) == 0


def test_solo_duenoRetira():
    if network.show_active() not in ENTORNO_LOCAL_BLOCKCHAIN:
        pytest.skip("Solo para testeo local")
    deposito = despliego_meFinancio()
    mal_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        deposito.retiro({"from": mal_actor})
