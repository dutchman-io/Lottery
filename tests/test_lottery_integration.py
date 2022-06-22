from brownie import network
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from script.deploy_lottery import deploy_lottery
import time
def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        
        lottery = deploy_lottery()
        account = get_account
        lottery.start_lottery({'from' :account})
        lottery.enter_lottery({'from': account, lottery.getEntranceFee()})
        lottery.enter_lottery({'from': account, lottery.getEntranceFee()})
        lottery.enter_lottery({'from': account, lottery.getEntranceFee()})
        lottery.end({'from' : account})
        time.sleep(60)

        assert lottery.recentWinner() == account
        assert.balance == 0
