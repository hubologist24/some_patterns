from eth_account import Account
from brownie import Over, network, Contract, config, exceptions

from web3 import Web3

import time


from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    fund_with_link,
)

STATIC_RNG = 777


def main():
    deploy()


def deploy():
    account = get_account()
    price_feed_address = get_contract("eth_usd_price_feed")
    vrf_coordi = get_contract("vrf_coordinator")
    link_token = get_contract("link_token")
    t = Over.deploy(
        price_feed_address,
        vrf_coordi,
        link_token,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    fund_with_link(t.address)
    print("deployed")
    print(t)
    print(f"usd price: {t.getUsdPrice()}")
    trans = t.requestRandomness({"from": account})
    time.sleep(60)
    request_id = trans.events["RequestedRandomness"]["requestId"]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        get_contract("vrf_coordinator").callBackWithRandomness(
            request_id, STATIC_RNG, t.address, {"from": account}
        )
    print(f"randomness:{t.randomness()}")
