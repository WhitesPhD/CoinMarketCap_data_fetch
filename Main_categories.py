#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Daniele Bianchi, d.bianchi@qmul.ac.uk, whitesphd.com
"""

import requests
from datetime import datetime, timedelta
from Coinmarketcap_functions import *
import pandas as pd

api_key = 'put your API key here'

# Get the list of coin categories 

categories = fetch_coin_categories(api_key)
file_name = f'list_of_categories.csv'
categories.to_csv(file_name, index=False)

data_categories = {}
for w in range(len(categories)):
    
    category_id = categories.loc[w, 'id']
    
    temp = fetch_coin_category_info(api_key, category_id)    
    data_categories[categories.loc[w, 'name']] = temp

    time.sleep(1)  # Respect the API's rate limit
    print(f"Retrieved category {categories.loc[w, 'name']}.")

file_name = 'data_categories.json.gz'
# Convert the dictionary to JSON and compress it
with gzip.open(file_name, 'wt', encoding='UTF-8') as zipfile:
    json.dump(data_categories, zipfile)

