# Code adapted from Author: Ahmet Taspinar, data: 2018, Availability: https://github.com/taspinar/twitterscraper 
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProjectStock.settings'

import django
django.setup()

import requests
import csv, io
from csv import writer
from Stocks.models import StockDetail
from datetime import datetime,date,time,timedelta
from twitterscraper import query_tweets


# this will query tweets from yesterday to today's date and save them into the repective CSV file
count=0
stockTicker = StockDetail.objects.all()
Previous_Date = date.today() - timedelta(days=1)

for ticker in stockTicker:
    with open('twitter_tweets/{}.csv'.format(ticker.stock_symbol),'w') as f:
        csv_writer = writer(f)
        headers = ['Tweet']
        csv_writer.writerow(headers)
        count+=1
        
        for tweet in query_tweets("${}".format(ticker.stock_symbol),20, Previous_Date):
            csv_writer.writerow([tweet.text])
    print(count)
    
print("all done")