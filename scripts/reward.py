# try:
#     from deploy import get_crowdcoin, get_reward
# except ImportError:
#     from .deploy import get_crowdcoin, get_reward
import os
from brownie import *
import json


# ac1 = accounts[1]
# ac2 = accounts[2]
ac0 = '0x66aB6D9362d4F35596279692F0251Db635165871'
ac1 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
ac2 = '0x0063046686E46Dc6F15918b61AE2B121458534a5'
ac3 = '0x46C0a5326E643E4f71D3149d50B48216e174Ae84'

dev = accounts.add(os.getenv(config['wallets']['from_key']))
with open('./build/contracts/CrowdCoin.json') as f:
    c_abi = json.load(f)
    c_abi = c_abi['abi']

with open('./build/contracts/Reward.json') as f:
    r_abi = json.load(f)
    r_abi = r_abi['abi']

with open('./address.txt') as f:
    address = json.load(f)
    c_address = address['CROWDCOIN_ADDRESS']
    r_address = address['REWARD_ADDRESS']

crowdcoin = Contract.from_abi("CrowdCoin", c_address, c_abi)
reward = Contract.from_abi("Reward", r_address, r_abi)

def get_balance(account):
    '''
    get balance of crowdcoin of that account
    '''
    return crowdcoin.balanceOf(account)
    
def add_coin(purchase_add, amount):
    '''
    account purchase crowdcoin
    '''
    reward.purchase_coin(purchase_add, amount, {'from': dev})
    return crowdcoin.balanceOf(purchase_add)

def deduct_coin(claim_add, amount):
    '''
    account spent crowdcoin for claiming rewards
    '''
    reward.claim_gift(claim_add, amount, {'from': dev})
    return crowdcoin.balanceOf(claim_add)

def get_survey_info(public_key):
    '''
    fetch the main points of survey 
    '''
    info = {}
    info[public_key] = reward.get_survey_reward_by_key(public_key)
    return info[public_key]

def create_survey(survey_owner_address,
    survey_public_key,
    _budget,
    _target_number,
    _top_perform_threshold,
    _low_perform_threshold):
    '''
    create survey records
    '''
    reward.create_survey(survey_owner_address,
        survey_public_key,
        _budget,
        _target_number,
        _top_perform_threshold,
        _low_perform_threshold,
        {'from': dev})

def upload_checksum(survey_key, checksum):
    '''
    upload the checksum of survey rewards records text file to the chain
    '''
    log = reward.log_checksum(survey_key, checksum, {'from': dev})
    return log  #return transaction hash that can see the checksum on etherscan

def get_dp(add):
    return reward.get_dp_stacking(add)
    


def main():
    # reward.calculate_reward(ac3, 'PUBLIC_KEY', 23, {'from': dev})
    # reward.calculate_reward('0x33A4622B82D4c04a53e170c638B944ce27cffce3', 'PUBLIC_KEY', 70, {'from': dev})
    # reward.calculate_reward('0x0063046686E46Dc6F15918b61AE2B121458534a5', 'PUBLIC_KEY', 20, {'from': dev})
    # print(reward.get_dp_stacking(ac3))
    # reward.distribute_all_rewards({'from': dev})
    # print(get_balance(ac0))
    # print(get_balance(reward.address))
    # print(get_balance(ac1))
    # print(get_balance(ac2))
    # print(accounts[1])/
    # reward.create_survey(accounts[1], 'KEY', 9999, 100, 75, 40, {'from': dev})
    # result = reward.get_survey_reward_by_key('KEY', {'from': dev})
    # print(list(result)[1:])
    # answer = [accounts[1], 9999, 100, 75, 40, 99, 44, 1320]
    # print(answer[1:])
    # print(result == answer)
    # log = reward.log_checksum('PUBLIC_KEY', '@@@', "CHECKSUM", {'from': dev})
    # event = log.events['Log_checksum']['checksum']
    # print(event)
    # result = {'Log_checksum': [OrderedDict([('survey_key', 'PUBLIC_KEY'), ('space', '@@@'), ('checksum', 'CHECKSUM')])]}
    # print(result == event)
    print(get_dp('0x21b42413bA931038f35e7A5224FaDb065d297Ba3'))

    
