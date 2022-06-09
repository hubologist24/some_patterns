from brownie import (
    accounts,
    network,
    config,
    Contract,
    VRFCoordinatorMock,
    MockV3Aggregator,
    LinkToken,
)

from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    # account[0]
    # accounts.add("env")
    # account.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("here1")
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        print("here2")
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    # if len(MockV3Aggregator) <= 0: {"from": get_account()}
    account = get_account()
    print(f"active network is {network.show_active()}")
    print("Deploying mocks...")
    MockV3Aggregator.deploy(decimals, INITIAL_VALUE, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account}),
    print("deployed")
    # recent -1
    # price_feed_addres = MockV3Aggregator[-1].address
    # decimals, Web3.toWei(initial_value, "ether"), {"from": account}


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # tx = interface.LinkTokenInterface.transfer(
    #    contract_address, amount, {"from": account}
    # )
    tx.wait(1)
    print("fund link contract")
