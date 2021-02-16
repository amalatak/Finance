import os
import string
import csv
import numpy as np 
import scipy as scp 
import statistics as stat 
import datetime as dt 
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd 
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
import bs4 as bs
import pickle
import requests

register_matplotlib_converters()
style.use('ggplot')

# web services
def save_sp500_tickers(base_dir="ExchangeTickers"):
    url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker.rstrip())
    with open(base_dir + "/sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

def get_exchange_tickers_from_web(exchange):
    web_url = 'http://eoddata.com/stocklist/'
    alphabet = list(string.ascii_uppercase)
    tickers = []
    base_url = web_url + exchange + '/'
    for letter in alphabet:
        url = base_url + letter + '.htm'
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, 'lxml')
        find_str = '/' + exchange + '/'
        for row in soup.findAll('table')[5].findAll('tr'):
            row = row.find('td')
            row_str = str(row)
            ticker = row_str[(row_str.find(find_str) + len(find_str)):row_str.find('.htm')]
            if ticker:
                tickers.append(ticker)
    return tickers
        
def get_exchanges_from_web():
    url = 'http://eoddata.com/symbols.aspx'
    find_str = 'value='
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'lxml')
    exchanges = []
    for row in soup.findAll('table')[2].findAll('select')[0].findAll('option'):
        row_str = str(row)
        if find_str in row_str:
            exchanges.append(row_str[row_str.find(find_str) + len(find_str):row_str.find('>')].strip('"'))
    return exchanges

# Saving Files to CSV or TXT
def stock_history_to_csv(ticker, path, start, end, overwrite_flag=0):
    if (not os.path.exists(path)) or overwrite_flag:
        print('writing {} history to {}'.format(ticker, path))
        try:
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv(path)
            return 1
        except Exception as e:
            print("Unable to write {} to csv".format(ticker))
            print(str(e))
            return 0

def save_exchange_tickers(exchange, base_dir='ExchangeTickers', overwrite_flag=0):
    path_to_exchange = os.path.join(base_dir, exchange + '.txt')
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    if (not os.path.exists(path_to_exchange)) or overwrite_flag:
        try:
            tickers = get_exchange_tickers_from_web(exchange)
            with open(path_to_exchange, 'w+') as write_file:
                for ticker in tickers:
                    write_file.write("{}\n".format(ticker))
            return tickers
        except:
            print('Could not get list of tickers from {}'.format(exchange))


# Read Values
def read_tickers(exchange, base_dir='ExchangeTickers'):
    path_to_exchange = os.path.join(base_dir, exchange + '.txt')
    tickers = []
    try:
        with open(path_to_exchange, 'r') as read_file:
            for line in read_file:
                tickers.append(line.rstrip())
        return tickers
    except:
        print('{} not found'.format(path_to_exchange))

def read_sp500_tickers(base_path="Data/ExchangeTickers"):
    with open(base_path + "/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    return tickers

def read_stocks_from_csv(path):
    df = pd.read_csv(path, parse_dates=True, index_col=0)
    df.set_index('Date', inplace=True)
    return df

# Resampling 
def moving_average(dataframe, days=100):
    dataframe[str(days) +'ma'] = dataframe['Adj Close'].rolling(window=days, min_periods=0).mean()
    return dataframe

def resample_ohlc(dataframe, rate='10D'):
    df_ohlc = dataframe['Adj Close'].resample(rate).ohlc()
    return df_ohlc

def resample_volume(dataframe, rate='10D'):
    df_volume = dataframe['Volume'].resample('10D').sum()
    return df_volume

# plotting
# wont work with a different ma
def plot_history(stock_df, ma_flag=0):

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

    ax1.plot(stock_df.index, stock_df['Adj Close'])
    ax2.bar(stock_df.index, stock_df['Volume'])
    if ma_flag:
        if '100ma' in stock_df.columns:
            ax1.plot(stock_df.index, stock_df['100ma'])
        else:
            print('Column {} not in dataframe'.format('100ma'))
    return plt

def plot_candlestick(stock_df, resample=''):
    if resample:
        df_ohlc = stock_df['Adj Close'].resample(resample).ohlc()
        df_volume = stock_df['Volume'].resample(resample).sum()
        df_ohlc.reset_index(inplace=True)
    else:
        df_ohlc = stock_df
        df_volume = stock_df['Volume']
        df_ohlc.reset_index(inplace=True)
    
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    return plt


# get all the stocks
def get_all_the_stocks(rewrite=0):
    print('\nGetting all stock tickers from exchanges')
    exchanges = get_exchanges_from_web()
    all_the_stocks = {}

    for exchange in exchanges:
        print(exchange)
        if rewrite:
            tickers = save_exchange_tickers(exchange, overwrite_flag=1)
            all_the_stocks.update({exchange:tickers})
        else:
            tickers = read_tickers(exchange)
            all_the_stocks.update({exchange:tickers})
    return all_the_stocks


# Operations
def compile_data(tickers):
    main_df = pd.DataFrame()
    for ticker in tickers:
        df = read_stocks_from_csv("CSV/{}".format(ticker))