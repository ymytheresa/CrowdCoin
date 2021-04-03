import json
import os
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes as hb
import argparse

dev = os.getenv("PUBLIC_KEY")
dev_priv = os.getenv("PRIVATE_KEY")
web3.eth.default_account = dev

infura_url = "https://rinkeby.infura.io/v3/9d9db26b6f8f47f5b3f2e04c8ca9f9fa" #if rinkeby
# infura_url = "http://127.0.0.1:7545" #if ganache
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

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

def get_tx(contract):
    nonce = web3.eth.getTransactionCount(dev)
    tx = {
        'nonce': nonce,
        'to': contract,
        'value': 0,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    return tx

def sign_tx(tx):
    signed = web3.eth.account.signTransaction(tx, dev_priv)
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    return hb.hex(tx_hash)

def get_balance(account):
    '''
    get balance of crowdcoin of that account
    '''
    balance = crowdcoin.functions.balanceOf(account).call()
    if infura_url != "http://127.0.0.1:7545":
        balance = web3.fromWei(balance, 'ether') #if on testnet
    return balance

def add_coin_get_bal(purchase_add, amount):
    result = web3.eth.waitForTransactionReceipt((add_coin(purchase_add, amount))) 
    return get_balance(purchase_add)

def add_coin(purchase_add, amount):
    '''
    account purchase crowdcoin
    '''
    amount = int(amount)
    if infura_url != "http://127.0.0.1:7545":
        amount = web3.toWei(amount, 'ether')
    tx = get_tx(reward.address)
    tx['data'] = reward.encodeABI(fn_name='purchase_coin', args=[purchase_add, amount])
    # sign_tx(tx)
    return sign_tx(tx)

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
    tx = get_tx(reward.address)
    _budget = int(_budget)
    _target_number = int(_target_number)
    _top_perform_threshold = int(_top_perform_threshold)
    _low_perform_threshold = int(_low_perform_threshold)

    tx['data'] = reward.encodeABI(fn_name='create_survey', args=[survey_owner_address,
                                                                    survey_public_key,
                                                                    _budget,
                                                                    _target_number,
                                                                    _top_perform_threshold,
                                                                    _low_perform_threshold,])
    return sign_tx(tx)

def upload_checksum(survey_id, checksum):
    '''
    upload the checksum of survey rewards records text file to the chain
    '''
    tx = get_tx(reward.address)
    separator = '@@@OMIT@@@'
    tx['data'] = reward.encodeABI(fn_name='log_checksum', args=[survey_id, separator, checksum])
    return sign_tx(tx)

def upload_checksum_get_hash(survey_id, checksum):
    result = web3.eth.waitForTransactionReceipt((upload_checksum(survey_id, checksum)))
    return hb.hex(result['transactionHash'])

def verify_purchase(sender_address, tx_hash):
    # log = web3.eth.getTransactionReceipt(tx_hash)
    transaction = web3.eth.get_transaction(tx_hash)
    recipient = crowdcoin.decode_function_input(transaction.input)[1]['recipient']
    amount = crowdcoin.decode_function_input(transaction.input)[1]['amount']
    from_address = transaction['from']
    if recipient == reward.address:
        if from_address == sender_address:
            if infura_url != "http://127.0.0.1:7545":
                return web3.fromWei(amount, 'ether')
            return amount
    return None

def calc_reward(address, survey_id, score):
    score = int(score)
    tx = get_tx(reward.address)
    tx['data'] = reward.encodeABI(fn_name='calculate_reward', args=[address, survey_id, score])
    return sign_tx(tx)

def distribute_reward():
    tx = get_tx(reward.address)
    tx['data'] = reward.encodeABI(fn_name='distribute_all_rewards', args=[])
    return sign_tx(tx)

FUNCTION_MAP = {
    'getbal': get_balance,
    'addcoin': add_coin_get_bal,
    'getsur': get_survey_info,
    'mksur': create_survey,
    'upcheck': upload_checksum_get_hash,
    'verify': verify_purchase,
    'calcrew': calc_reward,
    'distrew': distribute_reward
}

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=FUNCTION_MAP.keys())
parser.add_argument('revs', metavar='N', nargs='+', help='revisions')
args = parser.parse_args()
func = FUNCTION_MAP[args.command]

if func == distribute_reward:
    print(func())
elif func == get_balance or func == get_survey_info:
    print(func(args.revs[0]))
elif func == add_coin_get_bal or func == upload_checksum_get_hash or func == verify_purchase:
    print(func(args.revs[0],args.revs[1]))
elif func == calc_reward:
    print(func(args.revs[0],args.revs[1],args.revs[2]))
elif func == create_survey:
    print(func(args.revs[0],args.revs[1],args.revs[2],args.revs[3],args.revs[4],args.revs[5]))
