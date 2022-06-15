from brownie import network, Contract, config, Create2Factory

from web3 import Web3

from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def create_deneme():
    account = get_account()
    salt = 1235
    create_factory = Create2Factory.deploy({"from": account})
    bytecode = create_factory.getBytecode(account)
    print(bytecode)
    print("----------")
    print(f"contract will be deployed at:{create_factory.getAddress(bytecode, salt)}")
    t = create_factory.deploy2(salt)
    # print(t.events[0]["Deploy"])
    print(t.events[0]["addr"])


def main():
    create_deneme()
