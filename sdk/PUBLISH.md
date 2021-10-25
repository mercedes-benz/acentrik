
# Quickstart: Publish Flow (Fixed Rate Exchange)

This quickstart describes publishing flow.

It focuses on Alice's experience as a publisher

Here are the steps:

1.  Setup
2.  Alice generate & publish a datatoken
3.  Alice specify metadata and service attributes
4.  Alice publish metadata and service attributes on-chain
5.  Alice mints & approve data tokens
6.  Alice create pricing

Let's go through each step.
### Disclaimer!!!
Steps 6 (Alice create pricing) are still under maintainence. Currently still didn't support other baseToken other than OCEAN.

## 1. Setup
### Prerequisites
- Alice's Wallets have Publisher Roles

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

import os
from datetime import datetime
import random
import string
 
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.web3_internal.currency import to_wei
 
usdc_address = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b" # rinkeby usdc address
#usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" # polygon usdc address
 
#Token Id random generator
def id_generator(size=5, chars=string.ascii_uppercase):
  return ''.join(random.choice(chars) for _ in range(size))
```



## 2. Alice generate & publish a datatoken
In the same python console:
```python
#Check Alice have enough ETH
alice_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY1'), config.block_confirmations, config.transaction_timeout)
 
from ocean_lib.models.btoken import BToken #BToken is ERC20
USDC_token = BToken(ocean.web3, usdc_address)
 
#Verify that Alice has ETH
assert ocean.web3.eth.get_balance(alice_wallet.address) > 0, "need ETH"

#Generate & publish a datatoken
token_id = id_generator() + "001"
data_token = ocean.create_data_token(token_id+"Token", token_id , alice_wallet, blob=ocean.config.metadata_cache_uri)
token_address = data_token.address
 
print(f"token_id = '{token_id}'")
print(f"token_address = '{token_address}'")
```


## 3.  Alice specify metadata and service attributes
In the same python console:
```python
date_created = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
metadata = {
  "main": {
    "type": "dataset",
    "name": "Alice SDK Test " + token_id,
    "author": "Alice",
    "license": "CC0: Public Domain",
    "dateCreated": date_created,
    "files": [
      {
        "index": 0,
        "contentType": "text/plain",
        "url": "https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv",
        "contentLength": "113593"
      }
    ]
  },
  "additionalInformation": {
    "description": "Test Alice SDK " + token_id,
    "tags": [],
    "links": [],
    "termsAndConditions": True,
    "source": "ddm",
    "isExperimental": False,
    "categories": [
      "Insurance"
    ],
    "shortDescription": "Test Alice SDK",
    "input": {
      "size": 0,
      "sizeType": "",
      "fileType": "",
      "screenshot": ""
    },
    "output": {
      "size": 0,
      "sizeType": "",
      "fileType": "",
      "screenshot": ""
    },
    "remark": ""
  }
}

service_attributes = {
        "main": {
            "name": "dataAssetAccessServiceAgreement",
            "creator": alice_wallet.address,
            "timeout": 3600 * 24,
            "datePublished": date_created,
            "cost": 1.0, # <don't change, this is obsolete>
        }
}

```

## 4. Alice publish metadata and service attributes on-chain.
In the same python console:
```python
# The service urls will be encrypted before going on-chain.
# They're only decrypted for datatoken owners upon consume.
 
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.common.agreements.service_types import ServiceTypes
from ocean_lib.common.ddo.service import Service
 
service_endpoint = DataServiceProvider.get_url(ocean.config)
 
download_service = Service(
    service_endpoint=service_endpoint,
    service_type=ServiceTypes.ASSET_ACCESS,
    attributes=service_attributes,
)
 
assert alice_wallet.web3.eth.get_balance(alice_wallet.address) > 0, "need ETH"
asset = ocean.assets.create(
  metadata,
  alice_wallet,
  services=[download_service],
  data_token_address=token_address,
  encrypt=True
  )
assert token_address == asset.data_token_address
 
did = asset.did  # did contains the datatoken address
print(f"did = '{did}'")
```

## 5. Alice mints & approve data tokens
In the same python console:
```python
data_token.mint(alice_wallet.address, to_wei(100), alice_wallet)
data_token.approve(ocean.exchange._exchange_address, to_wei(100), alice_wallet)
```



## 6. Alice create pricing
```python
from ocean_lib.models.btoken import BToken #BToken is ERC20
USDC_token = BToken(ocean.web3, usdc_address)
assert USDC_token.balanceOf(alice_wallet.address) > 0, "need USDC"

exchange_id = ocean.exchange.create(token_address, to_wei("1"), alice_wallet)
print(f"exchange_id = '{exchange_id}'")
```