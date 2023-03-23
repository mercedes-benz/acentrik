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

First, the following resources are required for a proper runtime environment setup:

1. An Ether wallet (MetaMask) account for the Provider (You can read more about setting up a Metamask Wallet [here](https://support.acentrik.io/help/en-us/8-starter-kit/914-wallet-set-up-metamask-reference))
2. An Ethereum RPC service provider account which supported Polygon network (such as Infura, Chainstack, Alchemy)
3. Own-managed Kubernetes environment (Eg: EKS for AWS, AKS for Azure, GKE for GCP)
4. Redis for stateless provider setup to support High Availability (Optional)

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

| Variable                    | Description                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| secret.infuraProjectId      | Ethereum RPC Project ID                                                                                                 |
| secret.providerPrivateKey\* | Private key of your provider wallet account, which used to encrypt the data asset endpoint                              |
| config.networkUrl           | Network name: polygon                                                                                                   |
| config.redisConnection\*\*  | Connection URL to Redis. Defaults to None (no Redis connection, SQLite database embedded with provider is used instead) |
| config.ipfsGateway          | Your IPFS Gateway if any                                                                                                |
| config.operatorServiceUrl   | Your custom operator service endpoint URL (Leave the value empty if no need to run compute job)                         |
| config.aquariusUrl\*\*\*    | Predefined Aquarius URL of multi-chain network                                                                          |
| config.rbacUrl\*\*\*\*      | URL to the RBAC permissions server. Defaults to Acentrik RBAC Server                                                    |
| config.log.level            | Logging level                                                                                                           |
| config.allowNonPublicIp     | Allow Non Public IP to access from Provider                                                                             |

\*Provider Private Key

- The secret hash of your Ether wallet account
- A string of 64 hexadecimal characters
- Private key is unique to each wallet account
- Example: afdfd9c3d2095ef696594f6cedcae59e72dcd697e2a7521b1578140422a4f890
- As standard, the key will be stored as Kubernetes Secret. However, it is possible to integrate with an external secret provider depends on your distributed architecture infrastructure setup

\*\* Redis acting as a shared cache storage is highly recommended to support multi-replicas setup of provider service which ensure high availability. Without Redis, only 1 replica is supported.

\*\*\* Aquarius URL refer to https://v1.aquarius.acentrik.io (DO NOT change)

\*\*\*\* RBAC URL refer to https://v1.rbac.acentrik.io (DO NOT change)

#### Steps

Copy and modify the default helm values file as a new custom-values.yaml

```
helm upgrade provider ./provider \
    --install \
    --namespace polygon \
    -f ./provider/custom-values.yaml \
    --debug \
    --render-subchart-notes
```

---

<br />

## Best Practice

For more information, refer to: https://support.acentrik.io/help/en-us/10/10
