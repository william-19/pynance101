#how to get s&p500 list by using beautiful soup to webscrape
import bs4 as bs
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
        ticker = row.findAll('td')[0].text.replace('.','-').strip()
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        #to dump tickers to f
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

save_sp500_tickers()