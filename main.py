from backtester import Backtest
from actions import Actions
import pandas as pd


''' Eventually we would want to load these from a config file
'''
start_cash = 10000
benchmark = 'SPY'
tickers = ['AAPL', 'AMD']
start_date = '2002-03-27'
end_date = '2019-12-13'

Backtest = Backtest(start_cash, tickers, benchmark, start_date, end_date)
#Actions = Actions(start_cash, tickers, benchmark, start_date, end_date)
#Actions._test()

Backtest.set_stock_commissions(5, 5)
Backtest.buy_stock('AAPL', 2)
Backtest.sell_stock('AAPL', 2)
#Backtest.buy_stock('AAPL', -2)
#Backtest.buy('AAPL', 2)
Backtest.buy_stock('AMD', 2)
print(Backtest.Portfolio.stock_positions)

def main():
    pass

    #Backtest.Actions.buy('AAPL', 2)
    #for i in range(1, 3):
        #print(Backtest.Actions.buy('AAPL', 2))
        #Backtest.advance_day()


main()
