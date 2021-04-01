import json
import os
import web3
from web3 import Web3
import argparse

# ac1 = accounts[1]
# ac2 = accounts[2]
ac1 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
# ac2 = '0x0063046686E46Dc6F15918b61AE2B121458534a5'
# dev = accounts.add(os.getenv(config['wallets']['from_key']))
dev = '0x66aB6D9362d4F35596279692F0251Db635165871'

infura_url = "https://rinkeby.infura.io/v3/9d9db26b6f8f47f5b3f2e04c8ca9f9fa"
web3 = Web3(Web3.HTTPProvider(infura_url))

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

crowdcoin = web3.eth.contract(address=c_address, abi=c_abi)
reward = web3.eth.contract(address=r_address, abi=r_abi)

def get_balance(account):
    '''
    get balance of crowdcoin of that account
    '''
    return crowdcoin.functions.balanceOf(account).call()

FUNCTION_MAP = {
    'getbal': get_balance
}



parser = argparse.ArgumentParser()
parser.add_argument('command', choices=FUNCTION_MAP.keys())
parser.add_argument('integers', action='store')
args = parser.parse_args()
func = FUNCTION_MAP[args.command]
print(func(args.integers))
print(args.integers)
# print(func)
# print(args.integers)
print(get_balance(dev))
print(dev)

# my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

# my_parser = argparse.ArgumentParser()
# my_parser.add_argument('--input', action='store', type=int, required=True)
# my_parser.add_argument('--id', action='store', type=int)

# args = my_parser.parse_args()

# print(args.input)

# # Execute parse_args()
# args = my_parser.parse_args()

# print('If you read this line it means that you have provided '
#       'all the parameters')