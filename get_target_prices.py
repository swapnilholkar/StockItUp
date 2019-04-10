import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProjectStock.settings'

import django
django.setup()

import requests
from bs4 import BeautifulSoup
import csv, io
from csv import writer

get_yahoo_target_prices()
get_nasdaqSite_target_prices()
get_stocktargetadvisior_target_prices()

def get_yahoo_target_prices():
    stockTicker = StockDetail.objects.all()

    for ticker in stockTicker:
        response = requests.get('https://uk.finance.yahoo.com/quote/{}'.format(ticker.stock_symbol))
        soup = BeautifulSoup(response.text,'html.parser')
        spanTags = soup.findAll('span',{'class':'Trsdu(0.3s)'})
        span = spanTags[-1].get_text()


        with open('yahoo_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
            csv_writer = writer(f)
            headers = ['TargetPrice']
            csv_writer.writerow(headers)
            csv_writer.writerow([span])
    print("all done")
            

def get_nasdaqSite_target_prices():
    count=0
    stockTicker = StockDetail.objects.all()
    for ticker in stockTicker:
        if ticker.stock_symbol=='LBTYK':
            continue
        else:
            response = requests.get('https://www.nasdaq.com/symbol/{}/analyst-research'.format(ticker.stock_symbol))
            soup = BeautifulSoup(response.text,'html.parser')
            tdTags = soup.findAll('td')
            tag = tdTags[5].get_text()
            tagSplit=tag.split()
            tp = tagSplit[1]

            with open('nasdaq.com_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
                csv_writer = writer(f)
                headers = ['TargetPrice']
                csv_writer.writerow(headers)
                csv_writer.writerow([tp])
                count+=1
                print(count)
    print("all done")


def get_stocktargetadvisior_target_prices():
    count=0
    stockTicker = StockDetail.objects.all()
    print(stockTicker[count])
    try:
        for ticker in stockTicker:
            if ticker.stock_symbol=='LBTYK' or ticker.stock_symbol=='FOX':
                continue
            else:
                response = requests.get('https://www.stocktargetadvisor.com/stock/USA/NSD/{}'.format(ticker.stock_symbol))
                soup = BeautifulSoup(response.text,'html.parser')
                spanTags = soup.findAll('span')
                tag = spanTags[26].get_text()
                tagSplit=tag.split()
                tp = tagSplit[1]

                with open('stocktargetadvisor_target_prices/{}.csv'.format(ticker.stock_symbol),'w') as f:
                    csv_writer = writer(f)
                    headers = ['TargetPrice']
                    csv_writer.writerow(headers)
                    csv_writer.writerow([tp])
                    count+=1
                    print(count)
        print("all done")
    except:
        print(stockTicker[count])