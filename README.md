# README

## Environment variable

1. Private key of the contract owner address
   `export PRIVATE_KEY=$your_address_private_key`
2. Infura project id
   `export WEB3_INFURA_PROJECT_ID=$project_id_from_infura`
3. Testnet host address from Infura
   Change the host address inside `brownie_config.yaml` under the testnet name
4. Use ganache-cli instead of ganache gui app
   Change the host and port of `cmd_settings` inside `brownie_config.yaml`

## Package installation

1. eth-brownie
   `pip3 install eth-brownie'

## Compile contracts

1. Enter the directory
   `cd CrowdCoin`
2. Compile
   `brownie compile -all`

## Deploy the contracts

1. Under ganache
   `brownie run scripts/deploy.py --network development`
   The contract addresses and abi are stored in `address.txt` and `/build/contracts` for contract call uses

2. Under rinkeby
   `brownie run scripts/deploy.py --network rinkeby`

## Interact with contracts

1. call functions within `def main()` inside `reward.py`

2. Under ganache. If under rinkeby just the same as the above
   `brownie run scripts/reward.py --network development`
