# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plotting tools
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import matplotlib.pyplot as plt
from matplotlib import style

# plt.style.use('fivethirtyeight')

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