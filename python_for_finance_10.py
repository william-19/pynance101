import numpy as np
import pandas as pd
import pickle

#can we take many companies all together, does it affect the performance of the current stock we are interested in?
#features define something 
#label is target
# buy sell or hold? threshold for everythign is 2 percent

def process_data_for_labels(ticker):
    hm_days = 7 #in thenext 7 days, will it move up or down? how big is the change?
    df = pd.read_csv('sp500_join_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0,inplace=True)
    #print(df.head())
    return tickers, df


#learn about args and kwargs
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col>requirement:
            return 1
        if col<-requirement:
            return -1
    return 0 

#process_data_for_labels('XOM')
#buy_sell_hold()