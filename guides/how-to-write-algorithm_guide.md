# Algorithm guide
1. [Types of algorithm](#type-of-algorithm)
    - [Basic](#basic-algorithm)
    - [Federated](#federated-algorithm)
    - [Aggregate](#aggregate-algorithm)
2. [Compute Environment](#compute-environment)
    - [Build an image](#build-an-image)
    - [About entrypoint](#about-entrypoint)
    - [Environment variables available to algorithms](#environment-variables-available-to-algorithms)
    - [Hardware environment](#hardware-environment)
3. [How to write algorithm?](#how-to-write-algorithm)
    - [Known issues and workarounds](#known-issues-and-workarounds)
4. [Publishing an algorithm using sdk](#publish-an-algorithm-using-sdk)
    - [Algorithm metadata](#algorithm-metadata)
    - [Consumer parameter](#consumer-parameters)

<hr>

# Type of algorithm

### Basic algorithm
A basic algorithm performs computations on a single dataset, known as a single compute job. Upon purchasing a compute dataset, the consumer can opt for a compatible algorithm to carry out the computation. The compute environment for the basic algorithm operates without internet access, meaning the algorithm is unable to utilize internet resources like API endpoints during computation. You have the option to enable internet access for the edge node via the edge node configuration, if required.

### Federated algorithm
Similar to the basic algorithm, the federated algorithm can conduct computations on a single dataset. The distinctive feature of a federated algorithm is its capability to perform computations on multiple datasets, referred to as multiple compute jobs. When purchasing a federated algorithm, consumers can choose multiple datasets for computation and then select an aggregate algorithm. The compute environment for the federated algorithm functions without internet access, meaning the algorithm is unable to utilize internet resources like API endpoints during computation. You have the option to enable internet access for the edge node via the edge node configuration, if required.

### Aggregate algorithm
An aggregate algorithm is designed to perform computations on an aggregate dataset and multiple C2D jobs. Following the completion of the initial stage of computation, the federated computation, consumers can proceed with the aggregation process where the output from the federated computation serves as the input for the aggregate algorithm.

\* Note: To enable the aggregate algorithm functionality, it is essential to possess **an aggregate dataset** and designate the aggregate algorithm as a trusted algorithm. The utilization of the aggregate dataset in the aggregate algorithm is optional. Moreover, the compute environment **must have internet access** to retrieve result files from the federated computation..

<hr>

<div id='3-fundamental-of-c2d'>Three fundamentals of compute-to-data (C2D)</div>

1. **Algorithm Code:** The algorithm code refers to the specific instructions and logic that define the computational steps to be executed on a dataset. It encapsulates the algorithm's functionalities, calculations, and transformations.
2. **Docker Image:** A Docker image plays a crucial role in encapsulating the algorithm code and its runtime dependencies. It consists of a base image, which provides the underlying environment for the algorithm, and a corresponding tag that identifies a specific version or variant of the image.
3. **Entrypoint:** The entrypoint serves as the starting point for the algorithm's execution within the compute environment. It defines the initial actions to be performed when the algorithm is invoked, such as loading necessary libraries, setting up configurations, or calling specific functions.

<hr>

# Compute environment
A properly configured computing environment is essential for the efficient execution of a C2D task. Creating a customized image that meets the requirements of your algorithm is vital for this purpose. This image must be available publicly via `docker pull` to enable access. Following this, your algorithm will run within the customized container you have configured.

#### Build an image
This Dockerfile example demonstrates how to create a custom image tailored to your algorithm.
```
# build from a base image or build everything from scratch
FROM python:3.8

# create directories (required)
RUN mkdir -p /data/inputs
RUN mkdir -p /data/outputs
RUN mkdir -p /data/logs

# install additional library required
RUN pip install --no-cache-dir matplotlib seaborn numpy scikit-learn 
```

Ensure the necessary directories are created in your image.
|Path|Permissions|Usage|
|----|-----------|-----|
|`/data/inputs`|read|Storage for input data sets, accessible only to the algorithm running in the pod. Contents will be the files themselves, inside indexed folders e.g. `/data/inputs/{did}/{service_id}`.|
|`/data/ddos`|read|Storage for all DDOs involved in compute job (input data set + algorithm). Contents will json files containing the DDO structure.|
|`/data/outputs`|read/write|Storage for all of the algorithm's output files. They are uploaded on some form of cloud storage, and consumer could self retrieve them via URL returned from the C2D job.|
|`/data/logs`|read/write|All algorithm output (such as print, console.log, etc.) is stored in a file located in this folder. They are stored and consumer are able to self retrieve them as well.

Please note that when using local Providers or Metatata Caches, the ddos might not be correctly transferred into c2d, but inputs are still available. If your algorithm relies on contents from the DDO json structure, make sure to use a public Provider and Metadata Cache (Aquarius instance).

<br>

After making your Docker image publicly available, please take note of the following information. This information will be required to specify your custom image when publishing an algorithm:
- Docker Registry Path: The name and image tag of your custom image.
- Image Digest: Checksum of your docker image
- Image Reference URL: For consumer to find out more about your image.

#### About entrypoint
The Docker entrypoint. `$ALGO` is a macro that gets replaced inside the compute job, depending where your algorithm code is downloaded. Define your entrypoint according to your dependencies. E.g. if you have multiple versions of Python installed, use the appropriate command `python3.6 $ALGO`. Otherwise, `python $ALGO` should serve as the entrypoint for Python algorithms.

#### Environment variables available to algorithms

For every algorithm pod, the Compute to Data environment provides the following environment variables:
|Variable|Usage|
|----|-----|
|`DIDS`|An array of DID strings containing the input datasets.|
|`TRANSFORMATION_DID`|The DID of the algorithm.|

#### Hardware environment
Ensure that the hardware specifications of the edge node are adequate for running the algorithm. Factors to consider include the number of CPU cores, RAM capacity, algorithm runtime, and the potential utilization of GPU. For instance, when training a model with TensorFlow, verify that the edge node is equipped with GPU support.

<hr>


# How to write algorithm?
You can find the complete structure of the algorithms [here](./algorithm). Note that basic algorithm and federated algorithm share the same structure, while there are some differences for aggregate algorithm.

##### Known issues and workarounds:

This section will introduce some known issues when writing algorithm and workaround methods to over it. Click the link to find more information include benefit and use case of the method, and the sample code to implement the method.

1. [Identify file uniquely](/guides/known-issue-and-workaround/identify-file-uniquely.md)
2. [Load object via URL](/guides/known-issue-and-workaround/load-object-via-URL.md)
3. [Output multiple files from federated result to aggregate algorithm](/guides/known-issue-and-workaround/output-multiple-file-to-aggAlgo.md)


# Publish an algorithm using SDK

### Algorithm metadata
When publishing the algorithm using the SDK tool, it is important to pay attention to the algorithm metadata. An asset of type `algorithm` has additional attributes under `metadata.algorithm`, describing the algorithm and the Docker environment it is supposed to be run under.

|Attribute|Type|Description|
|----|-----|-|
|`metadata.algorithm.language`|`string`|Language used to implement the software|
|`metadata.algorithm.version`|`string`|Version of the software preferably in [SemVer](https://semver.org/) notation. E.g. `1.0.0`.|
|`metadata.algorithm.consumerParameters`|[Consumer Parameters](#consumer-parameters)|An object that defines required consumer input before running the algorithm|
|`metadata.algorithm.container`*|`container`|Object describing the Docker container image. See [below](#container) for more details|
|`metadata.additionalInformation`*|`additionalInformation`|Object describing the additional information of the algorithm. See [below](#additional-information) for more details|

\* **Note:** The field `metadata.algorithm.consumerParameters` currently only available on SDK, it is not supported by the current version of Acentrik Marketplace UI. This field allow consumer to parse in custom parameters into the algorithm. Read more about consumer parameters [here](#consumer-parameters).

<br>

##### Container
The `container` object has the following attributes defining the Docker image for running the algorithm:
|Attribute|Type|Description|
|----|-----|-|
|`entrypoint`*|`string`|The command to execute, or script to run inside the Docker image.|
|`image`*|`string`|Name of the Docker image|
|`tag`|`string`|Tag of the Docker image.|
|`checksum`*|`string`|Digest of the Docker image. (ie: sha256:xxxxx)|
|`referenceUrl`*|`string`|URL where data consumer can check the details of the Docker image|

##### Additional information
The `addionalInformation` object has the following attributes containing extra information of the asset:
|Attribute|Type|Description|
|----|-----|-|
|`source`|`string`|This field describes the marketplace instance and will be filled in automatically during the publish.
|`accessPermission`|`string`|This field control the permission of the access of consumer. Fill in `all` to allow all consumer to have access, fill in `deny` to deny all consumer to have access to your asset. Note that you can also set custom permission to allow only certain user to have access. Default value would be `allow`.
|`organization`*|`string`|This field contains the organization address.
|`signer`*|`string`|This field contains the asset provider's wallet address that is connected to their Acentrik marketplace account.
|`algorithmType`*|`string`|The type of the algorithm, value must be `Basic`, `Federated` or `Aggregate`.|


\* **Required**

```
Algorithm metadata example
{ 
  "metadata": { 
    "created": "2020-11-15T12:27:48Z", 
    "updated": "2021-05-17T21:58:02Z", 
    "description": "Sample description", 
    "name": "Sample algorithm asset", 
    "type": "algorithm", 
    "author": "OPF", 
    "license": "https://example-license.com/terms", 
    "algorithm": { 
        "language": "python3.7", 
        "version": "1.0.0", 
      "container": { 
        "entrypoint": "python $ALGO", 
        "image": "ubuntu", 
        "tag": "latest", 
        "checksum": "sha256:44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
        "referenceUrl": "https://google.com",
        "consumerParameters": {}
        }
        },
    "additionalInformation":{
        "source": "",
        "accessPermission": "allow",
        "organization": "",
        "signer": "",
        "algorithmType": "Basic"
        "relatedAggregateAlgorithms": []
    }
  }
} 
```
\* The field `metadata.additionalInformation.relatedAggregateAlgorithms` is required only when the `metadata.algorithmType` is `Federated`. This field contains a list of aggregate algorithm's DIDs that are permitted to conduct aggregate computation once federated computation is finished.

### Consumer parameters

> [!NOTE]
> This function currently only available on SDK, it is not supported by the current version of Acentrik Marketplace UI.

Sometimes, the asset needs additional input data before downloading or running a C2D job. This feature provides flexibility to the algorithm, enabling it to carry out computations that yield the desired outcome for the consumer. Examples:

An algorithm that needs to know the number of iterations it should perform. In this case, the algorithm publisher defines a field called iterations. The buyer needs to enter a value for the iterations parameter. Later, this value is stored in a specific location in the C2D pod for the algorithm to read and use it.

The `consumerParameters` is an array of objects. Each object defines a field and has the following structure:

|Attribute|Type|Description|
|-|-|-|
|`name`*|`string`|The parameter name (this is sent as HTTP param or key towards algo)
|`type`*|`string`|The field type (text, number, boolean, select)|
|`label`*|`string`|The field label which is displayed
|`required`*|`boolean`|If consumer input for this field is mandatory|
|`description`*|`string`|The field description.|
|`default`*|`string`, `number`, or `boolean`|The field default value. For select types, `string` key of default option.
|`options`|Array of `option`|For select types, a list of options.

\* **Required**

Each `option` is an `object` containing a single key: value pair where the key is the option name, and the value is the option value.

```
Consumer parameter example
[
  {
    "name": "hometown",
    "type": "text",
    "label": "Hometown",
    "required": true,
    "description": "What is your hometown?",
    "default": "Nowhere"
  },
  {
    "name": "age",
    "type": "number",
    "label": "Age",
    "required": false,
    "description": "Please fill your age",
    "default": 0
  },
  {
    "name": "developer",
    "type": "boolean",
    "label": "Developer",
    "required": false,
    "description": "Are you a developer?",
    "default": false
  },
  {
    "name": "languagePreference",
    "type": "select",
    "label": "Language",
    "required": false,
    "description": "Do you like NodeJs or Python",
    "default": "nodejs",
    "options": [
      {
        "nodejs": "I love NodeJs"
      },
      {
        "python": "I love Python"
      }
    ]
  }
]
```

Algorithms will have access to a JSON file located at `/data/inputs/algoCustomData.json`, which contains the `keys/values` input data required. Example:

```
Key value received by the algorithm example
{ 
    "hometown": "São Paulo",
    "age": 10, 
    "developer": true, 
    "languagePreference": "nodejs" 
}
```