from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
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

def test_can_end():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        lottery =deploy_lottery()
        account = get_account()
        lottery.start_lottery({'from' : account})
        #Act
        lottery.enter_lottery({'from' : account, 'value' : lottery.getEntranceFee()})

        fund_with_link(lottery)
        lottery.end({'from' : account})

def test_pick_winner():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        
        lottery= deploy_lottery()
        account = get_account()
        lottery.start_lottery({'from' : account})
        lottery.enter_lottery({'from' : account, 'value' : lottery.getEntranceFee()})
        lottery.enter_lottery({'from' : get_account(index = 1), 'value' : lottery.getEntranceFee()}) 
        lottery.enter_lottery({'from' : get_account(index = 2), 'value' : lottery.getEntranceFee()})

        fund_with_link(lottery)
        transaction = lottery.end({'from' : account})
        request_id = transaction.events['RequestedRandomness']['requestId']
        STATIC_RNG = 777
        get_contract('vrd_coordinator').callbackWithRandomness(request_id, STATIC_RNG, lottery.address, {'from': address})
        #Assert
        ST_balance = account.balance()
        balance_of_lottery = lottery.balance()
        assert lottery.recentWinner() == account
        assert lottery.balance() ==0
        assert account.balance == ST_balance + balance_of_lottery
