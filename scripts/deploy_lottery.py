from scripts.helpful_scripts import get_account, get_contract
from brownie import network, Lottery, config

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
            get_contract("eth_usd_price_feed").address,
            get_contract('vrf_coordinator').address,
            get_contract('link_token').address,
            config['networks'][network.show_active()]['fee'],
            config['networks'][network.show_active()]['keyhash'],
            {'from' : account},
            publish_source = ['networks'][network.show_active()].get('verify', False)
            )
    print('Deployed lottery!')

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.start({'from' : account})
    starting_tx.wait(1)
    print('lottery has started')


def main():
    deploy_lottery()
    start_lottery()

