from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import Lottery, network, accounts, config, exceptions
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    #Act
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entrance_fee = lottery.getEntranceFee()
    #Assert
    assert expected_entrance_fee == entrance_fee

def test_cannot_enter():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        lottery = deploy_lottery()
        #Act / Assert
        with pytest.raises(exceptions.VirtualMachineError):
            lottery.enter_lottery({'from' : get_account(), 'value' :lottery.getEntranceFee()})


def test_can_enter():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        lottery =deploy_lottery()
        account = get_account()
        lottery.start_lottery({'from' : account})

        #act
        lottery.enter_lottery({'from' : account, 'value' : lottery.getEntranceFee()})
        #assert
        assert lottery.player(0) == account
