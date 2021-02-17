import pandas_datareader.data as web
import pandas as pd 

# Moving Average
def moving_average_append(dataframe, days=100, column='Adj Close'):
    dataframe[str(days) +'ma'] = dataframe['Adj Close'].rolling(window=days, min_periods=0).mean()
    print(dataframe[column].rolling(window=days, min_periods=0).mean())
    return dataframe

def moving_average(dataframe, days=100, column='Adj Close'):
    return dataframe[column].rolling(window=days, min_periods=0).mean()

def moving_average_crossover(dataframe, short_period, long_period):
    ma_short = moving_average(dataframe, days=short_period)
    ma_long = moving_average(dataframe, days=long_period)


    return 0


# Some other stuff
def resample_ohlc(dataframe, rate='10D'):
    df_ohlc = dataframe['Adj Close'].resample(rate).ohlc()
    return df_ohlc

def resample_volume(dataframe, rate='10D'):
    df_volume = dataframe['Volume'].resample('10D').sum()
    return df_volume
