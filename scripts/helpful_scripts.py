from brownie import network, config, accounts, MockV3Aggregator, VRFCoordinatorMock, Contract, LinkToken
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
contract_to_mock = {
        "eth_usd_price_feed" : MockV3Aggregator,
        'vrf_coordinator' :VRFCoordinatorMock,
        'link_token' : LinkToken
        }
def get_contract(contract_name):
    """
    This is a contract that will get the contract address from the brownie config
    if defined, otherwise it will deploy with mock version of the contract and 
    return that contract adderss.
    args : contract name(string)
    Returns : brownie.network.contract.projectContract: The most recently deployed contract version.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in  LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
            contract = contract_type[-1]
            #MockV3Aggregator[-1]
        else:
            contract_adderss = config["networks"][network.show_active()][contract_name]
            #address
            #Abi
            contract = Contract.from_abi(
                    contract_type._name, contract_address, contract_type.abi
             )
            #MockV3Aggregator
            return contract

def deploy_mocks(decimal = DECIMALS, initial_value = STARTING_PRICE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        print("Deploying Mocks...")
        #mock_price_feed = 
        MockV3Aggregator.deploy(decimal, initial_value, {"from" : account})
        link_token = LinkToken.deploy({'from': account})
        VRFCoordinatorMock.deploy(link_token.address, {'from' : account})
    print("Mocks Deployed!")
