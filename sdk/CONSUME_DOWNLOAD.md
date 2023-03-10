# Quickstart: Consume downloadable asset Flow

This describes the flow when consuming a downloadable asset, focusing on ConsumerA's experience as a Data Consumer on Acentrik Data Marketplace:

Here are the steps:

1.  Setup
2.  ConsumerA Approve Data Token
3.  ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)
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
  "network": "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
  "networkName": "goerli",
  "networkID": 5,
  "aquariusUri": "https://v1.aquarius.dev.acentrik.io",
  "assetProviderUri": "https://v1.provider.goerli.dev.acentrik.io",
  "assetDid": "did:op:7cec0d397a24d38933cbf25a442cb426329fdb220c1b3e206e7545889e521173",
  "assetTokenAddress": "0xea1122E1Be1104Ac73732a98a7d6C84cf6476d98",
  "assetOwnerAddress": "0xd1CdD6182f86456712e49Eea0C03aF5A1375E8Ec",
  "assetBaseTokenAddress": "0x07865c6e87b9f70255377e024ace6630c1eaa37f"
}
```

<br />

![Copy info clipboard](./copy_info_clipboard.gif)

<em>Copy the asset details from Acentrik developer details section</em>

<br />

In the Python console:

```python
from web3.main import Web3
import json

# Read asset_info.json file
asset_info = open('asset_info.json')
data_asset_info = json.load(asset_info)
asset_info.close()
token_address =  data_asset_info["assetTokenAddress"]
did = data_asset_info["assetDid"]
data_token_owner_address = data_asset_info["assetOwnerAddress"]
base_token_address = data_asset_info["assetBaseTokenAddress"]
aquarius_uri = data_asset_info["aquariusUri"]
asset_provider_uri = data_asset_info["assetProviderUri"]


# Create Ocean instance
from ocean_lib.web3_internal.utils import connect_to_network
connect_to_network("goerli")
import os
from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean
config = get_config_dict("goerli")

config['METADATA_CACHE_URI'] = aquarius_uri
config['PROVIDER_URL'] = asset_provider_uri

ocean = Ocean(config)
from ocean_lib.models.datatoken2 import Datatoken2
from ocean_lib.models.datatoken_base import DatatokenBase, TokenFeeInfo
from brownie.network import accounts
print(f"config.metadata_cache_uri = {config['METADATA_CACHE_URI']}")
print(f"config.provider_url = {config['PROVIDER_URL']}")

# configure gas
from brownie.network.gas.strategies import GasNowStrategy
from brownie import network
gas_strategy = GasNowStrategy("fast")
network.gas_limit("auto")
network.gas_price("auto")
```

<br />

## 2. Approve tokens for consumer_A

In the same python console (Fixed Pricing Asset):

```python
## USDC Token Address for Goerli Network
USDC_token = DatatokenBase(config, Web3.toChecksumAddress("0x07865c6E87B9F70255377e024ace6630C1Eaa37F"))
erc20_enterprise_token = Datatoken2(config, Web3.toChecksumAddress(token_address))
accounts.clear()
consumer_private_key = os.getenv('TEST_PRIVATE_KEY1')
consumer_A_wallet = accounts.add(consumer_private_key)
print(f"================")
print(f"consumer_A_wallet.address = '{consumer_A_wallet.address}'")

# Get a list exchange addresses and ids with a given datatoken and exchange owner.
datatoken_address = token_address
nft_factory = ocean.data_nft_factory
exchange_addresses_and_ids = nft_factory.search_exchange_by_datatoken(ocean.fixed_rate_exchange, token_address, exchange_owner=data_token_owner_address)
assert (
    exchange_addresses_and_ids
), f"No exchanges found. datatoken_address = {datatoken_address}, exchange_owner = {data_token_owner_address}."
print(exchange_addresses_and_ids)
exchange_address = exchange_addresses_and_ids[0][0]
exchange_id = exchange_addresses_and_ids[0][1]
fixed_price_address = ocean.fixed_rate_exchange


# Approve tokens for consumer_A
USDC_token.approve(token_address,  Web3.toWei(1000, "ether"), {"from": consumer_A_wallet})
erc20_enterprise_token.approve(token_address,  Web3.toWei(1000, "ether"), {"from": consumer_A_wallet})
```

<br />

## 3. ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)

In the same python console (Fixed Pricing Asset):

```python
asset = ocean.assets.resolve(did)
access_service = asset.services[0]

provider_fee = ocean.retrieve_provider_fees(ddo=asset, access_service=access_service, publisher_wallet=consumer_A_wallet)
consume_market_fees=TokenFeeInfo(
            address=consumer_A_wallet.address,
            token=USDC_token.address,
            amount=0,
        )

from ocean_lib.models.fixed_rate_exchange import FixedRateExchange, OneExchange
fre_exchange = FixedRateExchange(config, ocean.fixed_rate_exchange.contract.address)
one_exchange = OneExchange(fre_exchange, exchange_id)

tx = erc20_enterprise_token.buy_DT_and_order(
        provider_fees=provider_fee,
        exchange=one_exchange,
        service_index=0,
        consume_market_fees=consume_market_fees,
        max_base_token_amount= Web3.toWei(20, "ether"),
        consume_market_swap_fee_amount=Web3.toWei(0.001, "ether"),   # 1e15 => 0.1%
        consume_market_swap_fee_address=consumer_A_wallet.address,
        tx_dict={"from": consumer_A_wallet},
    )
```

<br />

### If the Asset is Free Price

In the same python console (Free Pricing Asset):

```python
asset = ocean.assets.resolve(did)
access_service = asset.services[0]
provider_fee = ocean.retrieve_provider_fees(ddo=asset, access_service=access_service, publisher_wallet=consumer_A_wallet)
consume_market_fees=TokenFeeInfo(
            address=consumer_A_wallet.address,
            token=erc20_enterprise_token.address,
            amount=0,
        )

tx = erc20_enterprise_token.dispense_and_order(
    provider_fees=provider_fee,
    tx_dict={"from": consumer_A_wallet},
    service_index=0,
    consume_market_fees=consume_market_fees,
)
```

<br />

## 4. ConsumerA downloads asset

### ⚠️ Disclaimer

Please reuse a transaction ID if its not expired, so you wont be paying for the transaction fee again.
You can get your previous transaction on a dataToken using the method `erc20_enterprise_token.get_start_order_logs()` & just consume the asset using the transaction id, it will check if the asset is still consumable.

In the same python console:

```python
file_path = ocean.assets.download_asset(
    ddo=asset,
    consumer_wallet=consumer_A_wallet,
    destination='./',
    order_tx_id=tx.txid,
    service=access_service,
)
print(file_path)
```
