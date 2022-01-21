# Quickstart: Consume Compute-to-Data Flow

This describes the flow when running a Compute-to-Data job, focusing on ConsumerA's experience as a Data Consumer on Acentrik Data Marketplace

Here are the steps:

1.  Setup
2.  ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)
3.  ConsumerA pay datatoken for the service
4.  ConsumerA starts a compute job
5.  ConsumerA monitors logs / output file

Let's go through each step.

## 1. Setup

### Prerequisites

- ConsumerA's Wallets have Consumer roles
- Asset Information Json file

Create an asset_info.json file and filled up the asset details

```
{
  "network": "https://matic-mainnet.chainstacklabs.com",
  "networkName": "polygon",
  "networkID": 137,
  "metadataCacheUri": "https://aquarius.acentrik.io",
  "providerUri": "https://provider.polygon.acentrik.io",
  "assetTokenAddress": "0x8748ef04C53974821F1174749c4B7A9486dbad19",
  "assetDid": "did:op:8748ef04C53974821F1174749c4B7A9486dbad19",
  "assetOwnerAddress": "0x2eCA8718b2fCaf0CF9E150ad4B44EE8c54473D2C",
  "algorithmTokenAddress": "0xe75a2Ca6D9b184d9807A1A1B5AE9BE57e9c897cD",
  "algorithmDid": "did:op:e75a2Ca6D9b184d9807A1A1B5AE9BE57e9c897cD",
  "algorithmOwnerAddress": "0x500DB43EE6966e6213BA58EAF152dA593EB7432e"
}
```

<br />

![Copy info clipboard](./copy_info_clipboard.gif)

<em>Copy the asset details from Acentrik developer details section</em>

<br />

In the Python console:

```python
#create ocean instance
from web3.main import Web3
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.currency import from_wei, to_wei
from ocean_lib.config import Config
from ocean_lib.models.dispenser import DispenserContract
from ocean_lib.web3_internal.contract_utils import get_contracts_addresses
import json

print(f"ocean.exchange._exchange_address = '{ocean.exchange._exchange_address}'")
print(f"config.network_url = '{config.network_url}'")
print(f"config.block_confirmations = {config.block_confirmations.value}")
print(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
print(f"config.provider_url = '{config.provider_url}'")

config = Config('config.ini')
ocean = Ocean(config)
import os
from ocean_lib.web3_internal.wallet import Wallet

# Read asset_info.json file
asset_info = open('asset_info.json')
data_asset_info = json.load(asset_info)
asset_info.close()

DATA_did = data_asset_info["assetDid"]
data_token_address =  data_asset_info["assetTokenAddress"]
data_token_owner_address = data_asset_info["assetOwnerAddress"]

ALG_did = data_asset_info["algorithmDid"]
algo_token_address = data_asset_info["algorithmTokenAddress"]
algo_token_owner_address = data_asset_info["algorithmOwnerAddress"]
```

<br />

## 2. ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)

### If the Asset is Fixed Price

In the same python console (Fixed Pricing Asset):

```python
consumer_A_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY2'), config.block_confirmations,  config.transaction_timeout)

# ============================================================================================
# ConsumerA buys data tokens

data_token = ocean.get_data_token(data_token_address)
logs = ocean.exchange.search_exchange_by_data_token(data_token_address)
data_fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=consumer_A_wallet,
    max_OCEAN_amount=to_wei(25), # pay up to 25.0 USDC
    exchange_id=data_fre_exchange_id,
    data_token=data_token_address,
    exchange_owner=data_token_owner_address,
)

assert data_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"data token in ConsumerA wallet = '{data_token.balanceOf(consumer_A_wallet.address)}'")

# ============================================================================================
# ConsumerA buys algo tokens

algo_token = ocean.get_data_token(algo_token_address)
logs = ocean.exchange.search_exchange_by_data_token(algo_token_address)
algo_fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=consumer_A_wallet,
    max_OCEAN_amount=to_wei(25), # pay up to 25.0 USDC
    exchange_id=algo_fre_exchange_id,
    data_token=data_token_address,
    exchange_owner=algo_token_owner_address,
)

assert algo_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"algo token in ConsumerA wallet = '{algo_token.balanceOf(consumer_A_wallet.address)}'")
```

