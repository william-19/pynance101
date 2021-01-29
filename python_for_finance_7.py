#to combine all the stocks from the stock dfs folder
#the previous file is done because retrieveing the data locally is faster, later please discuss with others
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

#maybe need time.sleep(1) if there is a throttle in thte scraping process
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


def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    #create empty dataframe
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        #1 is to drop the axis 1
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

        if main_df.empty:
            main_df=df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_join_closes.csv')

#save_sp500_tickers()
#get_data_from_yahoo()
compile_data()