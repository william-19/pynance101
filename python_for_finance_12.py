from collections import Counter
import numpy as np
import pandas as pd
import pickle
#what is this
#cross validation for testing, neighbors for k nearest neighbours
#votingclassifier for using many classifier to further stabilize the result, same as random forest...
from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


#can we take many companies all together, does it affect the performance of the current stock we are interested in?
#features define something 
#label is target
# buy sell or hold? threshold for everythign is 2.5 percent

def process_data_for_labels(ticker):
    hm_days = 7 #in thenext 7 days, will it move up or down? how big is the change?
    df = pd.read_csv('sp500_join_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0,inplace=True)
    #print(df.head())
    return tickers, df, hm_days


#learn about args and kwargs
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.025
    for col in cols:
        if col>requirement:
            return 1
        if col<-requirement:
            return -1
    return 0 


def extract_featuresets(ticker):
    tickers, df, hm_days = process_data_for_labels(ticker)
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker,i)] for i in range(1,hm_days+1)]))

    """     
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, 
                                                df['{}_1d'.format(ticker)],
                                                df['{}_2d'.format(ticker)],
                                                df['{}_3d'.format(ticker)],
                                                df['{}_4d'.format(ticker)],
                                                df['{}_5d'.format(ticker)],
                                                df['{}_6d'.format(ticker)],
                                                df['{}_7d'.format(ticker)])) 
    """

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))
    
    df.fillna(0,inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df


def do_ml(ticker):
    #X is the percent changes of all the company, y is the target(0 for hold 1 for buy -1 for sell)
    X, y, df = extract_featuresets(ticker)
    #25 percent of the sample data will be tested (from test size)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.25)

    #clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print("Accuracy confidence:",confidence)
    predictions = clf.predict(X_test)
    print("Predicted spread:", Counter(predictions))

    return confidence

do_ml('BAC')