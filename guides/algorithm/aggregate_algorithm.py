# This algorithm structure is applicable for aggregate algorithm

import pandas as pd
import logging
from pathlib import Path
import os
import json 
from urllib import request
from io import StringIO

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', handlers=[logging.StreamHandler()])
logging.info('Starting logging')

# Setup paths using environment variables / default values
path_input = Path(os.environ.get('INPUTS', '/data/inputs')) # this allows you to get all input, include the job result from federated computation and the aggregate algorithm

path_output = Path(os.environ.get('OUTPUTS', '/data/outputs')) # get the output directory
path_logs = Path(os.environ.get('LOGS', '/data/logs')) # get the log directory

# load aggregate dataset if you want to use aggregate dataset
dids = json.loads(os.environ.get('DIDS', '[]'))

if dids:
    did = dids[0]
    aggregate_dataset_files_path = Path(os.path.join(path_input, did)) # this contains the aggregate dataset 
    input_files = list(aggregate_dataset_files_path.iterdir())
    aggregate_input = input_files.pop()

    aggregate_df = pd.read_csv(aggregate_input)
    logging.debug(f'Loaded aggregate dataset: {aggregate_input}')
else:
    logging.warning('no DIDS are defined')


# load result of the federated computation
try: 
    fed_result_files_path = Path(os.path.join(path_input, 'algoCustomData.json')) # this contains the federated job result URL and consumer parameters if available
    with open(fed_result_files_path, 'r') as json_file:
        algoCustomData = json.load(json_file)

    result_data = algoCustomData['resultUrls']
except Exception as e:
    logging.debug(f'Error fetching federated result: {e}')



# modify as required
data_frames = []
for job_data in result_data:
    try:
        url = job_data['job_url']
        headers = job_data['job_headers']
        req = request.Request(url, headers=headers)  # Create a request with headers
        response = request.urlopen(req)

        if response.getcode() == 200:
            csv_data = response.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_data))
            data_frames.append(df)
        else:
            logging.debug(f'Response data code {response.getcode()}, fail to get result')

    except Exception as e:
        logging.debug('Error fetching data from URL:', e)
logging.debug(f'Loaded input files from federated compute result. A total of {len(data_frames)} result is loaded.')


# you can define the output path here, either method works
path_output_file_A = path_output / 'output_A.csv' # method 1
path_output_file_B = os.path.join(path_output, 'output_B.csv') # method 2 

# Suggest to use method 2, some Python library only accept string file path 
# when saving their object, (e.g. plotly interactive graph) 

# If you want to use method 1, you can also convert the Path object to 
# string before saving object


# Insert your code logic here
if data_frames:
    logging.debug('Processing data frame')
    data_frames.append(aggregate_df)
    combined_df = pd.concat(data_frames, ignore_index=True)
    column_averages = combined_df.mean().to_frame().T
    column_averages.columns = combined_df.columns
    column_averages.to_csv(path_output_file_A, index=False)
    logging.debug('Wrote results to {}'.format(path_output_file_A))
else:
    logging.debug('No data frame found that can be process')


#Further Logging
logging.debug('FINISHED ALGORITHM EXECUTION')