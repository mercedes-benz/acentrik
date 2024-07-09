# Algorithm guide
1. [Compute Environment](#compute-environment)
    - [Build an image](#build-an-image)
    - [About entry point](#about-entry-point)
    - [Environment variables available to algorithms](#environment-variables-available-to-algorithms)
    - [Hardware environment](#hardware-environment)
2. Types of algorithm
    - [Basic](#basic-algorithm)
    - [Federated](#federated-algorithm)
    - [Aggregate](#aggregate-algorithm)
3. [How to write algorithm?](#how-to-write-algorithm)
    - Interesting Implementation
        - [Identify file uniquely](#1-identify-file-uniquely)
        - [Load object via URL](#2-load-object-via-url)
4. [Publishing using SDK](#publish-an-algorithm-using-sdk)

<hr>

Three fundamentals of compute-to-data (C2D)
1. **Algorithm Code:** The algorithm code refers to the specific instructions and logic that define the computational steps to be executed on a dataset. It encapsulates the algorithms' functionalities, calculations, and transformations.
2. **Docker Image:** A Docker image plays a crucial role in encapsulating the algorithm code and its runtime dependencies. It consists of a base image, which provides the underlying environment for the algorithm, and a corresponding tag that identifies a specific version or variant of the image.
3. **Entry Point:** The entry point serves as the starting point for the algorithm's execution within the compute environment. It defines the initial actions to be performed when the algorithm is invoked, such as loading necessary libraries, setting up configurations, or calling specific functions.

<hr>

# Compute environment
A properly configured computing environment is essential for the efficient execution of a C2D task. Creating a customized image that meets the requirements of your algorithm is vital for this purpose. This image should be shared publicly via `docker pull` to enable access. Following this, your algorithm will run within the customized container you have configured.

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

Ensure that the necessary directories are created in your image.
|Path|Usage|
|----|-----|
|`/data/inputs`|Storage for input data sets, accessible only to the algorithm running in the pod. Contents will be the files themselves, inside indexed folders e.g. `/data/inputs/{did}/{service_id}`.|
|`/data/outputs`|Storage for all of the algorithm's output files. They are uploaded on some form of cloud storage, and URLs are sent back to the consumer.|
|`/data/logs`|All algorithm output (such as print, console.log, etc.) is stored in a file located in this folder. They are stored and sent to the consumer as well.

<br>
<br>

After making your Docker image publicly available, please take note of the following information. This information will be required to specify your custom image when publishing an algorithm:
- Docker Registry Path: The name and image tag of your custom image.
- Image Digest: Checksum of your docker image
- Image Reference URL: For consumer to find out more about your image.

#### About entry point
The Docker entrypoint. `$ALGO` is a macro that gets replaced inside the compute job, depending where your algorithm code is downloaded. Define your entry point according to your dependencies. E.g. if you have multiple versions of Python installed, use the appropriate command `python3.6 $ALGO`. Otherwise, `python $ALGO` should serve as the entry point for Python algorithms.

#### Environment variables available to algorithms

For every algorithm pod, the Compute to Data environment provides the following environment variables:
|Variable|Usage|
|----|-----|
|`DIDS`|An array of DID strings containing the input datasets.|
|`TRANSFORMATION_DID`|The DID of the algorithm.|

#### Hardware environment
Ensure that the hardware specifications of the edge node are adequate for running the algorithm. Factors to consider include the number of CPU cores, RAM capacity, algorithm runtime, and the potential utilization of GPU. For instance, when training a model with TensorFlow, verify that the edge node is equipped with GPU support.

<hr>

### Basic algorithm
A basic algorithm performs computations on a single dataset, known as a single compute job. Upon purchasing a compute dataset, the consumer can opt for a compatible algorithm to carry out the computation. The compute environment for the basic algorithm operates without internet access, meaning the algorithm is unable to utilize internet resources like API endpoints during computation. You have the option to enable internet access for the edge node via the edge node configuration, if required.

### Federated algorithm
Similar to the basic algorithm, the federated algorithm can conduct computations on a single dataset. The distinctive feature of a federated algorithm is its capability to perform computations on multiple datasets, referred to as multiple compute jobs. When purchasing a federated algorithm, consumers can choose multiple datasets for computation and then select an aggregate algorithm. The compute environment for the federated algorithm functions without internet access, meaning the algorithm is unable to utilize internet resources like API endpoints during computation. You have the option to enable internet access for the edge node via the edge node configuration, if required.

### Aggregate algorithm
An aggregate algorithm is designed to perform computations on an aggregate dataset and multiple C2D jobs. Following the completion of the initial stage of computation, the federated computation, consumers can proceed with the aggregation process where the output from the federated computation serves as the input for the aggregate algorithm.

\* Note: To enable the aggregate algorithm functionality, it is essential to possess **an aggregate dataset** and designate the aggregate algorithm as a trusted algorithm. The utilization of the aggregate dataset in the aggregate algorithm is optional. Moreover, the compute environment **must have internet access** to retrieve result files from the federated computation..

<hr>

# How to write algorithm?
You can find the complete structure of the algorithms [here](./algorithm). Note that basic algorithm and federated algorithm share the same structure, while there are some differences for aggregate algorithm.

Some useful implementations that may catch your interest:
1. [Identify file uniquely](#1-identify-file-uniquely)
2. [Load object via URL](#2-load-object-via-url)

#### 1. Identify file uniquely
This method is beneficial when you need to develop a single federated algorithm to process various datasets with differing structures and file types. It is also beneficial for aggregate algorithms, especially when a user intends to assign a specific variable name to each input file.

\* Please be aware that the current version of Acentrik only supports the use of one federated algorithm in a multiple C2D job; utilizing multiple federated algorithms is not possible.

\* It is important to note that the implementation of federated algorithms differs from aggregate algorithms. Federated algorithms have their input files preloaded with hexadecimal file names that lack extensions. On the other hand, aggregate algorithms retrieve their input files from the URL of the federated compute job results, which include the file names in the header.

The following code demonstrates how to load various file formats and uniquely identify files for both **basic and federated algorithm**.
``` 
# for basic/federated

#import required library
import json
from pathlib import Path
import os
import pandas as pd
import joblib
import sklearn

# define paths
path_input = Path(os.environ.get("INPUTS", "/data/inputs"))
path_output = Path(os.environ.get("OUTPUTS", "/data/outputs"))
dids = json.loads(os.environ.get("DIDS", '[]'))
did = dids[0]
input_files_path = Path(os.path.join(path_input, did))
input_files = list(input_files_path.iterdir())
first_input = input_files.pop()

path_input_file = first_input

scaler_output = os.path.join(path_output, 'Scaler.pkl')
encoder_output = os.path.join(path_output, 'Encoder.pkl')
mental_health_output = os.path.join(path_output, 'mental_health.csv')
crime_output = os.path.join(path_output, 'crime.csv')

# try to read as csv
try:
    df = pd.read_csv(path_input_file)
except:
    pass

# try to use joblib to load
try:
    others = joblib.load(path_input_file)
except:
    pass

### Add other try-except statements for other loading methods ###

# raise an exception if the file is not laoded as one of the expected methods
if 'df' not in locals() and 'others' not in locals():
    raise Exception(f'File input "{path_input_file}" is not excepted, please ensure that the file input is correct!')

# You can uniquely identify the dataset using the columns the dataset has
if 'df' in locals():
    if 'criminal_records' in df.columns:
        # Identified and do some processing
        df.to_csv(crime_output, index=False) # save result to desired filepath
    
    elif 'mental_health' in df.columns and 'illness' in df.columns:
        # Identified and do some processing
        result = df.to_csv(mental_health_output, index=False) # save result to desired filepath

    else:
        # raise exception if file received does not met the condition
        raise Exception(f'File input "{path_input_file}" is not excepted, please ensure that the file input is correct!')

# You can uniquely identify the other objects using their type, in this case these objects are sklearn transformers
if 'others' in locals():
    if type(others) == sklearn.preprocessing._data.MinMaxScaler:
        result = joblib.dump(others, scaler_output) # save result to desired filepath
    
    elif type(others) == sklearn.preprocessing._encoders.OneHotEncoder:
        result = joblib.dump(others, encoder_output) # save result to desired filepath

    else:
        # raise exception if file received does not met the condition
        raise Exception(f'File input "{path_input_file}" is not excepted, please ensure that the file input is correct!')
```

The following code demonstrates how to load various file formats and uniquely identify files for the **aggregate algorithm**.

```
# for aggregate algorithm

# import required libraries
from io import BytesIO, StringIO
import os
import json 
from urllib import 
import pandas as pd
import joblib
from urllib.parse import 
from pathlib import Path

# get the input data, this is the result from federated computations
path_input = Path(
    os.path.join(os.environ.get("INPUTS", "/data/inputs"), "algoCustomData.json")
)
algoCustomData = {}

with open(path_input, "r") as json_file:
    algoCustomData = json.load(json_file)

result_data = algoCustomData["resultUrls"]

blacklist_df_list = []

# loading each file to their specify variable using file name
for job_data in result_data:
    try:
        # make a https request to retrieve the file
        url = job_data["job_url"]
        headers = job_data["job_headers"]
        req = request.Request(url, headers=headers)  # Create a request with headers
        response = request.urlopen(req)
        
        if response.getcode() == 200:
        
            # retrive the file name
            content_disposition = response.headers['content-disposition']
            filename_index = content_disposition.find('filename=')
            if filename_index != -1:
                filename = content_disposition[filename_index+len('filename='):]
                filename = unquote(filename)  
                filename = filename.strip('"') 
                
            # identify file using file extension and file name
            if filename.lower().endswith('.pkl') and 'scaler' in filename.lower():
                scaler = joblib.load(BytesIO(response.read()))
                
            elif filename.lower().endswith('.pkl') and 'encoder' in filename.lower():
                encoder = joblib.load(BytesIO(response.read()))
                
            elif filename.lower().endswith('.joblib') and 'model' in filename.lower():
                model = joblib.load(BytesIO(response.read()))

            elif filename.lower().endswith('.csv') and 'blacklist' in filename.lower():
                csv_data = response.read().decode("utf-8")
                blacklist_df_list.append(pd.read_csv(StringIO(csv_data)))

            elif filename.lower().endswith('.csv') and 'crime' in filename.lower():
                csv_data = response.read().decode("utf-8")
                crime_df = pd.read_csv(StringIO(csv_data))

            elif filename.lower().endswith('.csv') and 'mental_health' in filename.lower():
                csv_data = response.read().decode("utf-8")
                mental_health_df = pd.read_csv(StringIO(csv_data))

            elif filename.lower().endswith('.csv') and 'registration' in filename.lower():
                csv_data = response.read().decode("utf-8")
                registration_df = pd.read_csv(StringIO(csv_data))

    except Exception as e:
        raise Exception(f"Error fetching data from URL: {url}, error: {e}")
```
\* Note that you might need to perform some processing on the response content to ensure successful loading.. (e.g For .pkl file, the response need to be converted to bytes using `BytesIO()`. Similarly, for .CSV file response need to convert to string using `StringIO()`)


#### 2. Load object via URL
You have the option to upload necessary objects that are not in .CSV format via URL if you prefer not to create or upload the object as a dataset. For instance, you may want to utilize a trained machine learning model in your algorithm without making it published as a dataset. **This method is applicable for all algorithm type.**


**Pre-requisite**:
- Ensure that the compute environment **has internet access**.
- Ensure that the object is accessible via the internet. You can upload it to a hosting platform like GitHub or AWS S3 bucket.

```
import joblib
from io import BytesIO
from urllib import request

url = 'https://link-to-your-object'

# function to load object via URL
def load_from_url(url):
    req = request.Request(url) # you may want to add header, authentication or others if require
    response = request.urlopen(req)

    if response.getcode() == 200:
        return joblib.load(BytesIO(response.read())) # modified this line to suits the loading requirement for your object

    # raise exception if could not be loaded
    raise Exception(f'Error: Object could not be loaded from url ({url})')

loaded_object = load_from_url(url)

```
# Publish an algorithm using SDK
hen publishing the algorithm using the SDK tool, it is important to pay attention to the algorithm metadata. An asset of type `algorithm` has additional attributes under `metadata.algorithm`, describing the algorithm and the Docker environment it is supposed to be run under.

|Attribute|Type|Description|
|----|-----|-|
|`metadata.algorithmType`*|`string`|The type of the algorithm, value must be `Basic`, `Federated` or `Aggregate`.|
|`metadata.algorithm.language`|`string`|Language used to implement the software|
|`metadata.algorithm.version`|`string`|Version of the software preferably in [SemVer](https://semver.org/) notation. E.g. `1.0.0`.|
|`metadata.algorithm.container`*|`container`|Object describing the Docker container image. See below|

<br>

The `container` object has the following attributes defining the Docker image for running the algorithm:
|Attribute|Type|Description|
|----|-----|-|
|`entrypoint`*|`string`|The command to execute, or script to run inside the Docker image.|
|`image`*|`string`|Name of the Docker image|
|`tag`|`string`|Tag of the Docker image.|
|`checksum`*|`string`|Digest of the Docker image. (ie: sha256:xxxxx)|
|`referenceUrl`*|`string`|URL where data consumer can check the details of the Docker image|

\* Required

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
    "license": "https://market.oceanprotocol.com/terms", 
    "algorithmType": "Basic"
    "algorithm": { 
        "language": "python3.7", 
        "version": "1.0.0", 
      "container": { 
        "entrypoint": "python $ALGO", 
        "image": "ubuntu", 
        "tag": "latest", 
        "checksum": "sha256:44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550" 
        }, 
        "referenceUrl": "https://google.com"
        },
    "additionalInformation":{
        "source": "",
        "accessPermission": "allow",
        "organization": "",
        "signer": "",
        "relatedAggregateAlgorithms": []
    }
  }
} 
```
\* The field `metadata.additionalInformation.relatedAggregateAlgorithms` is required only when the `metadata.algorithmType` is `Federated`. This field contains a list of aggregate algorithms' DIDs that are permitted to conduct aggregate computation once federated computation is finished.