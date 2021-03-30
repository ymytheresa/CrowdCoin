import os
from brownie import *
import json

dev = accounts.add(os.getenv(config['wallets']['from_key']))
reward = Reward.deploy({'from': dev})
crowdcoin = CrowdCoin.deploy({'from': dev})

def main():
    print('crowdcoin :', crowdcoin.address)
    print('reward :', reward.address)
    data = {}
    data['CROWDCOIN_ADDRESS'] = crowdcoin.address
    data['REWARD_ADDRESS'] = reward.address
    with open('address.txt', 'w') as outfile:
        json.dump(data, outfile)

    
    
    