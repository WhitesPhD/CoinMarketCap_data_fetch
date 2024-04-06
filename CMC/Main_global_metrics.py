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

start_date  = datetime(2013, 4, 28)
end_date    = datetime.now()
interval    = 'daily'

# Get global metrics

df = fetch_historical_global_metrics(api_key, start_date, end_date, interval)
file_name = f'global_metrics.csv'
df.to_csv(file_name, index=False)