<br />

### If the Asset is Free Price

In the same python console (Free Pricing Asset):

```python
consumer_A_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY2'), config.block_confirmations,  config.transaction_timeout)

# ============================================================================================
# ConsumerA dispense data tokens

data_token = ocean.get_data_token(data_token_address)

contracts_addresses = get_contracts_addresses(config.network_name, config.address_file)
assert contracts_addresses, "invalid network."

dispenser_address = contracts_addresses["Dispenser"]
dispenser = DispenserContract(consumer_A_wallet.web3, dispenser_address)
assert dispenser.is_active(data_token_address), f"dispenser is not active for {data_token_address} data token. It its not free priced. "

#Dispense
tx_result = dispenser.dispense(data_token_address, to_wei(1), consumer_A_wallet)
assert tx_result, "failed to dispense data tokens."
print(f"tx_result = '{tx_result}'")

assert data_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"data token in ConsumerA wallet = '{data_token.balanceOf(consumer_A_wallet.address)}'")

# ============================================================================================
# ConsumerA dispense algo tokens

algo_token = ocean.get_data_token(algo_token_address)

assert dispenser.is_active(algo_token_address), f"dispenser is not active for {algo_token_address} algo token. It its not free priced. "

#Dispense
tx_result = dispenser.dispense(algo_token_address, to_wei(1), consumer_A_wallet)
assert tx_result, "failed to dispense algo tokens."
print(f"tx_result = '{tx_result}'")


assert algo_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"algo token in ConsumerA wallet = '{algo_token.balanceOf(consumer_A_wallet.address)}'")
```

<br />

## 3. ConsumerA pay datatoken for the service

In the same python console:

```python
DATA_DDO = ocean.assets.resolve(DATA_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
ALG_DDO = ocean.assets.resolve(ALG_did)

compute_service = DATA_DDO.get_service('compute')
algo_service = ALG_DDO.get_service('access')

from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.models.compute_input import ComputeInput

# order & pay for dataset
dataset_order_requirements = ocean.assets.order(
    DATA_did, consumer_A_wallet.address, service_type=compute_service.type
)
DATA_order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        dataset_order_requirements.amount,
        dataset_order_requirements.data_token_address,
        DATA_did,
        compute_service.index,
        ZERO_ADDRESS,
        consumer_A_wallet,
        dataset_order_requirements.computeAddress,
    )
print(f"DATA_order_tx_id: {DATA_order_tx_id}")

# order & pay for algo
algo_order_requirements = ocean.assets.order(
    ALG_did, consumer_A_wallet.address, service_type=algo_service.type
)
ALG_order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        algo_order_requirements.amount,
        algo_order_requirements.data_token_address,
        ALG_did,
        algo_service.index,
        ZERO_ADDRESS,
        consumer_A_wallet,
        algo_order_requirements.computeAddress,
)
print(f"ALG_order_tx_id: {ALG_order_tx_id}")

```

<br />

## 4. ConsumerA starts a compute job

In the same python console:

```python
# run job
compute_inputs = [ComputeInput(DATA_did, DATA_order_tx_id, compute_service.index)]
job_id = ocean.compute.start(
    compute_inputs,
    consumer_A_wallet,
    algorithm_did=ALG_did,
    algorithm_tx_id=ALG_order_tx_id,
    algorithm_data_token=algo_token_address
)
print(f"Started compute job with id: {job_id}")
```

<br />

## 5. ConsumerA monitors logs / algorithm output

In the same python console:

```python
# ConsumerA check job status
print(ocean.compute.status(DATA_did, job_id, consumer_A_wallet))

# ============================================================================================
# ConsumerA get result (After job finished)

result_file = ocean.compute.result_file(DATA_did, job_id, 0, consumer_A_wallet)  # 0 index, means we retrieve the results from the first dataset index
print(result_file)
```
