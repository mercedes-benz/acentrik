# Output multiple files from federated result to aggregate algorithm
In the current version of Acentrik, the aggregate function will only consider the initial output from each federated compute job. If you require the aggregate algorithm to process multiple outputs from the federated compute jobs, you will need to incorporate additional code to fetch these outputs, which can be a complex task.

A simpler approach would involve zipping the files within your federated algorithm and then unzipping them in the aggregate algorithm. This can be achieved using the Python library `zipfile`.

Alternatively, you could store all objects in a `.pkl` file. The benefit of this method is that you will only need to read the `.pkl` file once in the aggregate algorithm, allowing you to directly access the objects within your loaded object.

Below is an example demonstrating how you can utilize the joblib method to load more than one output from a federated compute job into the aggregate algorithm.

**Federated Algorithm**
```
import joblib
import os
import pandas as pd

path_output = Path(os.environ.get("OUTPUTS", "/data/outputs"))
file_output = os.path.join(path_output, f'output.pkl') # define output file

model = XGBRegressor(random_state=42) # machine learning model
df = pd.DataFrame() # Pandas dataframe

joblib.dump({'dataframe': df, 'model': model}, file_output) # save object in their repective variable
```

**Aggregate Algorithm**
```
import joblib
import os
import pandas as pd
from io import BytesIO
from urllib import request
from pathlib import Path
import json

path_input = Path(
    os.path.join(os.environ.get("INPUTS", "/data/inputs"), "algoCustomData.json")
)
with open(path_input, "r") as json_file:
    algoCustomData = json.load(json_file)

result_data = algoCustomData["resultUrls"] # retrieve federated job result URLs

for job_data in result_data:
    try:
        url = job_data["job_url"]
        headers = job_data["job_headers"]
        req = request.Request(url, headers=headers)  # Create a request with headers
        response = request.urlopen(req)
        
        if response.getcode() == 200:

            # load model and dataframe
            if filename.lower().endswith('.pkl'):
                loaded_objects = joblib.load(BytesIO(response.read())) # load the object once
                df_loaded = loaded_objects['dataframe'] # access the dataframe directly
                model_loaded = loaded_objects['model'] # access the model directly
                dfs.append(df_loaded)
                models.append(model_loaded)
```