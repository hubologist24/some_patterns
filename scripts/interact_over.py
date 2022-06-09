from eth_account import Account
from brownie import Over, network, Contract, config, exceptions

from web3 import Web3

import time

from scripts.helpful_scripts import get_account


def main():
    interact()


def interact():
    account = get_account()
    t = Over[-1]
    print(t.randomness({"from": account}))
    print(t.getUsdPrice({"from": account}))
