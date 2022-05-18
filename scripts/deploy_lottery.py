from scripts.helpful_script import get_account
from brownie import accounts, network, Lottery

def deploy_lottery():
    account = get_account
    Lottery =Lottery.deploy(get_contract("eth_usd_price_feed").address)

def main():
    deploy_lottery()
