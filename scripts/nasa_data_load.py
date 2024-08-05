import requests
import pandas as pd
response = requests.get(
    'https://data.nasa.gov/resource/gh4g-9sfh.json',
    params={'$limit':50_000}
)
if response.ok:
    payload=response.json()
    #print(payload)
else:
    print(f'request was not successful and return code:{response.status_code}')

df= pd.DataFrame(payload)
print(df.head(3))