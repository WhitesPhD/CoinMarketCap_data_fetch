#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Daniele Bianchi, d.bianchi@qmul.ac.uk, whitesphd.com
"""

from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import time

def fetch_historical_data(crypto_id: int, api_key: str, start_date: str, end_date: str, fiat: str, interval: str):
    
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'
    
    # Convert datetime objects to timestamps
    start = int(start_date.timestamp())
    end = int(end_date.timestamp())
    
    parameters = {
        'id': crypto_id,
        'time_start': start,
        'time_end': end,
        'convert': fiat,
        'count': 10000,  # Check if 'count' is a valid parameter for your API endpoint
        'interval': interval,
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    
    if response.status_code == 200:
        
        data = response.json().get('data', {})
        name = data.get('name')
        symbol = data.get('symbol')
        quotes = data.get('quotes', [])
        
        df_results = pd.DataFrame()  # Initialize an empty DataFrame

        for item in quotes:  # Iterate through each item in the data list
            # Flatten the nested structure and exclude specific keys
            flat_data = {**item['quote']['USD']}
            flat_data['timestamp'] = item['time_close']  # Assigning the timestamp for reference
            flat_data['name'] = name  # Add the name to each row
            flat_data['symbol'] = symbol  # Add the symbol to each row
            
            # Convert the flattened dictionary into a DataFrame and append it to the results
            df = pd.DataFrame([flat_data])  # Convert dictionary into a DataFrame
            df_results = df_results.append(df, ignore_index=True)
        
        return df_results
    else:
        print(f'Failed to retrieve data for ID {crypto_id}: Error code {response.status_code}')
        return None


def fetch_crypto_metadata(api_key: str, crypto_id: int):
    
    url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'

    parameters = {
        'id': crypto_id,
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)

       # Check if response is successful
    if response.status_code == 200:
        data = response.json().get('data', {}).get(str(crypto_id))

        # Check if data was found
        if data:
            # Flatten urls by creating new keys
            for key, value in data['urls'].items():
                # Only add if the list is not empty
                data[f'url_{key}'] = ', '.join(value) if value else ''

            # Remove the original 'urls' field as it's now flattened
            del data['urls']

            # Convert the modified dictionary into a DataFrame
            df = pd.DataFrame([data])  # Pass the dictionary as a list
            return df
        else:
            print(f"No data found for cryptocurrency with ID {crypto_id}")
            return None
    else:
        print(f"Failed to retrieve data: Error code {response.status_code}")
        return None
    


def fetch_historical_global_metrics(api_key: str, start_date: str, end_date: str, interval: str):
    url = 'https://pro-api.coinmarketcap.com/v2/global-metrics/quotes/historical'  # Hypothetical endpoint

    # Convert datetime objects to timestamps
    start = int(start_date.timestamp())
    end = int(end_date.timestamp())

    parameters = {
        'time_start': start,  # Format: 'YYYY-MM-DD'
        'time_end': end,      # Format: 'YYYY-MM-DD'
        'interval': interval, # e.g., 'daily'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response   = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        data = response.json().get('data', {}).get('quotes', [])

        df_results = pd.DataFrame()  # Initialize an empty DataFrame

        for quote in data:  # Fixed iteration over 'data'
            # Flatten the nested 'quote' dictionary
            flat_data = {
                **quote,
                **quote['quote']['USD']  # Merge the inner USD dictionary into the main dictionary
            }
            del flat_data['quote']  # Remove the original nested 'quote' field

            # Convert the flattened dictionary into a DataFrame and append it to the results
            df = pd.DataFrame([flat_data])  # Convert dictionary into a DataFrame
            df_results = df_results.append(df, ignore_index=True)

        return df_results
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def fetch_coin_category_info(api_key: str, category_id: str):

    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'  # Hypothetical endpoint
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accepts': 'application/json'
    }
    
    parameters = {
        'id': category_id,
        'limit': 1000,
        }
    
    response = requests.get(url, headers=headers, params=parameters)
    
    if response.status_code == 200:
        # Assuming the data structure is consistent with CoinMarketCap's standards
        category_data = response.json().get('data', {})
        return category_data
    else:
        print(f"Failed to fetch data for category {category_id}: {response.status_code}")
        return {}

    
    
    
    