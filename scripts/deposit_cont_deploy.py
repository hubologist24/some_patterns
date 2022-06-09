from brownie import DepositContract, network, Contract, config

from web3 import Web3

from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_deneme():
    account = get_account()
    try:
        t = DepositContract[-1]
    except (IndexError):
        print("deploying ")
        t = DepositContract.deploy({"from": account})
    finally:
        print(t)


def deploy_another_deneme():
    account = get_account()


def deploy():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        another_acc = get_account(index=3)
        some_another_acc = get_account(index=5)
    t = DepositContract.deploy({"from": account})
    t.deposit({"from": account, "value": Web3.toWei(0.001, "ether")})
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        t.deposit({"from": some_another_acc, "value": Web3.toWei(5, "ether")})
        t.deposit({"from": another_acc, "value": Web3.toWei(7, "ether")})

    for index in range(len(t.getAccountHolders())):
        add, amount = t.getAccountHolders()[index]
        print(add)
        print(amount)
    # print(t.getAccountHolders[0].amount())


def main():
    # deploy_deneme()
    # deploy()
    deploy_another_deneme()
