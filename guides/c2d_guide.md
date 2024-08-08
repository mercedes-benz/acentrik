# Acentrik compute-to-data Handbook
1. [Compute-to-data on Acentrik](#compute-to-data-on-acentrik)
2. [Benefit of using C2D](#benefit-of-using-c2d)
3. [When to use C2D](#when-to-use-c2d)
4. [Data asset ownership scenarios in C2D](#data-asset-ownership-scenarios-in-c2d)
    1. [Data Owner provides both datasets and algorithms](#1-data-owner-provides-both-datasets-and-algorithms)
    2. [Data Owner only provides datasets while algorithm is owned by another party](#2-data-owner-only-provides-datasets-while-algorithm-is-owned-by-another-party)
    3. [Algorithm Creator who only provides algorithms, while dataset is owned by another party](#3-algorithm-creator-who-only-provides-algorithms-while-dataset-is-owned-by-another-party)
5. [Best practices](#best-practices)
6. [Other aspects of C2D](#other-aspects-of-c2d)
    1. [Pricing mechanism](#1-pricing-mechanism)
    2. [Checksum](#2-checksum)
    3. [Testing of algorithms before publishing or adding into the allowlist](#3-testing-of-algorithms-before-publishing-or-adding-into-the-allowlist)
    4. [Query parameter and HTTP header option for your API endpoint when creating a dataset asset or algorithm](#4-query-parameter---and-http-header-option-for-your-api---endpoint-when-creating-a-dataset-asset-or-algorithm)
    5. [Recommended size of dataset; minimum resources required](#5-recommended-size-of-dataset-minimum-resources-required)
7. [Technical FAQ](#technical-faq)
    1. [What are the components of C2D?](#1-what-are-the-components-of-c2d)
    2. [How does the architecture of C2D look like?](#2-how-does-the-architecture-of-c2d-look-like)
    3. [How do I setup/install the C2D component](#3-how-do-i-setupinstall-the-c2d-component)
    4. [Container Registry](#4-container-registry)
    5. [SDK](#5-sdk)
    6. [Custom Docker Image](#6-custom-docker-image)

<hr>

### Compute-to-data on Acentrik
Compute-to-Data (C2D) is a means to exchange data while preserving privacy by allowing the data to stay on-premise with the data provider, allowing data consumers to run compute jobs on the data. 

Acentrik is a decentralized enterprise-grade data marketplace platform that uses C2D, which functionality solves the current tradeoff between the benefits of using private data and the risks of exposing it. 

For data consumers, the most important advantage of C2D is the ability to access hard-to-get private data of other enterprises, which is valuable to gain further insights to their company/industry. At the same time, for data providers, the process of monetizing private data by selling it without leaving their premises guarantees the security and privacy of their data assets. 

<hr>

### Benefit of using C2D
- Faster and easier to extract useful information from data assets directly
- Get access to more accurate information from algorithm models that are continuously trained based on extensive and massive data
- Obtain recommendations and suggestions on ways to extract valuable insights provided by algorithms from C2D
- Added values from datasets could be discovered through algorithms created by others (Ex. feature engineering, data visualizations, etc)

<hr>

### When to use C2D
- If you need to acquire private data that can be used by your algorithms 
- If you are willing to run and shoulder the cost of a private edge node infrastructure
- If you want to keep utilization of data in a private context
- If you would like to explore and validate more algorithms for your datasets, with active collaboration with Algorithm Creators

<hr>

### Data asset ownership scenarios in C2D

##### 1. Data Owner provides both datasets and algorithms
In this scenario, the Data Owner is in charge of the datasets and algorithms, and should set up their own private edge computing node. This scenario provides the most secure method for preserving one's private data as it will only be managed by the Data Owner on their own edge node. With their own algorithm and dataset, the Data Owner will have full control of the compute job output, and hence the result of what the Data Consumers are purchasing. Additionally, it could serve as an example for other Algorithm Creators to create algorithms suitable for their datasets, increasing the datasets’ computing potential and therefore potentially increase monetization.

##### 2. Data Owner only provides datasets while algorithm is owned by another party
In the second scenario, the Data Owner just provides the datasets without the algorithm. Consent is required for other private algorithms to run on their datasets, by inspecting malicious codes that could leak or harm private data. In order to encourage collaboration with more Algorithm Creators to develop algorithms for their datasets, it is recommended to provide small sample or test data that could be utilized for experimental purposes. 

##### 3. Algorithm Creator who only provides algorithms, while dataset is owned by another party
In the last scenario, Algorithm Creators can propose to pair their algorithms with any datasets that allows computation. Once verified by the Data Owner, Algorithm Creators can start monetizing from their algorithms from compute jobs. In order for the algorithms to be verified, mutual communication needs to take place outside of Acentrik, so that both parties can explore ways to develop the Algorithms more efficiently.

<hr>

### Best practices
- Ensure Personally Identifiable Information (PII) is not included in the result of the compute job created by your algorithms.
- Ensure a proper setup of adhering to the guidelines for setting up a private edge computing node, including the minimum resources required. 
- We highly encourage Data Owners to provide sample files, sample screenshots and detailed description with master data information so that data consumers or algorithm creators can know the dataset better.
- Never include malicious code or inappropriate content into your algorithm.

<hr>

### Other aspects of C2D

##### 1. Pricing mechanism
- Stablecoins such as USDC are used in Acentrik to price the data assets in order to avoid the volatility issues that cryptocurrencies are prone to
- Data Owners could price their experimental datasets for free in the marketplace in order to estimate the demand of the actual data
- Datasets and algorithms are priced independent of each other
- Data Owners can take the estimated infrastructure resource fees into account and factor it in as a price variable for their datasets

##### 2. Checksum
- A checksum is used to enhance the security for a Data Owner’s private data as it checks the integrity of the algorithms and docker container paired with it.
- It will issue a warning to the Data Owner if either the algorithm or its docker container has been modified. The modified algorithm will then be automatically unavailable for selection during a possible purchase action. This prevents any malicious actions that may occur in the private data during the compute process.
- When the warning is issued, the Data Owner is advised to contact the Algorithm Owner and verify the changes. Once verified, the Data Owner needs to acknowledge updates of the algorithms in order to remove the warning and continue using the algorithm paired with the dataset.

##### 3. Testing of algorithms before publishing or adding into the allowlist
- If sample data and detailed metadata are provided by the Data Owner, the Algorithm Owner can create their algorithms based on that
- If Data Owner has another experimental dataset on the Public marketplace as a sneak peek of their Private data, the Algorithm Owner can create your algorithms based on that as well
- In order to comply with Acentrik’s standard code structure (such as logging and file path) and also to ensure it is error-free, a sample algorithm with the required blocks of code will be included and you will just need to insert your algorithm logic along with input and output path. Sample algorithm reference: https://github.com/mercedes-benz/acentrik/blob/main/guides/algorithm/structure.py

![Alt text](/guides/handbook-6iii.png)

##### 4. Query parameter and HTTP header option for your API endpoint when creating a dataset asset or algorithm
- Query Parameter option enables a Dataset Owner to allow more specific data to be fetched from your endpoint, whereas a HTTP header is primarily used to enter your private API Key.
- For Query Parameter, it is required to have a display name, a parameter key, and a parameter type while a description to describe the parameter usage is optional but highly recommended.
- For HTTP Header, it is required to have a Header Name and a value for your API Key. 
- If the Query Parameter option is enabled by the asset owner, it is mandatory to put in value for the parameters specified and so, detailed documentation on parameters usage should be included in the description column here under parameters.
- Since multiple parameters are allowed, you can insert multiple parameters for one asset as long as it is prohibited by the API. If not, you will need to create another new asset with different parameters set up.
- Also, since the parameter type is mandatory to input with the purpose to limit errors in creating a successful API connection, if there are comma-delimited strings (e.g. Sam,John), do note that it would not be considered. 

##### 5. Recommended size of dataset; minimum resources required
- To support C2D, it is mandatory to use your own private edge computing node and so, the recommended dataset size and also minimum resources required are actually depending on the Data Owner’s setup
- For Data Owners, make sure your own infrastructure of private edge computing node is able to support your own dataset and is able to scale up with no issues.
- The minimum resources required are as follows:

<br>


|Minimum Infrastructure Requirements||
|-|-|
|Kubenetes Cluster|1|
|Kubenetes Node|2 vCPU, 4GB RAM x 2|
|PostgreSQL|0.5 vCPU, 1GB RAM x 1|
|Redis|Optional (Required redis if enable HA on edge node)|
|Compute temporary storage (Kubenetes Persistent volume)|On demand x Jobs|
|Compute Output Storage|S3 or IPFS|

|**Application Stack Requirements (Kubernetes Object Resources)**||
|-|-|
|Deployment: Provider|0.5 vCPU, 1GB RAM x 1|
|Deployment: Operator-Service|0.5 vCPU, 1GB RAM x 1|
|Deployment: Compute-Engine|0.5 vCPU, 0.25GB RAM x 1|
|Job: Configuration / Algorithm / Filtering / Publish|1 vCPU, 0.5GB RAM x N (Amount of Jobs)|
|Total vCPU & RAM for Application (Minimum)|0.5 + 0.5 + 0.5 + 1 vCPU = **2.5 vCPU** <br> 1GB + 1GB + 0.25 + 0.5 RAM = **2.75GB RAM**|

<hr>

### Technical FAQ
##### 1. What are the components of C2D?

Currently, C2D consists of 3 main components, collectively known as the “Edge Node Cluster”.
- Edge Node (Provider) – Component that manages and proxies the marketplace request to actual asset URL and Compute-to-Data components
- Operator API (Operator Service) – Component that manages compute job execution schedule, existing job state and download computed result(s)
- Ocean Compute Operator (Operator Engine) – Component that defines compute job resources and spawn container instance to run compute jobs

##### 2. How does the architecture of C2D look like?

The C2D infrastructure is set up as a Kubernetes (K8s) cluster e.g on AWS or Azure in the background. This Kubernetes cluster is responsible for running the actual compute jobs (each compute job runs in an isolated Kubernetes Pod), out of sight for marketplace clients and end-users. 

![Alt text](/guides/handbook-7ii.png)

Typically, the consumer calls the ‘Edge Node provider’ to start a job -- ensuring that the consumer has the respective datatoken access. Then it calls the ‘operator API’, creating the compute job workflow. The ‘ocean compute operator’ then retrieves the workflows created by ‘operator API’ in the Kubenetes Cluster, allowing it to:
1. Orchestrate the flow of the execution
2. Start the configuration pod to download the workflow dependencies (datasets and algorithms)
3. Start the execution pod to execute the compute job
4. Start the publishing pod to publish the compute result artifacts into storage

##### 3. How do I setup/install the C2D component 

There are helm charts available to install the C2D components in Kubenetes. You can modify the helm chart according to your own Kubenetes cluster setup. Alternatively, you can deploy the standard Kubernetes objects by creating your own deployment yaml files. 

You can read more about helm charts here: https://github.com/mercedes-benz/acentrik/tree/main/helm-charts

##### 4. Container Registry 
By default, all helm charts are predefined with public docker images available in Acentrik's Amazon Elastic Container Registry (Amazon ECR), as following public registry: 
“public.ecr.aws/acentrik"

##### 5. SDK 
SDK is a python library that user can utilize to publish, consume asset, and run a C2D job on Acentrik without using the marketplace interface. User just need to install the python library and run the script or python command. 

You can read more about the SDK here: https://github.com/mercedes-benz/acentrik/tree/main/sdk

##### 6. Custom Docker Image 
Custom Docker Image is now supported, and user can use their own public docker image to run algorithms. User would need to put in the details of their custom docker image under the runtime environment section during algorithm creation. There will be 4 different sections:
1. Public Docker Image (public-docker-repository/image-name)
2. Docker Image Digest (sha256:xxxxxxx)
3. Docker Image EntryPoint (python $ALGO)
4. Docker Image Reference URL (https://xxxx)
      
You can find a a template to create the Dockerfile for your custom docker image creation [here](/guides/how-to-write-algorithm_guide.md#build-an-image).

Find more about compute environment [here](/guides/how-to-write-algorithm_guide.md#compute-environment).
       


