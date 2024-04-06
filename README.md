# CoinMarketCap_data_fetch
Codes and functions you can use to fetch historical and latest data from CoinMarketCap, subject to having a pro API key 

The folder contains:
CoinMarketCap_functions.py: A series of functions that allows to fetch data from CoinMarketCap API
  1. fetch_historical_data.py: can be used to get historical time series data for all pairs (against your preferred fiat) available on CMC
  2. fetch_crypto_metadata.py: can be used to get the metadata for each cryptocurrency available in CMC
  3. fetch_historical_global_metrics.py: can be used to get historical global information on the market
  4. fetch_coin_category_info.py: can be used to get information on each category of cryptocurrency

Main_categories.py is a script that can be used to implement fetch_coin_category_info.py
Main_global_metrics.py is a script that can be used to implement fetch_historical_global_metrics.py
Main_request_historical.py is a script that can be used to implement fetch_historical_data.py
Main_metadata.py is a script that can be used to implement fetch_crypto_metadata.py

Note you need a subscription to CoinMarketCap to use these functions, as they are subject to having your own API key. The scripts assume you own a pro API, so check with your subscription if it works. Errors and mistakes are my own. 

