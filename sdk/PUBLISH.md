# Quickstart: Publish Flow

This describes the flow when publishing a Data Asset, focusing on ProviderrA's experience as a Data Provider on Acentrik Data Marketplace

Here are the steps:

1.  Setup
2.  PublisherA generate & publish a datatoken (Fixed / Free Pricing)
3.  PublisherA specify metadata and service attributes (Compute / Download)
4.  PublisherA publish metadata and service attributes on-chain

Let's go through each step.

<br />

## 1. Setup

### Prerequisites

- PublisherA's Wallets have Publisher Roles
- Base Token address (Eg: USDC on rinkeby network are "0x4dbcdf9b62e891a7cec5a2568c3f4faf9e8abe2b")
- Clone words.json file from [OceanJs Repository](https://github.com/oceanprotocol/ocean.js/blob/v4main/src/data/words.json)

In the Python console:

```python
#create ocean instance
from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean
config = Config('config.ini')
ocean = Ocean(config)
import json
print(f"config.network_url = '{config.network_url}'")
print(f"config.block_confirmations = {config.block_confirmations.value}")
print(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
print(f"config.provider_url = '{config.provider_url}'")

from ocean_lib.web3_internal.currency import from_wei, to_wei
import os
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from datetime import datetime
import string
import random
import base64
import hashlib

words = open('words.json')
list = json.load(words)
words.close()

def nft_symbol_generator(size=8):
  return "AAMT-" + ''.join(random.choice(string.ascii_uppercase + string.digits ) for _ in range(size))

def dt_generator(size=8):
    adjective = random.choice(list["adjectives"])
    noun = random.choice(list["nouns"])
    random_number = "{:02d}".format(random.randint(1, 99))

    name = adjective.title() + " " + noun.title() + " Token"
    symbol = adjective[0:3].upper() + noun[0:3].upper() + random_number
    return name, symbol
```

<br />

## 2. PublisherA generate & publish a datatoken (Fixed / Free Pricing)

### If the Asset is Fixed Price

In the same python console:

```python
usdc_token = ocean.get_datatoken(ocean.web3.toChecksumAddress("0x4dbcdf9b62e891a7cec5a2568c3f4faf9e8abe2b"))

publisher_A_wallet = Wallet(ocean.web3, os.getenv('TEST_PRIVATE_KEY1'), config.block_confirmations, config.transaction_timeout)

#Generate & publish a datatoken
nft_symbol = nft_symbol_generator()
nft_metadata = {
  "name": "Acentrik Asset Management",
  "symbol": nft_symbol,
  "description": "This token represents the holder’s ability to manage the corresponding Data Asset on Acentrik Data Marketplace.",
  "external_url": "https://market.oceanprotocol.com",
  "background_color": "141414",
  "image_data": "https://acentrik-assets.s3.ap-southeast-1.amazonaws.com/static/acentrik_logo_short.svg"
}
str_nft_metadata = json.dumps(nft_metadata)
base64_nft_metadata = base64.b64encode(str_nft_metadata.encode('utf-8'))
nft_token_uri = "data:application/json;base64," + base64_nft_metadata.decode('ascii')

data_token_name, data_token_symbol = dt_generator()

fixed_rate_exchange = ocean.fixed_rate_exchange.address

# fixed rate
tx = ocean.get_nft_factory().create_nft_erc20_with_fixed_rate(
        nft_name='Acentrik Asset Management',
        nft_symbol=nft_symbol,
        nft_template=1,
        nft_token_uri=nft_token_uri,
        nft_transferable=True,
        nft_owner=publisher_A_wallet.address,
        datatoken_template=2,
        datatoken_name=data_token_name,
        datatoken_symbol=data_token_symbol,
        datatoken_minter=publisher_A_wallet.address,
        datatoken_fee_manager=publisher_A_wallet.address,
        datatoken_publish_market_order_fee_address=usdc_token.address,
        datatoken_publish_market_order_fee_token=usdc_token.address,
        datatoken_cap=to_wei(100),
        datatoken_publish_market_order_fee_amount=0,
        datatoken_bytess=[b""],
        fixed_price_address=ocean.fixed_rate_exchange.address,
        fixed_price_base_token=usdc_token.address,
        fixed_price_owner=publisher_A_wallet.address,
        fixed_price_publish_market_swap_fee_collector=publisher_A_wallet.address,
        fixed_price_allowed_swapper=ZERO_ADDRESS,
        fixed_price_base_token_decimals=6,
        fixed_price_datatoken_decimals=18,
        fixed_price_rate=to_wei("1"), # fixed rate price
        fixed_price_publish_market_swap_fee_amount=0,
        fixed_price_with_mint=1,
        from_wallet=publisher_A_wallet,
    )

nft_address = ocean.get_nft_factory().get_token_address(tx)
erc721_nft = ocean.get_nft_token(nft_address)
data_token_address = erc721_nft.get_tokens_list()[0]
data_token = ocean.get_datatoken(data_token_address)

```

### If the Asset is Free Price

```python
# Free rate
tx = ocean.get_nft_factory().create_nft_erc20_with_dispenser(
        nft_name='Acentrik Asset Management',
        nft_symbol=nft_symbol,
        nft_template=1,
        nft_token_uri=nft_token_uri,
        nft_transferable=True,
        nft_owner=publisher_A_wallet.address,
        datatoken_template=2,
        datatoken_name=data_token_name,
        datatoken_symbol=data_token_symbol,
        datatoken_minter=publisher_A_wallet.address,
        datatoken_fee_manager=publisher_A_wallet.address,
        datatoken_publish_market_order_fee_address=usdc_token.address,
        datatoken_publish_market_order_fee_token=usdc_token.address,
        datatoken_cap=to_wei(100),
        datatoken_publish_market_order_fee_amount=0,
        datatoken_bytess=[b""],
        dispenser_address=ocean.dispenser.address,
        dispenser_max_tokens=to_wei(1),
        dispenser_max_balance=to_wei(1),
        dispenser_with_mint=True,
        dispenser_allowed_swapper=ZERO_ADDRESS,
        from_wallet=publisher_A_wallet,
    )
```

<br />

## 3. PublisherA specify metadata and service attributes (Compute / Download)

### If the Asset is Dataset (Download) Type

In the same python console:

```python
date_created = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "dataset",
    "license": "https://market.oceanprotocol.com/terms",
    "name": "Heart.py Asset from SDK",
    "description": "Description for SDK Asset Heart.py https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py",
    "additionalInformation": {
      "eulaType": "URL",
      "source": "ddmdev"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [
      "test"
    ],
}

from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service
from ocean_lib.agreements.service_types import ServiceTypes

url_file = UrlFile(
    url="https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py"
)

service_id = hashlib.sha256((data_token.address).encode()).hexdigest()

service = [Service(
    service_id=service_id,
    service_type=ServiceTypes.ASSET_ACCESS,
    service_endpoint=config.provider_url,
    datatoken=data_token.address,
    files=[url_file],
    timeout=3600,
    name="Download service for SDK",
    compute_values=None,
    description="Description for SDK",
    additional_information={
        "eulaType": "URL",
        "input": {
          "fileType": ""
        },
        "isExperimental": False,
        "output": {
          "fileType": "",
          "screenshot": ""
        },
        "sampleType": "URL",
        "source": "ddmdev",
        "termsAndConditions": True
      }
)]
```

### If the Asset is Algorithm (Download) Type

Metadata & Service attributes if the asset are Algorithm

```python
metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "algorithm",
    "algorithm": {
      "container": {
        "checksum": "",
        "entrypoint": "python $ALGO",
        "image": "public.ecr.aws/acentrik/oceanprotocol/algo_dockers",
        "tag": "python-panda"
      },
      "language": "python3.7",
      "version": "0.1"
    },
    "license": "https://market.oceanprotocol.com/terms",
    "name": "Heart.py Algorithm from SDK",
    "description": "Description for SDK Algorithm Heart.py https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py",
    "additionalInformation": {
      "eulaType": "URL",
      "source": "ddmdev"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [
      "test"
    ],
}

service = [Service(
    service_id=service_id,
    service_type=ServiceTypes.ASSET_ACCESS,
    service_endpoint=config.provider_url,
    datatoken=data_token.address,
    files=[url_file],
    timeout=3600,
    name="Service for SDK",
    compute_values=None,
    description="Description for SDK Algorithm Heart.py https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py",
    additional_information={
        "eulaType": "URL",
        "input": {
          "fileType": ""
        },
        "isExperimental": False,
        "output": {
          "fileType": "",
          "screenshot": ""
        },
        "sampleType": "URL",
        "source": "ddmdev",
        "termsAndConditions": True
      }
)]
```

### If the Asset is Compute Type

Metadata & Service attributes if the asset are Compute

```python
metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "dataset",
    "license": "https://market.oceanprotocol.com/terms",
    "name": "Heart.csv Compute from SDK",
    "description": "Description for SDK Compute Heart.csv  https://raw.githubusercontent.com/ngboonpin/GettingAndCleaningData/master/heart.csv",
    "additionalInformation": {
      "eulaType": "URL",
      "source": "ddmdev"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [
      "test"
    ],
}

service = [Service(
    service_id=service_id,
    service_type=ServiceTypes.CLOUD_COMPUTE,
    service_endpoint=config.provider_url,
    datatoken=data_token.address,
    files=[url_file],
    timeout=3600,
    name="Service for SDK",
    compute_values=compute_value,
    description="Description for SDK Compute Heart.csv  https://raw.githubusercontent.com/ngboonpin/GettingAndCleaningData/master/heart.csv",
    additional_information={
        "eulaType": "URL",
        "input": {
          "fileType": ""
        },
        "isExperimental": False,
        "output": {
          "fileType": "",
          "screenshot": ""
        },
        "sampleType": "URL",
        "source": "ddmdev",
        "termsAndConditions": True
      }
)]
```

<br />

## 4. PublisherA publish metadata and service attributes on-chain.

In the same python console:

```python
# The service urls will be encrypted before going on-chain.
# They're only decrypted for datatoken owners upon consume.

asset = ocean.assets.create(
    metadata,
    publisher_A_wallet,
    [url_file],
    services=service,
    provider_uri=config.provider_url,
    data_nft_address= nft_address,
    deployed_datatokens=[data_token],
    encrypt_flag=True
)

did = asset.did  # did contains the datatoken address
print(f"did = '{did}'")
```
