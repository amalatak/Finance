import sys
sys.path.insert(0, 'Utils')
import Utils.dataUtils as dataUtils
import Utils.Analysis.plotUtils as plotUtils
import Utils.Analysis.trendUtils as trendUtils
import quandl
import os
import pandas as pd 
import datetime as dt 
import pandas_datareader.data as web
import matplotlib.pyplot as plt
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
    #utils.save_sp500_tickers()
    #tickers = utils.read_sp500_tickers()

    #exchanges = dataUtils.download_exchanges()

    #tickers = dataUtils.download_tickers_in_exchange(exchanges[9])

    df = dataUtils.read_stocks_from_csv('AAPL')

    maco = trendUtils.moving_average_crossover(df, 30, 100)

    apple_ma100 = trendUtils.moving_average(df)
    apple_ma30 = trendUtils.moving_average(df, 30)

    plt.figure(2)
    plt.plot(df['Adj Close'])
    plt.plot(apple_ma100)
    plt.plot(apple_ma30)
    plt.legend(['RT', 'MA 100', 'MA 30'])

    plt.xlabel('Time')
    plt.ylabel('Price ($USD)')
    plt.title('APPLE INC Price History')
    plt.show()


    #for ticker in tickers:
    #    path = os.path.join("DATA/CSV", ticker + '.csv')

    #    stock_write = utils.stock_history_to_csv(ticker, path, start, end, 0)
    #    if not stock_write:
    #        continue

    #    df = utils.read_stocks_from_csv(path)
        # df_ma = moving_average(df)
        # plt = plot_candlestick(df, '10D')
        # plt = plot_history(df, 1)


if __name__ == "__main__":
    main()
