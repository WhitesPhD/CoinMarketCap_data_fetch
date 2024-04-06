#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Daniele Bianchi, d.bianchi@qmul.ac.uk, whitesphd.com
"""

import requests
import json
from datetime import datetime, timedelta
from Coinmarketcap_functions import *
import pandas as pd
import time
import gzip


api_key = 'put your API key here'

# Fetch the full list of cryptocurrencies you want to obtain. 
# If you have your list you can skip this part

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

response = requests.get(url, headers=headers)
if response.status_code == 200: #Check you get a correct response
    # Convert the response to JSON format
    data = response.json()
    
    # Extract the list of cryptocurrencies. 
    cryptocurrencies = data['data']
        
    # Optionally, you can save this list to a json file
    with open('cryptocurrencies.json', 'w') as f:
        json.dump(cryptocurrencies, f, indent=4)
        
else:
    print(f'Failed to retrieve data: Error code {response.status_code}')

# Fetch the metadata for each cryptocurrency 
df_results = pd.DataFrame()

for w in range(len(cryptocurrencies)):
    
    crypto_id  = cryptocurrencies[w].get('id')
    df         = fetch_crypto_metadata(api_key, crypto_id)

    # Check if the dataframe is not None before appending
    if df is not None:
        df_results = df_results.append(df, ignore_index=True)
        print(f"Retrieved cryptocurrency {w}.")
    else:
        print(f"Failed to retrieve data for cryptocurrency {w}.")
    
    time.sleep(1)  # Respect the API's rate limit

file_name       = f'meta_data.csv'
df_results.to_csv(file_name, index=False)


        
        