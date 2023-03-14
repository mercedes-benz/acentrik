# Quickstart: Publish Flow

This describes the flow when publishing a Data Asset, focusing on ProviderrA's experience as a Data Provider on Acentrik Data Marketplace

Here are the steps:

1.  Setup
2.  Generate & publish a datatoken (Fixed / Free Pricing)
3.  Specify metadata and service attributes (Compute / Download)
4.  Publish metadata and service attributes on-chain

<br />

Let's go through each step. <b> There's two possible scenario (Compute / Download), And for each scenario, user can decided pricing of the asset (Fixed Rate / Free). </b>

<br />

## 1. Setup

### Prerequisites

- PublisherA's Wallets have Publisher Roles
- Base Token address (Eg: USDC on goerli network are "0x07865c6E87B9F70255377e024ace6630C1Eaa37F")
- Clone words.json file from [OceanJs Repository](https://raw.githubusercontent.com/oceanprotocol/ocean.js/v2.7.0-next.2/src/utils/data/words.json)
- Aquarius and Provider Uri
- Set config parameter

<br />

### Set config parameter

An Ocean instance will hold a config_dict that holds various config parameters. These parameters need to get set. This is set based on what's input to Ocean constructor:

1.  dict input: `Ocean({'METADATA_CACHE_URI':..})`
2.  use boilerplate from example config

#### Example

Here is an example for (1): dict input, filled from envvars

```python
from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean
config = get_config_dict("goerli")

config['METADATA_CACHE_URI'] = aquarius_uri
config['PROVIDER_URL'] = asset_provider_uri

ocean = Ocean(config)
```

<br />

In the Python console:

```python
import json
from ocean_lib.ocean.util import to_wei
import os
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
  return "ATT-TEST-" + ''.join(random.choice(string.ascii_uppercase + string.digits ) for _ in range(size))
def dt_generator(size=8):
    adjective = random.choice(list["adjectives"])
    noun = random.choice(list["nouns"])
    random_number = "{:02d}".format(random.randint(1, 99))
    name = adjective.title() + " " + noun.title() + " Token"
    symbol = adjective[0:3].upper() + noun[0:3].upper() + random_number
    return name, symbol

#create ocean instance
from ocean_lib.web3_internal.utils import connect_to_network
connect_to_network("goerli")
import os
from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean
config = get_config_dict("goerli")

# Set config parameter
config['METADATA_CACHE_URI'] = "https://v1.aquarius.dev.acentrik.io"  # Aquarius URI
config['PROVIDER_URL'] = "https://v1.provider.goerli.dev.acentrik.io"  # Provider URI

ocean = Ocean(config)

print(f"config.metadata_cache_uri = {config['METADATA_CACHE_URI']}")
print(f"config.provider_url = {config['PROVIDER_URL']}")
from brownie.network.gas.strategies import GasNowStrategy
from brownie import network
gas_strategy = GasNowStrategy("fast")
network.priority_fee("75 gwei")
network.gas_limit("auto")
network.gas_price("auto")
```

<br />

## 2. Generate & publish a datatoken (Fixed / Free Pricing)

### Scenario A - Fixed-rate aka Premium

In the same python console:

```python
# get asset token/ mint
usdc_token = ocean.get_datatoken("0x07865c6E87B9F70255377e024ace6630C1Eaa37F")
from brownie.network import accounts
accounts.clear()
consumer_private_key = os.getenv('TEST_PRIVATE_KEY1')
publisher_A_wallet = accounts.add(consumer_private_key)
print(f"publisher_A_wallet.address = '{publisher_A_wallet.address}'")

# create_nft_erc20_with_fixed_rate ================================
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
fixed_rate_exchange = ocean.fixed_rate_exchange
from ocean_lib.models.data_nft import DataNFT, DataNFTArguments
nft_name = 'Acentrik Asset Management'
data_nft_arguments = DataNFTArguments(
  name=nft_name,
  symbol=nft_symbol,
  template_index=1,
  uri=nft_token_uri,
  transferable=True,
  owner=publisher_A_wallet.address
  )
from ocean_lib.models.datatoken_base import DatatokenArguments
dt_arguments = DatatokenArguments(
  name=data_token_name,
  symbol=data_token_symbol,
  template_index=2,
  minter=publisher_A_wallet.address,
  fee_manager=publisher_A_wallet.address,
  publish_market_order_fees=0,
  bytess=[b""],
  cap=to_wei(100)
  )
from ocean_lib.models.fixed_rate_exchange import ExchangeArguments
fixed_price_arguments = ExchangeArguments(
  rate=to_wei(1), # Data Asset Price
  base_token_addr=usdc_token.address,
  owner_addr=publisher_A_wallet.address,
  publish_market_fee_collector=publisher_A_wallet.address,
  publish_market_fee=0,
  with_mint=True,
  allowed_swapper=ZERO_ADDRESS,
  dt_decimals=18
)
tx = ocean.data_nft_factory.create_with_erc20_and_fixed_rate(
  data_nft_args=data_nft_arguments,
  datatoken_args=dt_arguments,
  fixed_price_args=fixed_price_arguments,
  tx_dict={"from": publisher_A_wallet}
)
data_nft: DataNFT = tx[0]
from ocean_lib.models.datatoken2 import Datatoken2
datatoken: Datatoken2 = tx[1]
```

### Scenario B - Free

```python
# Free rate
data_nft_arguments = DataNFTArguments(
  name=nft_name,
  symbol=nft_symbol,
  template_index=1,
  uri=nft_token_uri,
  transferable=True,
  owner=publisher_A_wallet.address
  )

from ocean_lib.models.datatoken_base import DatatokenArguments
dt_arguments = DatatokenArguments(
  name=data_token_name,
  symbol=data_token_symbol,
  template_index=2,
  minter=publisher_A_wallet.address,
  fee_manager=publisher_A_wallet.address,
  publish_market_order_fees=0,
  bytess=[b""],
  cap=to_wei(100)
  )

from ocean_lib.models.dispenser import DispenserArguments
dispenser_arguments = DispenserArguments(
  max_tokens=to_wei(1),
  max_balance=to_wei(1),
  with_mint=True,
  allowed_swapper=ZERO_ADDRESS,
)

tx = ocean.data_nft_factory.create_with_erc20_and_dispenser(
  data_nft_args=data_nft_arguments,
  datatoken_args=dt_arguments,
  dispenser_args=dispenser_arguments,
  tx_dict={"from": publisher_A_wallet}
)
```

<br />

## 3. Specify metadata and service attributes (Compute / Download)

### If the Asset is Dataset (Download) Type

In the same python console:

```python
# specify metadata and service attributes
date_created = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "dataset",
    "license": "https://market.oceanprotocol.com/terms",
    "name": "heart py download from SDK",
    "description": "",
    "additionalInformation": {
      "source": "ddmdev",
      "accessPermission": "allow"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [],
}
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service
from ocean_lib.agreements.service_types import ServiceTypes

url_file = UrlFile(
    url="https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py"
)

service_id = hashlib.sha256((datatoken.address).encode()).hexdigest()

service = Service(
    service_id=service_id,
    service_type=ServiceTypes.ASSET_ACCESS,
    service_endpoint=config['PROVIDER_URL'],
    datatoken=datatoken.address,
    files=[url_file],
    timeout=3600,
    compute_values=None,
    description="",
    additional_information={
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
        "links": [],
      }
)
```

### If the Asset is Algorithm (Download) Type

Metadata & Service attributes if the asset are Algorithm

```python
date_created = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "algorithm",
    "algorithm": {
      "container": {
        "checksum": "sha256:c3961075147711755b24d91213daaece5ea74fdb8f746b79b912926d7c9a1981",
        "entrypoint": "python $ALGO",
        "image": "public.ecr.aws/acentrik/oceanprotocol/algo_dockers",
        "tag": "python-panda"
      },
      "language": "python3.7",
      "version": "0.1"
    },
    "license": "https://market.oceanprotocol.com/terms",
    "name": "heart py algo from SDK - Algo ",
    "description": "",
    "additionalInformation": {
      "eulaType": "URL",
      "source": "ddmdev"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [],
}

# ocean.py offers multiple file types, but a simple url file should be enough for this example
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service
from ocean_lib.agreements.service_types import ServiceTypes

url_file = UrlFile(
    url="https://project-sgx-datasets.s3.ap-southeast-1.amazonaws.com/Others/Heart.py"
)

service_id = hashlib.sha256((datatoken.address).encode()).hexdigest()

service = Service(
    service_id=service_id,
    service_type=ServiceTypes.ASSET_ACCESS,
    service_endpoint=config['PROVIDER_URL'],
    datatoken=datatoken.address,
    files=[url_file],
    timeout=3600,
    compute_values=None,
    description="",
    additional_information={
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
        "links": [],
      }
)

```

### If the Asset is Compute Type

Metadata & Service attributes if the asset are Compute

```python
date_created = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
metadata = {
    "created": date_created,
    "updated": date_created,
    "author": "",
    "type": "dataset",
    "license": "https://market.oceanprotocol.com/terms",
    "name": "heart csv from SDK - Compute",
    "description": "",
    "additionalInformation": {
      "eulaType": "URL",
      "source": "ddmdev"
    },
    "categories": [
      "Aerospace"
    ],
    "tags": [],
}

# ocean.py offers multiple file types, but a simple url file should be enough for this example
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service
from ocean_lib.agreements.service_types import ServiceTypes

url_file = UrlFile(
    url="https://raw.githubusercontent.com/ngboonpin/GettingAndCleaningData/master/heart.csv"
)

# Specify which algo asset are compatible with you asset
algo_asset = ocean.assets.resolve("did:op:91e47e398b12929f57753f32216a1e63c731058a111555e2017cc03ef2bfc13d")
compute_value =  {
        "allowNetworkAccess": True,
        "allowRawAlgorithm": False,
        "publisherTrustedAlgorithmPublishers": None,
        "publisherTrustedAlgorithms": [ algo_asset.generate_trusted_algorithms()]
      }

service_id = hashlib.sha256((datatoken.address).encode()).hexdigest()

service = Service(
    service_id=service_id,
    service_type=ServiceTypes.CLOUD_COMPUTE,
    service_endpoint=config['PROVIDER_URL'],
    datatoken=datatoken.address,
    files=[url_file],
    timeout=3600,
    name="Service for SDK",
    compute_values=compute_value,
    description="",
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
)
```

<br />

## 4. Publish metadata and service attributes on-chain

In the same python console:

```python
# The service urls will be encrypted before going on-chain.
# They're only decrypted for datatoken owners upon consume.

asset = ocean.assets.create(
    metadata=metadata,
    tx_dict={"from": publisher_A_wallet.address},
    data_nft_address=data_nft.address,
    data_nft_args=data_nft_arguments,
    deployed_datatokens=[datatoken],
    services=[service],
    datatoken_args=dt_arguments,
    encrypt_flag=True,
    compress_flag=True
)
print("ddo")
did = asset[2].did # did contains the datatoken address
```
