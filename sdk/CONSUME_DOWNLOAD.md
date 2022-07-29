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
  "network": "https://matic-mainnet.chainstacklabs.com",
  "networkName": "polygon",
  "networkID": 137,
  "metadataCacheUri": "https://aquarius.acentrik.io",
  "providerUri": "https://provider.polygon.acentrik.io",
  "assetTokenAddress": "0x53406e3A470Cdbb3dEC62Af5064950FdE8f78938",
  "assetDid": "did:op:53406e3A470Cdbb3dEC62Af5064950FdE8f78938",
  "assetOwnerAddress": "0x9Bf750b5465a51689fA4235aAc1F37EC692ef7b4",
  "baseTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
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
from ocean_lib.models.datatoken_enterprise import DatatokenEnterprise
import json

# print(f"ocean.exchange._exchange_address = '{ocean.exchange._exchange_address}'")
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
base_token_address = data_asset_info["baseTokenAddress"]
```

<br />

## 2. Approve tokens for consumer_A

In the same python console (Fixed Pricing Asset):

```python
usdc_token = ocean.get_datatoken(ocean.web3.toChecksumAddress(base_token_address))

erc20_enterprise_token = DatatokenEnterprise(ocean.web3, ocean.web3.toChecksumAddress(token_address))


consumer_private_key = os.getenv('TEST_PRIVATE_KEY2')
consumer_A_wallet = Wallet(ocean.web3, consumer_private_key, config.block_confirmations,  config.transaction_timeout)

datatoken_address = token_address
nft_factory = ocean.get_nft_factory()

exchange_addresses_and_ids = nft_factory.search_exchange_by_datatoken(ocean.fixed_rate_exchange, erc20_enterprise_token.address, exchange_owner=data_token_owner_address)
assert (
    exchange_addresses_and_ids
), f"No exchanges found. datatoken_address = {datatoken_address}, exchange_owner = {data_token_owner_address}."


exchange_address = exchange_addresses_and_ids[0][0]
exchange_id = exchange_addresses_and_ids[0][1]

fixed_price_address = ocean.fixed_rate_exchange.address

# Approve tokens for consumer_A
usdc_token.approve(erc20_enterprise_token.address, ocean.to_wei(100), consumer_A_wallet)
erc20_enterprise_token.approve(erc20_enterprise_token.address, ocean.to_wei(100), consumer_A_wallet)
```

<br />

## 3. ConsumerA buys datatoken (Fixed-rate) / request datatoken from dispenser (Free)

In the same python console (Fixed Pricing Asset):

```python
asset = ocean.assets.resolve(did)
access_service = asset.services[0]

(
    provider_fee_address,
    provider_fee_token,
    provider_fee_amount,
    v,
    r,
    s,
    valid_until,
    provider_data,
) = ocean.retrieve_provider_fees(asset=asset, access_service=access_service, publisher_wallet=consumer_A_wallet)

tx = erc20_enterprise_token.buy_from_fre_and_order(
        consumer=consumer_A_wallet.address,
        service_index=0,
        provider_fee_address=provider_fee_address,
        provider_fee_token=provider_fee_token,
        provider_fee_amount=int(provider_fee_amount),
        v=v,
        r=r,
        s=s,
        valid_until=0,
        provider_data=provider_data,
        consume_market_order_fee_address=consumer_A_wallet.address,
        consume_market_order_fee_token=erc20_enterprise_token.address,
        consume_market_order_fee_amount=0,
        exchange_contract=ocean.fixed_rate_exchange.address,

        exchange_id=exchange_id,
        max_base_token_amount=to_wei(10),
        consume_market_swap_fee_amount=to_wei("0.001"),  # 1e15 => 0.1%
        consume_market_swap_fee_address=consumer_A_wallet.address,
        from_wallet=consumer_A_wallet,
    )
```

<br />

### If the Asset is Free Price

In the same python console (Free Pricing Asset):

```python
asset = ocean.assets.resolve(did)
access_service = asset.services[0]


(
    provider_fee_address,
    provider_fee_token,
    provider_fee_amount,
    v,
    r,
    s,
    valid_until,
    provider_data,
) = ocean.retrieve_provider_fees(asset=asset, access_service=access_service, publisher_wallet=consumer_A_wallet)

tx = erc20_enterprise_token.buy_from_dispenser_and_order(
    consumer=consumer_A_wallet.address,
    service_index=0,
    provider_fee_address=provider_fee_address,
    provider_fee_token=provider_fee_token,
    provider_fee_amount=int(provider_fee_amount),
    v=v,
    r=r,
    s=s,
    valid_until=valid_until,
    provider_data=provider_data,
    consume_market_order_fee_address=consumer_A_wallet.address,
    consume_market_order_fee_token=erc20_enterprise_token.address,
    consume_market_order_fee_amount=0,
    dispenser_address=ocean.dispenser.address,
    from_wallet=consumer_A_wallet,
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
    asset=asset,
    service=access_service,
    consumer_wallet=consumer_A_wallet,
    destination='./',
    order_tx_id=tx
    )
print(file_path)
```
