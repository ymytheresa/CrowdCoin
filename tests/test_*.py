from brownie import *
import brownie
import pytest


@pytest.fixture
def coin():
    return accounts[0].deploy(CrowdCoin)

@pytest.fixture
def reward(coin):
    reward = accounts[0].deploy(Reward)
    reward.set_coin(coin.address)
    return reward

def test_bal(coin, reward):
    assert coin.getBal(reward.address) == 10000000000000000000000000

def test_set(coin, reward):
    with brownie.reverts():
        reward.set_coin(coin.address)
        print('revert due to CrowdCoin is already minted')

def test_add_coin(reward):
    with brownie.reverts():
        reward.purchase_coin(accounts[1], 100, {'from': accounts[1]})

def test_add_coin_2(reward, coin):
    reward.purchase_coin(accounts[1], 100)
    assert coin.getBal(accounts[1]) == 100

def test_create_survey(reward):
    reward.create_survey(accounts[1], 'KEY', 9999, 100, 75, 40)
    result = list(reward.get_survey_reward_by_key('KEY'))[1:]
    answer = [9999, 100, 75, 40, 99, 44, 1320]
    assert result == answer

def test_calc_reward(reward):
    reward.calculate_reward(accounts[1], 'PUBLIC_KEY', 90)
    result = reward.get_dp_stacking(accounts[1])
    assert result == 10

def test_calc_reward_2(reward):
    reward.calculate_reward(accounts[1], 'PUBLIC_KEY', 70)
    result = reward.get_dp_stacking(accounts[1])
    assert result == 9

def test_calc_reward_3(reward):
    reward.calculate_reward(accounts[1], 'PUBLIC_KEY', 23)
    result = reward.get_dp_stacking(accounts[1])
    assert result == 1

def test_dist(reward, coin):
    reward.calculate_reward(accounts[1], 'PUBLIC_KEY', 90)
    reward.distribute_all_rewards()
    ac1 = coin.getBal(accounts[1])
    assert ac1 == 10

def test_dist_2(reward, coin):
    reward.calculate_reward(accounts[1], 'PUBLIC_KEY', 10)
    reward.distribute_all_rewards()
    ac1 = coin.getBal(accounts[1])
    assert ac1 == 0

def test_emit(reward):
    tx = reward.log_checksum('PUBLIC_KEY', '@@@', 'checksum')
    key = tx.events['Log_checksum']['survey_key']
    check = tx.events['Log_checksum']['checksum']
    first_check = (key == 'PUBLIC_KEY')
    second_check = (check == 'checksum')
    assert first_check == second_check
