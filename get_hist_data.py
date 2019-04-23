# Libray used iexfinance 0.4.0, Author: Addison Lynch, Last modified 21 Feb 2019, Avaialbility: https://github.com/addisonlynch/iexfinance

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProjectStock.settings'

import django
django.setup()

from datetime import datetime,date,time,timedelta
from iexfinance.stocks import get_historical_data
import pandas as pd

from Stocks.models import StockDetail

print('currently in the get_stock function')
stockTicker = StockDetail.objects.all()

start = datetime(2017, 1, 1)
end = datetime.now()
for ticker in stockTicker:
    print('inside the loop creating the files:')
    print(ticker)

    if not os.path.exists('stock_data/{}.csv'.format(ticker.stock_symbol)):
        df = get_historical_data(ticker.stock_symbol, start, end, output_format='pandas')
        df.to_csv('stock_data/{}.csv'.format(ticker.stock_symbol))
    else:
        print('Already have {}'.format(ticker.stock_symbol))
        df = get_historical_data(ticker.stock_symbol, start, end, output_format='pandas')
        df.to_csv('stock_data/{}.csv'.format(ticker.stock_symbol))

print("all done")