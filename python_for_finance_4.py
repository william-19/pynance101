import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd 
#import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

style.use('ggplot')
df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

#rolling window tuh artinya dia mau ambil dari 100 data sebelumnya terus di mean
#df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

#ilangin 99 hari pertama soalnya 100ma nya Nan. 
#dropnanya diilangin soalnya uda pake min period=0. kalo defaultnay min period=100 soalnya window =100
#df.dropna(inplace=True)

#for resampling and get the ohlc(open,high,low,close). this is to prevent any error when the stock split somewhere in the timeframe
#difference between this and rolling is that this function reduce the total number of data (gabungin 10 hari jadi 1)
df_ohlc = df['Adj Close'].resample('10D').ohlc()
#to resample the volume section
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

df_ohlc['Date']= df_ohlc['Date'].map(mdates.date2num)
#print(df_ohlc.head())


#first parameter is the grip dimension(6 rows 1 column), then start at 0,0 , then rowspan and colspan
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=5, colspan=1, sharex=ax1)
#share x tuh biar kalo dia zoom yang pertama, yang dibawahnay kezoom juga
ax1.xaxis_date()

#width is the width of the candlestick, colorup is for the color for going up
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

#the x axis is filled with the mdates.... to show dates and the y axis will show the df_volume
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()