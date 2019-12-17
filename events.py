from data import Data
import os
import pandas as pd


class Events(Data):

    def __init__(self):
        pass

    def _check_file_exists(self, ticker):
        if os.path.exists(f'stockdata/{ticker}.csv') is False:
            raise NameError(f'{ticker} does not have a file!')

    def _type_checker(self, tickers):
        if isinstance(tickers, list):
            for ticker in tickers:
                if not isinstance(ticker, str):
                    raise TypeError(f'{ticker} is not a string!')
            return 'list'
        if not isinstance(tickers, str):
            raise TypeError(f'{tickers} is not a string!')
        else:
            return 'symbol'

    def _return_sma(self, df, ticker, period):
        df[f'{period}_SMA'] = df['Adjusted Close'].rolling(window=period).mean()
        df.to_csv(f'stockdata/{ticker}.csv')

    def _return_daily_percent_change(self, df, ticker):
        df['Daily % Change'] = df['Adjusted Close'].pct_change()
        df.to_csv(f'stockdata/{ticker}.csv')

    def daily_percent_change(self, tickers):
        if self._type_checker(tickers) == 'list':
            for ticker in tickers:
                self._check_file_exists(ticker)
                df = pd.read_csv(f'stockdata/{ticker}.csv', index_col='Date')
                self._return_daily_percent_change(df, ticker)
        elif self._type_checker(tickers) == 'symbol':
            self._check_file_exists(tickers)
            df = pd.read_csv(f'stockdata/{tickers}.csv', index_col='Date')
            self._return_daily_percent_change(df, tickers)

    def sma(self, tickers, period):
        if self._type_checker(tickers) == 'list':
            for ticker in tickers:
                self._check_file_exists(ticker)
                df = pd.read_csv(f'stockdata/{ticker}.csv', index_col='Date')
                self._return_sma(df, ticker, period)
        elif self._type_checker(tickers) == 'symbol':
            self._check_file_exists(tickers)
            df = pd.read_csv(f'stockdata/{tickers}.csv', index_col='Date')
            self._return_sma(df, tickers, period)
