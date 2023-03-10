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
- pip install wheel
- pip install --pre ocean-lib

- Ocean.py

  - Either install using (pip install 'ocean-lib>=v2.1.0')
  - or pull latest ocean.py code (https://github.com/oceanprotocol/ocean.py) & build it (pip install ./ocean.py/ )
  - ⚠️ Mac users: the ocean.py installation are not compatible with Apple M1 Processor[[Details](https://github.com/oceanprotocol/ocean.py/issues/486).]

<br />

- Configure Brownie networks

  Brownie's network configuration file is in your home folder, at `~/.brownie/network-config.yaml` on Linux/MacOS systems. For Windows users, that means `C:\Users\<user_name>\.brownie\network-config.yaml`. If you have no prior brownie installation on your computer, in order to create this file, you need to call any brownie function from a python console, beforehand (e.g., run `from ocean_lib.example_config import get_config_dict`).

  The network configuration file has settings for each network, e.g. development (ganache), Ethereum mainnet, Polygon, and Mumbai.

  Each network gets specifications for:

  - `host` - the RPC URL, i.e. what URL do we pass through to talk to the chain
  - `required_confs` - the number of confirmations before a tx is done
  - `id` - e.g. `polygon-main` (Polygon), `polygon-test` (Mumbai)

  [Here's](https://github.com/eth-brownie/brownie/blob/master/brownie/data/network-config.yaml) the `network-config.yaml` from Brownie's GitHub repository. It can serve as a comparison to your local copy.

  For Windows OS deployments, it is possible that the network-config.yaml does not include all the network entries. In this case, you can replace the content of the network-config.yaml file on your computer with the content from this [link](https://github.com/eth-brownie/brownie/blob/master/brownie/data/network-config.yaml).

  `development` chains run locally; `live` chains run remotely.

  Ocean.py follows the exact `id` name for the network's name from the default Brownie configuration file. Therefore, you need to ensure that your target network name matches the corresponding Brownie `id`.

  <br />

  The config file's default RPCs point to Infura, which require you to have an Infura account with corresponding token `WEB3_INFURA_PROJECT_ID`.

  #### If you do have an Infura account

  - Linux & MacOS users: in console: `export WEB3_INFURA_PROJECT_ID=<your infura ID>`
  - Windows: in console: `set WEB3_INFURA_PROJECT_ID=<your infura ID>`

<br />

- Set Env variable in your work console

```
#set private keys (PublisherA & ConsumerA)
export TEST_PRIVATE_KEY1=0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fecXXXXXX
export TEST_PRIVATE_KEY2=0x804365e293b9fab9bd11bddd39082396d56d30779efbb3ffb0a6089027XXXXXX
```

## Relevant Docs (Ocean Protocol)

- https://github.com/oceanprotocol/ocean.py/tree/v2.1.0/READMEs
