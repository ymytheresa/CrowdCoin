# README

## Prerequisites

### Crypto account

Install MetaMask extension on your web browser. \
Please go to the Q&A at the bottom part of this ReadMe for more details about the CrowdCoin setting up inside the wallet. \

### Infura io

Create account on Infura.io and get the infura project id and url for connecting to the mainnet or testnets. \

### Etherscan

Create account on Etherscan.io and get the etherscan token for automatic contract verification. \

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
Change the infura links to your own infura links \

## Compile contracts

```bash
cd CrowdCoin
brownie compile --all
```

## Deploy the contracts

Brownie supports different networks. \
Argument `--network` will take in a parameter that indicates the network you want to use. \
`rinkeby` = rinkeby testnet \
`development` = local ganache \

```bash
# Deploy to ganache
brownie run scripts/deploy.py --network development

# Deploy to rinkeby
brownie run scripts/deploy.py --network rinkeby
```

## Interact with contracts using CLI

CLI format \

```bash
python3 scripts/interact.py [command] [arguments]
```

### Get deployed contract addresses

command : `getcont` \

arguments : `all` \

Success Responses Content : \

```
{ "crowdcoin": $crowdcoin_contract_address, "reward": $reward_contract_address}
```

Sample call : \

```bash
python3 scripts/interact.py getcont all
```

### Get account balance of CrowdCoin

command : `getbal` \

arguments : $address \

Success Responses Content : \

````
{"adddress": $address, "balance": $address_balance}

Sample call : \
```bash
python3 scripts/interact.py getbal 0x66aB6D9362d4F35596279692F0251Db635165871
````

## Add Crowdcoin to address

command : `addcoin` \

arguments : $address, $amount \

Success Responses Content : \

````
{"adddress": $address, "balance": $address_balance_after_addcoin, "tx_hash": $transaction_hash}

Sample call : \
```bash
python3 scripts/interact.py addcoin 0x66aB6D9362d4F35596279692F0251Db635165871 100
````
