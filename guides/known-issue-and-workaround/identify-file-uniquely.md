# Identify file uniquely
This method is beneficial when you need to develop a single federated algorithm to process various datasets with differing structures and file types. It is also beneficial for aggregate algorithms, especially when a user intends to assign a specific variable name to each input file.

\* Please be aware that the current version of Acentrik only supports the use of one federated algorithm in a multiple C2D job; using multiple federated algorithms is not possible.

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

# raise an exception if the file is not loaded as one of the expected methods
if 'df' not in locals() and 'others' not in locals():
    raise Exception(f'File input "{path_input_file}" is not accepted, please ensure that the file input is correct!')

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
        raise Exception(f'File input "{path_input_file}" is not accepted, please ensure that the file input is correct!')

# You can uniquely identify the other objects using their type, in this case these objects are sklearn transformers
if 'others' in locals():
    if type(others) == sklearn.preprocessing._data.MinMaxScaler:
        result = joblib.dump(others, scaler_output) # save result to desired filepath
    
    elif type(others) == sklearn.preprocessing._encoders.OneHotEncoder:
        result = joblib.dump(others, encoder_output) # save result to desired filepath

    else:
        # raise exception if file received does not met the condition
        raise Exception(f'File input "{path_input_file}" is not accepted, please ensure that the file input is correct!')
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
\* Note that you might need to perform some processing on the response content to ensure successful loading.. (e.g For .pkl file, the response needs to be converted to bytes using `BytesIO()`. Similarly, for .CSV file response need to convert to string using `StringIO()`)