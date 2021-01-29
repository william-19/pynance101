import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd 
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

style.use('ggplot')
df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

#rolling window tuh artinya dia mau ambil dari 100 data sebelumnya terus di mean
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

#ilangin 99 hari pertama soalnya 100ma nya Nan. 
#dropnanya diilangin soalnya uda pake min period=0. kalo defaultnay min period=100 soalnya window =100
#df.dropna(inplace=True)

print(df.head())

#first parameter is the grip dimension(6 rows 1 column), then start at 0,0 , then rowspan and colspan
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=5, colspan=1, sharex=ax1)
#share x tuh biar kalo dia zoom yang pertama, yang dibawahnay kezoom juga

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()