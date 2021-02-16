import sys
sys.path.insert(0, 'Utils')
import Utils.utilities as utils
import quandl
import os
import pandas as pd 
import datetime as dt 
import pandas_datareader.data as web
#import fix_yahoo_finance

# to do: 
# make moving average code more robust 
# url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

tickers = ['TSLA', 'GS', 'BML-J', 'MSFT']
start = dt.datetime(2017, 1, 1)
end = dt.datetime.now()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():
    #tickers = utils.get_all_the_stocks(1)['NYSE'] # dict {exchange:list_of_tickers}
    tickers = utils.read_sp500_tickers()

    for ticker in tickers:
        path = os.path.join("DATA/CSV", ticker + '.csv')

        stock_write = utils.stock_history_to_csv(ticker, path, start, end, 0)
        if not stock_write:
            continue

        df = utils.read_stocks_from_csv(path)
        # df_ma = moving_average(df)
        # plt = plot_candlestick(df, '10D')
        # plt = plot_history(df, 1)


if __name__ == "__main__":
    main()
