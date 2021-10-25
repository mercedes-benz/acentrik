
# Quickstart: Consume downloadable asset Flow (Fixed Rate Exchange)

This quickstart describes consuming downloadable asset flow.

It focuses on Bob's experience as a consumer

Here are the steps:

1.  Setup
2.  Bob buys data tokens
3.  Bob sends his datatoken to the service
4.  Bob downloads asset

Let's go through each step.

## 1. Setup

### Prerequisites
- Bob's Wallets have Consumer roles
- Dataset did
- Dataset token address
- Dataset token owner's wallet address

In the Python console:
```python
#create ocean instance
from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean
config = Config('config.ini')
ocean = Ocean(config)
 
print(f"ocean.exchange._exchange_address = '{ocean.exchange._exchange_address}'")
print(f"config.network_url = '{config.network_url}'")
print(f"config.block_confirmations = {config.block_confirmations.value}")
print(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
print(f"config.provider_url = '{config.provider_url}'")
 
 
from ocean_lib.web3_internal.currency import from_wei, to_wei
 
import os
from ocean_lib.web3_internal.wallet import Wallet
 
usdc_address = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b" # rinkeby usdc address  
#usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" # polygon usdc address
 
token_address =  "0x53406e3A470Cdbb3dEC62Af5064950FdE8f78938"
did = "did:op:53406e3A470Cdbb3dEC62Af5064950FdE8f78938"
data_token_owner_address ="0x9Bf750b5465a51689fA4235aAc1F37EC692ef7b4"
```

## 2. Bob buys data tokens
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
 
data_token = ocean.get_data_token(token_address)
 
logs = ocean.exchange.search_exchange_by_data_token(token_address)
fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=bob_wallet,
    max_OCEAN_amount=to_wei(10), # pay up to 10.0 OCEAN
    exchange_id=fre_exchange_id,
    data_token=token_address,
    exchange_owner=data_token_owner_address,
)
 
assert data_token.balanceOf(bob_wallet.address) >= 1.0, "Bob didn't get 1.0 datatokens"
print(f"data token in bob wallet = '{data_token.balanceOf(bob_wallet.address)}'")
```


## 3. Bob sends his datatoken to the service
In the same python console:
```python
# Bob points to the service object
 
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.common.agreements.service_types import ServiceTypes
asset = ocean.assets.resolve(did)
service = asset.get_service(ServiceTypes.ASSET_ACCESS)
 
# ============================================================================================
# Bob sends his datatoken to the service
 
quote = ocean.assets.order(asset.did, bob_wallet.address, service_index=service.index)
 
order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        quote.amount,
        quote.data_token_address,
        asset.did,
        service.index,
        ZERO_ADDRESS,
        bob_wallet,
        quote.computeAddress,
)
print(f"order_tx_id = '{order_tx_id}'")
```

## 4. Bob downloads asset
In the same python console:
```python
#If the connection breaks, Bob can request again by showing order_tx_id.
file_path = ocean.assets.download(
    asset.did,
    service.index,
    bob_wallet,
    order_tx_id,
    destination='./'
)
print(f"file_path = '{file_path}'") #e.g. datafile.0xAf07...
```
