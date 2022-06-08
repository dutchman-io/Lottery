from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import network, Lottery, config
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
            get_contract("eth_usd_price_feed"),#.address,
            get_contract("vrf_coordinator"),#.address,
            get_contract('link_token').address,
            config['networks'][network.show_active()]['fee'],
            config['networks'][network.show_active()]['keyhash'],
            {'from' : account},
            publish_source = config['networks'][network.show_active()].get('verify', False)
            )
    print('Deployed lottery!')
    return lottery
def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.begin({'from' : account})
    starting_tx.wait(1)
    print('lottery has started')

def enter_lottery():
    account = get_account()
    lottery =Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({'from':account, 'value' : value})
    tx.wait(1)
    print('You entered the lottery')

def end():
    account = get_account()
    lottery= Lottery[-1]
    print('add', lottery)
    tx = fund_with_link(lottery.address)
    print(f'This is {tx}')

    #tx.wait(1)
    ending_transaction = lottery.end({'from':account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end()

