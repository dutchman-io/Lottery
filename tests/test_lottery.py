from scripts.deploy_lottery import deploy_lottery
from brownie import Lottery, network, accounts, config
from web3 import Web3


def test_get_entrance_fee():
    #Arrange
    lottery = deploy_lottery()
    #Act
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entrance_fee = lottery.getEntranceFee()
    #Assert
    assert(expected_entrance_fee == entrance_fee)
