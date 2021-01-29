#get the data of s&p500 companies
import bs4 as bs
import datetime as dt
import os
import pandas as pd
import yfinance as yf
#import pandas_datareader.data as web
from pandas_datareader import data as pdr
yf.pdr_override()
#to serialize any python object 
import pickle 
import requests


def save_sp500_tickers() :
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    #to get the text of a source code use resp.txt
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable', 'id':"constituents"})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace(".","-").strip()
        tickers.append(ticker)

    #wb is for write, rb is for read
    with open("sp500tickers.pickle", "wb") as f:
        #to dump tickers to f
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

def get_data_from_yahoo(reload_sp500 = False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            #df = web.DataReader(ticker, 'yahoo', start, end)
            df = pdr.get_data_yahoo(ticker, start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

save_sp500_tickers()
get_data_from_yahoo()

#maybe need time.sleep(1) if there is a throttle in thte scraping process