# SDK (Ocean.py)
Python library to privately & securely publish and consume data on Acentrik


With ocean.py, you can:
- **Publish** data services: downloadable files or compute-to-data, datatoken for each dataset / data service.
- **Mint** datatokens for the service
- **Sell** datatokens for a fixed price
- **Consume** datatokens, to access the service

## Setup
### Prerequisites
- Python 3.8.5+
- Aquarius URL v3.1.1+
- Provider URL v0.4.16+
- Ocean.py  
    - Either install using (pip install 'ocean-lib>= 0.8.5')
    - or pull latest ocean.py code (https://github.com/oceanprotocol/ocean.py) & build it (pip install  ./ocean.py/ ) 


- Create a config.ini and fill in as below (Example are with Rinkeby network)
```
[eth-network]
network = https://rinkeby.infura.io/v3/d64c34d769c64cbd80c39d3f25XXXXXX # RPC URL
address.file =  /home/ubuntu/contracts-artifacts/address.json
 
; If polygon network
; chain_id = 137
; network_name = polygon
; network = https://matic-mainnet.chainstacklabs.com/ # RPC URL
; block_confirmations = 15
; transaction_timeout = 600
 
 [resources]
metadata_cache_uri = https://aquarius.acentrik.io
provider.url = https://provider.rinkeby.acentrik.io
provider.address = https://provider.rinkeby.acentrik.io
 
downloads.path = /home/ubuntu/download-path/
```

- Clone address file from [ocean contract repo](https://github.com/oceanprotocol/contracts/blob/main/artifacts/address.json), then edit it's FixedRateExchange values (For Rinkeby & Polygon) 

```
"rinkeby": {
    "DTFactory": "0x3fd7A00106038Fb5c802c6d63fa7147Fe429E83a",
    "BFactory": "0x53eDF9289B0898e1652Ce009AACf8D25fA9A42F8",
    "FixedRateExchange": "0x1Ca58726115923C94B63cb43A8774D9589e7Cce4",
    "Metadata": "0xFD8a7b6297153397B7eb4356C47dbd381d58bFF4",
    "Ocean": "0x8967BCF84170c91B0d24D4302C2376283b0B3a07",
    "Dispenser": "0x623744Cd25Ed553d3b4722667697F926cf99658B",
    "chainId": 4,
    "startBlock": 9043179
   },
"polygon": {
    "DTFactory": "0xF6410bf5d773C7a41ebFf972f38e7463FA242477",
    "BFactory": "0x69B6E54Ad2b3c2801d11d8Ad56ea1d892555b776",
    "FixedRateExchange": "0x2720d405ef7cDC8a2E2e5AeBC8883C99611d893C",
    "Metadata": "0x80E63f73cAc60c1662f27D2DFd2EA834acddBaa8",
    "Ocean": "0x282d8efCe846A88B159800bd4130ad77443Fa1A1",
    "Dispenser": "0x30E4CC2C7A9c6aA2b2Ce93586E3Df24a3A00bcDD",
    "chainId": 137,
    "startBlock": 17638255
   },
```

- Set Env variable in your work console
```
#set private keys of two accounts (Alice & Bob)
export TEST_PRIVATE_KEY1=0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fecXXXXXX
export TEST_PRIVATE_KEY2=0x804365e293b9fab9bd11bddd39082396d56d30779efbb3ffb0a6089027XXXXXX
 
export OCEAN_NETWORK_URL=https://rinkeby.infura.io/v3/d64c34d769c64cbd80c39d3f25XXXXXX
export ADDRESS_FILE=/home/ubuntu/contracts-artifacts/address.json
```


## Relevant Docs (Ocean)
- Fixed Rate Exchange Flow : https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/fixed-rate-exchange-flow.md
- Compute-to-Data (C2D) Flow: https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/c2d-flow.md