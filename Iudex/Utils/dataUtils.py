"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Utilities file for downloading, storing, and getting 
market data



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

import bs4 as bs
import requests
import string
import os
import pandas_datareader.data as web
import pandas as pd 
import pickle

# CONSTANTS
BASE_EXCHANGE_TICKER_DIR = 'Data/ExchangeTickers'
BASE_STOCK_DATA_DIR = 'Data/CSV'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Web functionality
# - download data from the web and return it
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def download_exchanges():
    """
        Get a list of stock exchanges from the interwebs 
    """

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


def download_tickers_in_exchange(exchange):
    """
        Download all tickers in a given exchange
    """

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Write functionality
# - Write data to files
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_sp500_tickers(base_dir=BASE_EXCHANGE_TICKER_DIR):
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

def save_exchange_tickers(exchange, base_dir=BASE_EXCHANGE_TICKER_DIR, overwrite_flag=0):
    """
        Save a list of tickers in a given exchange
    """
    path_to_exchange = os.path.join(base_dir, exchange + '.txt')
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    if (not os.path.exists(path_to_exchange)) or overwrite_flag:
        try:
            tickers = download_tickers_in_exchange(exchange)
            with open(path_to_exchange, 'w+') as write_file:
                for ticker in tickers:
                    write_file.write("{}\n".format(ticker))
            return tickers
        except:
            print('Could not get list of tickers from {}'.format(exchange))


def save_stock_history_to_csv(ticker, start, end, base_path=BASE_EXCHANGE_TICKER_DIR, overwrite_flag=0):
    """
        Save stock history as CSV
    """
    path = os.path.join(base_path, ticker + '.csv')
    
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Read functionality
# - Read data from files
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def read_sp500_tickers(base_path=BASE_EXCHANGE_TICKER_DIR):
    with open(base_path + "/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    return tickers

def read_tickers_in_exchange(exchange, base_dir=BASE_EXCHANGE_TICKER_DIR):
    """
        Read from a list of tickers in a given exchange
    """

    path_to_exchange = os.path.join(base_dir, exchange + '.txt')
    tickers = []
    try:
        with open(path_to_exchange, 'r') as read_file:
            for line in read_file:
                tickers.append(line.rstrip())
        return tickers
    except:
        print('{} not found'.format(path_to_exchange))

def read_stocks_from_csv(ticker, base_path=BASE_STOCK_DATA_DIR):
    """
        Read a given stocks data in a given CSV
    """

    path = os.path.join(base_path, ticker + '.csv')
    df = pd.read_csv(path, parse_dates=True, index_col=0)
    return df


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Combined functionality
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_all_the_stocks(rewrite=0):
    """ 
        Loop through exchanges and get list of all tickers in each exchange
    """
    print('\nGetting all stock tickers from exchanges')
    exchanges = download_exchanges()
    all_the_stocks = {}

    for exchange in exchanges:
        print(exchange)
        if rewrite:
            tickers = save_exchange_tickers(exchange, overwrite_flag=1)
            all_the_stocks.update({exchange:tickers})
        else:
            tickers = read_tickers_in_exchange(exchange)
            all_the_stocks.update({exchange:tickers})
    return all_the_stocks