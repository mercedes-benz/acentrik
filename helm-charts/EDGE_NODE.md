# Edge Node Guidelines and Setup Instructions

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Tools](#tools)
- [Installation](#installation)
  - [Container Registry](#container-registry)
  - [Customize Provider Deployment](#customize-your-provider-deployment)
- [Best Practice](#best-practice)

---

## Overview

An edge node contains only one components: Provider

---

## Prerequisites

Setting up a Edge Node stack requires expertise on **Kubernetes**, **Helm** and **Cloud Services** such as AWS/Azure (Depending on which Cloud you will be running the Edge Node On)

First, the following resources are required for a proper runtime environment setup:

1. An EVM-based wallet (MetaMask) account for the Provider (You can read more about setting up a Metamask Wallet [here](https://support.acentrik.io/help/en-us/8-starter-kit/914-wallet-set-up-metamask-reference))
2. An EVM RPC service provider subscription (can be free or lowest tier subscription) which supported Polygon network (such as Infura, Chainstack, Alchemy, ...)
3. Own-managed Kubernetes environment (Eg: EKS for AWS, AKS for Azure, GKE for GCP)
4. Redis for stateless provider setup to support High Availability (Optional)
5. **Outbound network** required on the kubernetes setup, this is because provider are required to request endpoint from Acentrik services, such as Aquarius & RBAC
   - Refer to config such as `config.aquariusUrl` & `config.rbacUrl` on the values file
6. **Inbound network** required for provider, In order for Acentrik Marketplace to connect to the Edge Node, Provider need to be internet-facing and **publically accessible** from Acentrik Marketplace
   - Preferably a SSL Certificated public facing endpoint
   - Please make sure that the endpoint is accessible over the internet and is not protected by a firewall or by credentials.
7. To confidently validate above prerequisite, a **Hello world API** could be deploy on your infrastucture setup and cover at least point 3, 6. If **Hellow world API** works as expected, the kubernetes object can be replace with Edge Node component.

---

## Tools

1. Helm 3 CLI - [install](https://helm.sh/docs/intro/install/)
   - Helm CLI are for helm chart installation, Edge Node will be deploying with Helm Chart
2. Kubectl CLI - [install](https://kubernetes.io/docs/tasks/tools/#kubectl)
   - Kubectl CLI are use to run commands against Kubernetes cluster

---

## Installation

Deploy the following helm chart with appropriate customized values. The download links for each helm charts will be provided.

|     | Helm Chart             | Recommended Namespace          | Description                                                                         |
| :-- | :--------------------- | :----------------------------- | ----------------------------------------------------------------------------------- |
| 1   | [provider](./provider) | network specific, e.g. polygon | An Ethereum network-specific deployment object to serve an interface to Marketplace |

Note: Modify the helm charts according on your own Kubernetes cluster setup when necessary. Alternatively you can deploy the standard Kubernetes objects by creating your own deployment yaml files.

<br />

### Container registry

By default, all helm charts are predefined with public docker images available in Acentrik's Amazon Elastic Container Registry (Amazon ECR), as following public registry

```
public.ecr.aws/acentrik
```

Optionally you can pull and mirror all the required images to your own private registry if necessary.

<br />

### [Customize your Provider deployment](./provider)

| Variable                          | Description                                                                                                                                                     |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| secret.infuraProjectId            | Ethereum RPC Project ID                                                                                                                                         |
| secret.providerPrivateKey\*       | Private key of your provider wallet account, which used to encrypt the data asset endpoint                                                                      |
| secret.networkUrl                 | Network name: polygon                                                                                                                                           |
| secret.redisConnection\*\*        | Connection URL to Redis. Defaults to None (no Redis connection, SQLite database embedded with provider is used instead)                                         |
| config.ipfsGateway                | Your IPFS Gateway if any                                                                                                                                        |
| config.operatorServiceUrl         | Your custom operator service endpoint URL (Leave the value empty if no need to run compute job)                                                                 |
| config.aquariusUrl\*\*\*          | Predefined Aquarius URL of multi-chain network. Defaults to Acentrik Aquarius URL                                                                               |
| config.authorizedDecrypters\*\*\* | List of authorized addresses that are allowed to decrypt chain data. Use it to restrict access only to certain callers (e.g. Acentrik Aquarius wallet address). |
| config.rbacUrl\*\*\*              | URL to the RBAC permissions server. Defaults to Acentrik RBAC Server                                                                                            |
| config.log.level                  | Logging level                                                                                                                                                   |
| config.allowNonPublicIp           | Allow Non Public IP to access from Provider                                                                                                                     |
| config.providerFeeToken\*\*\*     | the address of ERC20 token used to get fees, or string containing a dict of chain_id to token address pairs                                                     |

\*Provider Private Key

- The secret hash of your Ether wallet account
- A string of 64 hexadecimal characters
- Private key is unique to each wallet account
- Example: afdfd9c3d2095ef696594f6cedcae59e72dcd697e2a7521b1578140422a4f890
- As standard, the key will be stored as Kubernetes Secret. However, it is possible to integrate with an external secret provider depends on your distributed architecture infrastructure setup

\*\* Redis acting as a shared cache storage is highly recommended to support multi-replicas setup of provider service which ensure high availability. Without Redis, only 1 replica is supported.

\*\*\* For config value such as `aquariusUrl` , `authorizedDecrypters` , `rbacUrl` & `providerFeeToken`. Please request from the Acentrik team, the values will likely be dependent on which network the Edge node will be running in and which Acentrik enviroment the Edge Node will be connecting to.

For example, it'll be running Polygon Network & connecting to Acentrik Production Enviroment.

#### Steps

Copy and modify the default helm values file as a new custom-values.yaml

There's a helm values file for each network (Eg: values-polygon.yaml)

```
helm upgrade provider ./provider \
    --install \
    --namespace polygon \
    -f ./provider/custom-values.yaml \
    --debug \
    --render-subchart-notes
```

---

## Post-installation

### Verify if provider are working as expected

Check if provider are running as expected, expected to see the pod are running with status 1/1

```
kubectl get pods -n polygon
```

Run a curl command to verify if Provider REST API are working

This API will Retrieves Content-Type and Content-Length from the given asset URL and make sure if its valid

```
curl --location --request POST 'https://{{provider-url}}/api/services/fileinfo' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "url",
    "url": "https://{{sample-asset-url}}/.csv",
    "checksum": false
}'
```

<br />

---

<br />

## Best Practice

For more information, refer to: https://support.acentrik.io/help/en-us/10/10
