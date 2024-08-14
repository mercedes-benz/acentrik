# Load object via URL instead of publishing as compute dataset
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