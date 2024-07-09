# Import Whatever Libraries needed

import json
from pathlib import Path
import os
import logging
import pandas as pd
from zipfile import ZipFile
from PIL import Image

# %% Setup Acentrik Standard Logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', handlers=[logging.StreamHandler()])
logging.info("Starting logging")

# %% Setup Acentrik Standard File Paths

path_input = Path(os.environ.get("INPUTS", "/data/inputs"))
path_output = Path(os.environ.get("OUTPUTS", "/data/outputs"))
path_logs = Path(os.environ.get("LOGS", "/data/logs"))
dids = json.loads(os.environ.get("DIDS", '[]'))
assert dids, f'no DIDS are defined, cannot continue with the algorithm'
did = dids[0]
input_files_path = Path(os.path.join(path_input, did))
input_files = list(input_files_path.iterdir())
first_input = input_files.pop()
path_input_file = first_input
logging.debug(f'got input file: {path_input_file}, {did}, {input_files}')

# Insert your desired Output File Names (can be more than 1 output too with different output file types)
path_output_file = path_output / 'res_customer_preference.xlsx' 
path_output_file2 = path_output / 'Cars_Sold_Per_Year.png'

# %% File Paths Checking
assert path_input_file.exists(), "Can't find required mounted path: {}".format(path_input_file)
assert path_input_file.is_file() | path_input_file.is_symlink(), "{} must be a file.".format(path_input_file)
assert path_output.exists(), "Can't find required mounted path: {}".format(path_output)
logging.debug(f"Selected input file: {path_input_file} {os.path.getsize(path_input_file)/1000/1000} MB")
logging.debug(f"Target output folder: {path_output}")

# %% Load data (can be 1 single file or multiple files)
logging.debug("Loading {}".format(path_input_file))

with open(path_input_file, 'rb') as fh:
    df = pd.read_excel(fh) 
    # df = pd.read_csv(fh)
    # archive = ZipFile(fh, 'r') Ex of reading multiple image files using ZipFile

logging.debug("Loaded {} records into DataFrame".format(len(df)))


# Insert your code logic here
a = pd.DataFrame(df.nlargest(3,'count')['Vehicle Model/ Engine']) 

#Further Logging                  
logging.debug("Built summary of records.")

#Outputing result to file
a.to_excel(path_output_file)

#Further Logging
logging.debug("Wrote results to {}".format(path_output_file))
logging.debug("FINISHED ALGORITHM EXECUTION")