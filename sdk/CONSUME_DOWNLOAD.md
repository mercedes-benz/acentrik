# Quickstart: Consume downloadable asset Flow

This describes the flow when consuming a downloadable asset, focusing on ConsumerA's experience as a Data Consumer on Acentrik Data Marketplace:

Here are the steps:

1.  Setup
2.  ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)
3.  ConsumerA pay datatoken for the service
4.  ConsumerA downloads asset

<br />

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
  "assetTokenAddress": "0x53406e3A470Cdbb3dEC62Af5064950FdE8f78938",
  "assetDid": "did:op:53406e3A470Cdbb3dEC62Af5064950FdE8f78938",
  "assetOwnerAddress": "0x9Bf750b5465a51689fA4235aAc1F37EC692ef7b4"
}
```

<br />

![Copy info clipboard](./copy_info_clipboard.gif)

<em>Copy the asset details from Acentrik developer details section</em>

<br />

In the Python console:

```python

#create ocean instance
from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean
config = Config('config.ini')
ocean = Ocean(config)
from ocean_lib.models.dispenser import DispenserContract
from ocean_lib.web3_internal.contract_utils import get_contracts_addresses
import json

print(f"ocean.exchange._exchange_address = '{ocean.exchange._exchange_address}'")
print(f"config.network_url = '{config.network_url}'")
print(f"config.block_confirmations = {config.block_confirmations.value}")
print(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
print(f"config.provider_url = '{config.provider_url}'")


from ocean_lib.web3_internal.currency import from_wei, to_wei
import os
from ocean_lib.web3_internal.wallet import Wallet

# Read asset_info.json file
asset_info = open('asset_info.json')
data_asset_info = json.load(asset_info)
asset_info.close()

token_address =  data_asset_info["assetTokenAddress"]
did = data_asset_info["assetDid"]
data_token_owner_address = data_asset_info["assetOwnerAddress"]
```

<br />

## 2. ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)

### If the Asset is Fixed Price

In the same python console (Fixed Pricing Asset):

```python

consumer_A_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY2'), config.block_confirmations,  config.transaction_timeout)

# ============================================================================================
# ConsumerA buys data tokens (Fixed)

data_token = ocean.get_data_token(token_address)

logs = ocean.exchange.search_exchange_by_data_token(token_address)
fre_exchange_id = logs[0].args.exchangeId
ocean.exchange.buy_at_fixed_rate(
    amount=to_wei(1), # buy 1.0 datatoken
    wallet=consumer_A_wallet,
    max_OCEAN_amount=to_wei(10), # pay up to 10.0 USDC
    exchange_id=fre_exchange_id,
    data_token=token_address,
    exchange_owner=data_token_owner_address,
)

assert data_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"data token in ConsumerA wallet = '{data_token.balanceOf(consumer_A_wallet.address)}'")
```

<br />

### If the Asset is Free Price

In the same python console (Free Pricing Asset):

```python
consumer_A_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY2'), config.block_confirmations,  config.transaction_timeout)

# ============================================================================================
# ConsumerA dispense data tokens (Free)
data_token = ocean.get_data_token(token_address)

contracts_addresses = get_contracts_addresses(config.network_name, config.address_file)
assert contracts_addresses, "invalid network."

dispenser_address = contracts_addresses["Dispenser"]
dispenser = DispenserContract(consumer_A_wallet.web3, dispenser_address)
assert dispenser.is_active(token_address), f"dispenser is not active for {token_address} data token. It its not free priced. "

#Dispense
tx_result = dispenser.dispense(token_address, to_wei(1), consumer_A_wallet)
assert tx_result, "failed to dispense data tokens."
print(f"tx_result = '{tx_result}'")

assert data_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"data token in ConsumerA wallet = '{data_token.balanceOf(consumer_A_wallet.address)}'")

```

<br />

## 3. ConsumerA pay datatoken for the service

In the same python console:

```python
# ConsumerA points to the service object

from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.common.agreements.service_types import ServiceTypes
asset = ocean.assets.resolve(did)
service = asset.get_service(ServiceTypes.ASSET_ACCESS)

# ============================================================================================
# ConsumerA sends his datatoken to the service

quote = ocean.assets.order(asset.did, consumer_A_wallet.address, service_index=service.index)

order_tx_id = ocean.assets.pay_for_service(
        ocean.web3,
        quote.amount,
        quote.data_token_address,
        asset.did,
        service.index,
        ZERO_ADDRESS,
        consumer_A_wallet,
        quote.computeAddress,
)
print(f"order_tx_id = '{order_tx_id}'")

assert data_token.balanceOf(consumer_A_wallet.address) >= 1.0, "ConsumerA didn't get 1.0 datatokens"
print(f"data token in ConsumerA wallet = '{data_token.balanceOf(consumer_A_wallet.address)}'")
```

<br />

## 4. ConsumerA downloads asset

In the same python console:

```python
#If the connection breaks, ConsumerA can request again by showing order_tx_id.
file_path = ocean.assets.download(
    asset.did,
    service.index,
    consumer_A_wallet,
    order_tx_id,
    destination='./'
)
print(f"file_path = '{file_path}'") #e.g. datafile.0xAf07...
```
