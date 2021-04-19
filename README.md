# README

## Prerequisites

### Crypto account

Install MetaMask extension on your web browser. \
Please go to the Q&A at the bottom part of this ReadMe for more details about the CrowdCoin setting up inside the wallet.

### Infura io

Create account on Infura.io and get the infura project id and url for connecting to the mainnet or testnets.

### Etherscan

Create account on Etherscan.io and get the etherscan token for automatic contract verification.

## Package installation

```bash
pip3 install eth-brownie web3
brownie pm install OpenZeppelin/openzeppelin-contracts@3.0.0
```

If unable to run Brownie, you can try to install from source:

```bash
git clone https://github.com/eth-brownie/brownie.git
cd brownie
python3 setup.py install

pip3 install web3
brownie pm install OpenZeppelin/openzeppelin-contracts@3.0.0
```

## Environment variable

```bash
touch ~/.bash_profile
vim ~/.bash_profile
<!-- please add the following inside the vim: -->
<!-- export PUBLIC_KEY=$your_address
export PRIVATE_KEY=$your_address_private_key
export WEB3_INFURA_PROJECT_ID=$project_id_from_infura
export ETHERSCAN_TOKEN=$etherscan_token -->
source ~/.bash_profile
```

## Brownie supported networks configuration

Inside `brownie_config.yaml` \
Change the infura links to your own infura links

## Compile contracts

```bash
cd CrowdCoin
brownie compile --all
```

## Deploy the contracts

Brownie supports different networks. \
Argument `--network` will take in a parameter that indicates the network you want to use. \
`rinkeby` = rinkeby testnet \
`development` = local ganache

```bash
# Deploy to ganache
brownie run scripts/deploy.py --network development

# Deploy to rinkeby
brownie run scripts/deploy.py --network rinkeby
```

## Interact with contracts using CLI

CLI format

```bash
python3 scripts/interact.py [command] [arguments]
```

### Get deployed contract addresses

command : `getcont`

arguments : `all`

Sample call :

```bash
python3 scripts/interact.py getcont all
```

Success Responses Content :

```bash
{ "crowdcoin": $crowdcoin_contract_address, "reward": $reward_contract_address}
```

### Get account balance of CrowdCoin

command : `getbal`

arguments : `$address`

Sample call :

```bash
python3 scripts/interact.py getbal 0x66aB6D9362d4F35596279692F0251Db635165871
```

Success Responses Content :

```bash
{"adddress": $address, "balance": $address_balance}
```

## Add Crowdcoin to address

command : `addcoin`

restriction :
Only owner can perform this action

arguments : `$address, $amount`

Sample call :

```bash
python3 scripts/interact.py addcoin 0x66aB6D9362d4F35596279692F0251Db635165871 100
```

Success Responses Content :

```bash
{"adddress": $address, "balance": $address_balance_after_addcoin, "tx_hash": $transaction_hash}
```

## Create survey

command : `mksur`

arguments : `$survey_owner_address, $public_key_of_survey, $budget, $target_number_of_responses, $top_performance_threshold, $low_performance_threshold`

Sample call :

```bash
python3 scripts/interact.py mksur 0x33A4622B82D4c04a53e170c638B944ce27cffce3 KEY 9999 100 70 20
```

Success Responses Content :

```bash
{"tx_hash": $transaction_hash}
```

## Get survey information

command : `getsur`

arguments : `$public_key_of_survey`

Sample call :

```bash
python3 scripts/interact.py getsur KEY
```

Success Responses Content :

```bash
{
    "owner_address": $owner_address,
    "budget": $budget,
    "number": $target_number_of_responses,
    "top_threshold": $top_performance_threshold,
    "low_threshold": $low_performance_threshold,
    "max_reward": $maximum_reward_of_this_surveys
}
```

## Calculate reward for data providers who submitted data

command : `calcrew`

restriction :
Only owner can perform this action

arguments : `$data_provider_address, $public_key_of_survey, $his_performance_score`

Sample call :

```bash
python3 scripts/interact.py calcrew 0x66aB6D9362d4F35596279692F0251Db635165871 KEY 90
```

Success Responses Content :

```bash
{"tx_hash": $transaction_hash}
```

## Distribute all calculated rewards

command : `distrew`

restriction :
Only owner can perform this action

arguments : `all`

Sample call :

```bash
python3 scripts/interact.py distrew all
```

Success Responses Content :

```bash
{"tx_hash": $transaction_hash}
```

## Upload checksum

command : `upcheck`

arguments : `$public_key_of_survey, $checksum`

Sample call :

```bash
python3 scripts/interact.py upcheck KEY checksum
```

Success Responses Content :

```bash
{"survey_id": $public_key_of_survey, "checksum": $checksum, "tx_hash": $transaction_hash}
```

## Verify the amount of CrowdCoin received from address to our reward contract address

command : `verify`

arguments : `$address, $transaction_hash`

Sample call :

```bash
python3 scripts/interact.py verify 0x66aB6D9362d4F35596279692F0251Db635165871 0x2c7d403a2be07e5f55e343b8506dc7afdca3ae556dd242e9bb7d5210d93d46f9
```

Success Responses Content :

```bash
{"amount": $amount_received}
```

# Q&A

- How to add CrowdCoin to any crypto wallet ?

  1. Copy the CrowdCoin contract address
  2. Go to 'Assets' inside the wallet
  3. 'Add Tokens'
  4. Paste the address to 'Token Contract Address'
  5. 'Next'

- How to get transaction hash for sending CrowdCoin to reward contract address ?
  1. Copy reward contract address
  2. 'Send CWC' on the crypto wallet page
  3. Pate the address to 'Add Recipient'
  4. Enter the amount of CrowdCoin to be sent in 'Amount'
  5. 'Next' and 'Confirm'
  6. Go to wallet home page
  7. Go to 'Activity'
  8. Click the last transaction and click the copy button to copy the transaction hash to clipboard
