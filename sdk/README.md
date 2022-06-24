# SDK (Ocean.py)

Use of Python Library to publish/consume data on Acentrik privately and securely.

With ocean.py, you can:

- **Publish** data services: downloadable files or run compute-to-data jobs, datatoken for each dataset / data service.
- **Mint** datatokens for the service
- **Sell** datatokens for a premium price
- **Consume** datatokens, to access the service

## Setup

### Prerequisites

- Python 3.8.5+
- Ocean.py
  - Either install using (pip install 'ocean-lib>=v1.0.0')
  - or pull latest ocean.py code (https://github.com/oceanprotocol/ocean.py) & build it (pip install ./ocean.py/ )
- Create a config.ini and fill in as below (Example are with Polygon network)

  - You are able to get the required details from Acentrik Developers Details Section

    ![Copy info clipboard](./copy_info_clipboard.gif)

```
[eth-network]
network = https://matic-mainnet.chainstacklabs.com #network
network_name = polygon  #networkName
chain_id = 137  #networkID

address.file =  /home/ubuntu/contracts-artifacts/address.json

[resources]
metadata_cache_uri = https://aquarius.acentrik.io  #metadataCacheUri
provider.url = https://provider.polygon.acentrik.io  #providerUri
provider.address = https://provider.polygon.acentrik.io  #providerUri
downloads.path = /home/ubuntu/download-path/
```

- Clone address file from [ocean contract repo](https://github.com/oceanprotocol/contracts/blob/v4main/addresses/address.json)

  - This is the address.file that you filled in on config.ini

<br />

- Set Env variable in your work console

```
#set private keys (PublisherA & ConsumerA)
export TEST_PRIVATE_KEY1=0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fecXXXXXX
export TEST_PRIVATE_KEY2=0x804365e293b9fab9bd11bddd39082396d56d30779efbb3ffb0a6089027XXXXXX
```

## Relevant Docs (Ocean)

- Fixed Rate Exchange Flow : https://github.com/oceanprotocol/ocean.py/blob/v4main/READMEs/fixed-rate-exchange-flow.md
- Compute-to-Data (C2D) Flow: https://github.com/oceanprotocol/ocean.py/blob/v4main/READMEs/c2d-flow.md
- Enterprise ERC20 Flow: https://github.com/oceanprotocol/ocean.py/blob/v4main/READMEs/erc20-enterprise.md
