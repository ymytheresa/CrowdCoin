import json
import os
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes as hb
import argparse

# ac1 = accounts[1]
# ac2 = accounts[2]
ac1 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
# ac2 = '0x0063046686E46Dc6F15918b61AE2B121458534a5'
# dev = accounts.add(os.getenv(config['wallets']['from_key']))
<<<<<<< Updated upstream
dev = '0x66aB6D9362d4F35596279692F0251Db635165871'
=======
# dev = '0x66aB6D9362d4F35596279692F0251Db635165871'
dev = os.getenv("PUBLIC_KEY")
# print(dev)
>>>>>>> Stashed changes

# infura_url = "https://rinkeby.infura.io/v3/9d9db26b6f8f47f5b3f2e04c8ca9f9fa"
# infura_url = 'https://ropsten.infura.io/v3/9d9db26b6f8f47f5b3f2e04c8ca9f9fa'
infura_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(infura_url))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)

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
    balance = crowdcoin.functions.balanceOf(account).call()
    # balance = web3.fromWei(balance, 'ether')
    return balance

def add_coin(purchase_add, amount):
    '''
    account purchase crowdcoin
    '''
    amount = int(amount)

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

def verify_purchase(sender_address, tx_hash):
    # log = web3.eth.getTransactionReceipt(tx_hash)
    transaction = web3.eth.get_transaction(tx_hash)
    recipient = crowdcoin.decode_function_input(transaction.input)[1]['recipient']
    amount = crowdcoin.decode_function_input(transaction.input)[1]['amount']
    from_address = transaction['from']
    if recipient == reward.address:
        if  from_address == sender_address:
            # return web3.fromWei(amount, 'ether')
            return amount
    return None
    # print(log)


FUNCTION_MAP = {
    'getbal': get_balance,
    'addcoin': add_coin,
    'getsur': get_survey_info,
    'mksur': create_survey,
    'upcheck': upload_checksum_get_hash,
    'verify': verify_purchase

}

# print(get_balance('0x724Ca58E1e6e64BFB1E15d7Eec0fe1E5f581c7bD'))
# print(add_coin(ac1, 100))
# print(upload_checksum('text', '123'))


parser = argparse.ArgumentParser()
parser.add_argument('command', choices=FUNCTION_MAP.keys())
parser.add_argument('revs', metavar='N', nargs='+', help='revisions')
args = parser.parse_args()
func = FUNCTION_MAP[args.command]

if func == get_balance or func == get_survey_info:
    print(func(args.revs[0]))
elif func == add_coin or func == upload_checksum_get_hash or func == verify_purchase:
    a = str(args.revs[0])
    b = str(args.revs[1])
    print(func(a,b))
elif func == create_survey:
    print(func(args.revs[0],args.revs[1],args.revs[2],args.revs[3],args.revs[4],args.revs[5]))

# print(func(args.integers))
# print(func == get_balance)
# print(type(args.revs[0]))
# print(type(args.revs[1]))
# print(type(args.revs[2]))

# create_survey(ac1, 'key', 100000, 1000, 50, 10)
# print(get_survey_info('key'))
# add_coin('0x66aB6D9362d4F35596279692F0251Db635165871', '123')
# print(get_balance(dev))