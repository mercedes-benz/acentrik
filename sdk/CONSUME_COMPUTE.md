
# Quickstart: Consume Compute-to-Data Flow (Fixed Rate Exchange)

This quickstart describes consuming Compute-to-Data flow.

It focuses on Bob's experience as a consumer

Here are the steps:

1.  Setup
2.  Bob buys data tokens (for data and algorithm)
3.  Bob sends his datatoken to the service
4.  Bob starts a compute job
5.  Bob monitors logs / algorithm output

Let's go through each step.

## 1. Setup

### Prerequisites
- Bob's Wallets have Consumer roles
- Dataset & Algo did
- Dataset & Algo token address
- Dataset & Algo token owner's wallet address

In the Python console:
```python
#create ocean instance
from web3.main import Web3
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.currency import from_wei, to_wei
from ocean_lib.config import Config
 
print(f"ocean.exchange._exchange_address = '{ocean.exchange._exchange_address}'")
print(f"config.network_url = '{config.network_url}'")
print(f"config.block_confirmations = {config.block_confirmations.value}")
print(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
print(f"config.provider_url = '{config.provider_url}'")
 
config = Config('config.ini')
ocean = Ocean(config)
import os
from ocean_lib.web3_internal.wallet import Wallet
 
usdc_address = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b" # rinkeby usdc address
#usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" # polygon usdc address
 
DATA_did = "did:op:Dd02a7b29B5C654378d39DCc9532aB3B5a77BD8a"
data_token_address =  "0xDd02a7b29B5C654378d39DCc9532aB3B5a77BD8a"
data_token_owner_address = "0x9Bf750b5465a51689fA4235aAc1F37EC692ef7b4"
 
ALG_did = "did:op:b4C10A8767269F6Da1C5701e11e7EBE2E9303F05"
algo_token_address = "0xb4C10A8767269F6Da1C5701e11e7EBE2E9303F05"
algo_token_owner_address = "0x500DB43EE6966e6213BA58EAF152dA593EB7432e"
```

## 2. Bob buys data tokens (for data and algorithm)
In the same python console:
```python
# Check bob have enough ETH & USDC
 
bob_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY2'), config.block_confirmations,  config.transaction_timeout)
 
from ocean_lib.models.btoken import BToken #BToken is ERC20
USDC_token = BToken(ocean.web3, usdc_address)
 
#Verify that Bob has USDC
assert USDC_token.balanceOf(bob_wallet.address) > 0, "need USDC"
 
#Verify that Bob has ETH
assert ocean.web3.eth.get_balance(bob_wallet.address) > 0, "need ETH"
 
# ============================================================================================
# Bob buys data tokens
 
data_token = ocean.get_data_token(data_token_address)
logs = ocean.exchange.search_exchange_by_data_token(data_token_address)
data_fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=bob_wallet,
    max_OCEAN_amount=to_wei(25), # pay up to 25.0 OCEAN
    exchange_id=data_fre_exchange_id,
    data_token=data_token_address,
    exchange_owner=data_token_owner_address,
)
 
assert data_token.balanceOf(bob_wallet.address) >= 1.0, "Bob didn't get 1.0 datatokens"
print(f"data token in bob wallet = '{data_token.balanceOf(bob_wallet.address)}'")
 
# ============================================================================================
# Bob buys algo tokens
 
algo_token = ocean.get_data_token(algo_token_address)
logs = ocean.exchange.search_exchange_by_data_token(algo_token_address)
algo_fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=bob_wallet,
    max_OCEAN_amount=to_wei(25), # pay up to 25.0 OCEAN
    exchange_id=algo_fre_exchange_id,
    data_token=data_token_address,
    exchange_owner=algo_token_owner_address,
)
 
assert algo_token.balanceOf(bob_wallet.address) >= 1.0, "Bob didn't get 1.0 datatokens"
print(f"algo token in bob wallet = '{algo_token.balanceOf(bob_wallet.address)}'")
```


## 3. Bob sends his datatoken to the service
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
    DATA_did, bob_wallet.address, service_type=compute_service.type
)
DATA_order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        dataset_order_requirements.amount,
        dataset_order_requirements.data_token_address,
        DATA_did,
        compute_service.index,
        ZERO_ADDRESS,
        bob_wallet,
        dataset_order_requirements.computeAddress,
    )
print(f"DATA_order_tx_id: {DATA_order_tx_id}")

# order & pay for algo
algo_order_requirements = ocean.assets.order(
    ALG_did, bob_wallet.address, service_type=algo_service.type
)
ALG_order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        algo_order_requirements.amount,
        algo_order_requirements.data_token_address,
        ALG_did,
        algo_service.index,
        ZERO_ADDRESS,
        bob_wallet,
        algo_order_requirements.computeAddress,
)
print(f"ALG_order_tx_id: {ALG_order_tx_id}")

```

## 4. Bob starts a compute job
In the same python console:
```python
# run job
compute_inputs = [ComputeInput(DATA_did, DATA_order_tx_id, compute_service.index)]
job_id = ocean.compute.start(
    compute_inputs,
    bob_wallet,
    algorithm_did=ALG_did,
    algorithm_tx_id=ALG_order_tx_id,
    algorithm_data_token=algo_token_address
)
print(f"Started compute job with id: {job_id}")
```

## 5. Bob monitors logs / algorithm output
In the same python console:
```python
# Bob check job status
print(ocean.compute.status(DATA_did, job_id, bob_wallet))
 
# ============================================================================================
# Bob get result (After job finished)
 
result_file = ocean.compute.result_file(DATA_did, job_id, 0, bob_wallet)  # 0 index, means we retrieve the results from the first dataset index
print(result_file)
```