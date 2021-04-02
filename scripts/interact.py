import json
import os
import web3
from web3 import Web3
from hexbytes import HexBytes as hb
import argparse

# ac1 = accounts[1]
# ac2 = accounts[2]
ac1 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
# ac2 = '0x0063046686E46Dc6F15918b61AE2B121458534a5'
# dev = accounts.add(os.getenv(config['wallets']['from_key']))
dev = '0x66aB6D9362d4F35596279692F0251Db635165871'

# infura_url = "https://rinkeby.infura.io/v3/9d9db26b6f8f47f5b3f2e04c8ca9f9fa"
infura_url = "http://127.0.0.1:7545"
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

def add_coin(purchase_add, amount):
    '''
    account purchase crowdcoin
    '''
    reward.functions.purchase_coin(purchase_add, amount).transact({'from': dev})
    return crowdcoin.functions.balanceOf(purchase_add).call()

def get_survey_info(public_key):
    '''
    fetch the main points of survey 
    '''
    info = {}
    info[public_key] = reward.functions.get_survey_reward_by_key(public_key).call()
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
    reward.functions.create_survey(survey_owner_address,
        survey_public_key,
        _budget,
        _target_number,
        _top_perform_threshold,
        _low_perform_threshold,
    ).transact({'from': dev})

def upload_checksum(survey_key, checksum):
    '''
    upload the checksum of survey rewards records text file to the chain
    '''
    log = reward.functions.log_checksum(survey_key, checksum).transact({'from': dev})
    return log 

def upload_checksum_get_hash(survey_key, checksum):
    result = web3.eth.waitForTransactionReceipt((upload_checksum(survey_key, checksum)))
    return hb.hex(result['transactionHash'])

# print(get_balance(reward.address))
# print(upload_checksum('public_key', 'checksum123'))
# result = web3.eth.waitForTransactionReceipt((upload_checksum('public_key', 'checksum123')))
# print(hb.hex(result['transactionHash']))
print(upload_checksum_get_hash('test','123'))
# print(result['logs'][0]['data'])

# hex_string = result['logs'][0]['data']
# print(bytes.fromhex(hex_string).decode('utf-8'))

# bytes_object = bytes.fromhex(hex_string)
# ascii_string = bytes_object.decode("ASCII")
# print(ascii_string)
FUNCTION_MAP = {
    'getbal': get_balance
}
# parser = argparse.ArgumentParser()
# parser.add_argument('command', choices=FUNCTION_MAP.keys())
# parser.add_argument('-integers', action='store')
# parser.add_argument('-a', action='store')

# # NOW MUST NEED ONE AND ONLY ONE COMMAND TO RUN THE PROG
# # BUT CAN HAVE OPTIONAL PARAM

# args = parser.parse_args()
# # func = FUNCTION_MAP[args.command]
# # print(func(args.integers))
# print(args.integers)

# print(get_balance(dev))
# print(dev)