# This algorithm structure is applicable for both basic and federated algorithm

import json
from pathlib import Path
import os
import logging
import pandas as pd


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', handlers=[logging.StreamHandler()])
logging.info('Starting logging')

# Setup paths using environment variables / default values

path_input = Path(os.environ.get('INPUTS', '/data/inputs'))
path_output = Path(os.environ.get('OUTPUTS', '/data/outputs'))
path_logs = Path(os.environ.get('LOGS', '/data/logs'))
dids = json.loads(os.environ.get('DIDS', '[]'))
assert dids, f'no DIDS are defined, cannot continue with the algorithm'
did = dids[0]
input_files_path = Path(os.path.join(path_input, did))
input_files = list(input_files_path.iterdir())
first_input = input_files.pop()

path_input_file = first_input # this contains the dataset

# to retrieve consumer parameters if available, note that this function currently on available on SDK
# it is not supported on Acentrik marketplace UI 
# consumer_parameter_files_path = Path(os.path.join(path_input, 'algoCustomData.json'))

# you can define the output path here, either method works
path_output_file_A = path_output / 'output_A.csv' # method 1
path_output_file_B = os.path.join(path_output, 'output_B.csv') # method 2 

# Suggest to use method 2, some Python library only accept string file path 
# when saving their object, (e.g. plotly interactive graph) 

# If you want to use method 1, you can also convert the Path object to 
# string before saving object

# optional checking 
assert path_input_file.exists(), 'Can\'t find required mounted path: {}'.format(path_input_file)
assert path_input_file.is_file() | path_input_file.is_symlink(), '{} must be a file.'.format(path_input_file)
assert path_output.exists(), 'Can\'t find required mounted path: {}'.format(path_output)
logging.debug(f'Selected input file: {path_input_file}, Size: {os.path.getsize(path_input_file)/1000/1000} MB')
logging.debug(f'Target output folder: {path_output}')

# load dataset
try:
    df = pd.read_csv(path_input_file)
    logging.debug(f'Loaded dataset: {path_input_file}')

    logging.debug('Loaded {} records into DataFrame'.format(len(df)))
except Exception as e:
    logging.debug(f'Load data frame from: {path_input_file} with error: {e}')


# Insert your code logic here
try:
    a = df.sum(axis=0)
    b = df.sum(axis=1)

    #Further Logging                  
    logging.debug('Built summary of records.')

    #Outputing result to file
    a.to_csv(path_output_file_A)
    b.to_csv(path_output_file_B)

    #Further Logging
    logging.debug('Wrote results to {}'.format(path_output_file_A))
    logging.debug('Wrote results to {}'.format(path_output_file_B))
except Exception as e:
    logging.debug(f'Processing data fail with error: {e}')

logging.debug('FINISHED ALGORITHM EXECUTION')

