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

# Define the time series you need (boundaries), the fiat currency you want the 
# prices to be expressed and the sample frequency. For a full description of the 
# available fiat currencies and frequencies you should check the CoinMarketCap API 
# documentation

start_date  = datetime(2013, 4, 28)
end_date    = datetime.now()
fiat        = 'USD'
interval    = 'daily'

# Fetch the historical prices and volumes for all cryptocurrencies in the list

df_results  = pd.DataFrame()

for w in range(len(cryptocurrencies)):
    
    crypto_id  = cryptocurrencies[w].get('id')
    
    # To fetch the data you use the fetch_historical_data function
    df         = fetch_historical_data(crypto_id, api_key, start_date, end_date, fiat, interval)
    
    # Check if the dataframe is not None before appending
    if df is not None:
        df_results = df_results.append(df, ignore_index=True)
        print(f"Retrieved cryptocurrency {w}.")
    else:
        print(f"Failed to retrieve data for cryptocurrency {w}.")
    
    time.sleep(1)  # Respect the API's rate limit (check API documentation)

# Convert the DataFrame to a JSON string without line delimiters
json_str = df_results.to_json(orient='records')

file_name = f'name_you_prefer..gz'

# Compress and save the JSON string
with gzip.open(file_name, 'wt', encoding='utf-8') as f:
    f.write(json_str)

# save the file as a compressed json to save space 
file_name = f'market_data.json.gz'
df_results.to_json(file_name, orient='records', lines=True, compression='gzip')



        
        
        