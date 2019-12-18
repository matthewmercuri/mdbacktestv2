import os
from datetime import datetime, timedelta
from loggingmod import Log
import pandas as pd
from portfolio import Portfolio


class Backtest(Log):

    def __init__(self, start_cash, tickers, benchmark, start_date, end_date):
        ''' We're going to have to eventually have instance variables
        that allow shortselling or options trading
        '''
        self.benchmark = benchmark
        self.tradeables = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.trade_date = start_date
        self.buy_stock_com = 0
        self.sell_stock_com = 0
        self.closed_pnl = 0
        self.log_df = self._create_log_df()
        self.Portfolio = Portfolio(start_cash)
        self._validate()

    def _validate(self):
        tradeables = self.tradeables
        tradeables.append(self.benchmark)

        for tradeable in tradeables:
            if os.path.exists(f'stockdata/{tradeable}.csv') is False:
                ''' Should go and get file if it does not already exist
                '''
                raise NameError(f'{tradeable} does not have a file!')

            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            if self.start_date not in df.index or self.end_date not in df.index:
                print(f'The start or end date is not available for {tradeable}.')

        print('All downloaded data has been validated!')

    def _check_day(self):
        ''' Going to have to fix this when it comes time to trade tickers
        that may or may not have been listed
        '''
        for tradeable in self.tradeables:
            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            if self.trade_date not in df.index:
                self.advance_day()
                print(f'{self.trade_date} is not in {tradeable} data. Advancing...')

    def _get_todays_date(self):
        ''' function should just return todays trading date
        '''
        pass

    def _check_current_positions(self, symbol):
        ''' Checks current positions to see if it currently exists in the
        portolio
        '''
        df = self.Portfolio.stock_positions
        if df.index == symbol:
            return True
        else:
            return False

    def _check_valid_buy(self, price, quantity):
        ''' should be different in certain situaitons. E.g. allowing
        short-selling or options. Certain procedures must be excecuted
        regardless. Might be different if trading percentages instead
        of dollar amounts.
        '''
        total_price = quantity * price
        if total_price > self.Portfolio.cash:
            return False
        else:
            return True
        pass

    def _purchase_sale_helper(self, symbol, quantity):
        '''  Need to work in commissions with cost basis. Have to be
        adding a 'Closed PnL' to each holding in stock_positions df
        '''
        stock_port_df = self.Portfolio.stock_positions

        price = self._get_todays_price(symbol)

        if self._check_valid_buy(price, quantity) is True:
            if self._check_current_positions(symbol) is True:
                stock_port_df = stock_port_df.loc[symbol]
                if stock_port_df['Quantity'] + quantity == 0:
                    df = self.Portfolio.stock_positions
                    df.drop(symbol, inplace=True)
                    self.Portfolio.stock_positions = df
                else:
                    stock_port_df['Quantity'] = stock_port_df['Quantity'] + quantity
                    stock_port_df['Cost Basis'] = (stock_port_df['Quantity'] * price) / stock_port_df['Quantity']
                    self.Portfolio.stock_positions.loc[symbol] = stock_port_df
            else:
                addition = {'Quantity': quantity, 'Cost Basis': price}
                stock_port_df.loc[symbol] = addition
                self.Portfolio.stock_positions = stock_port_df
        else:
            ''' What do we do when there is not a valid transaction requested?
            '''
            pass

    def _get_todays_price(self, symbol):
        _todays_df = self.get_todays_df()
        self.todays_date = _todays_df.index[0]
        _todays_df = _todays_df[_todays_df['Symbol'] == symbol]
        price = _todays_df['Adjusted Close'].iloc[0]
        return price

    def _find_pnl_on_trans(self, symbol, quantity, current_port_df, buy_or_sell):
        ''' Should also return transaction PnL. Fix situation where if
        the trade executes for a quantity that changes the net long or
        short,it'll remain accurate. Maybe only pass quantity that will
        make the net quantity zero?
        '''
        current_port_df = self.Portfolio.stock_positions
        current_port_df = current_port_df.loc[symbol]

        price = self._get_todays_price(symbol)

        if current_port_df['Quantity'] > 0 and buy_or_sell == 'sell':
            trans_pnl = quantity*(price - current_port_df['Cost Basis'])
            self.closed_pnl += trans_pnl
        elif current_port_df['Quantity'] < 0 and buy_or_sell == 'buy':
            trans_pnl = quantity*(current_port_df['Cost Basis'] - price)
            self.closed_pnl += trans_pnl
        else:
            raise ValueError('Unable to calculate PnL!')

        return trans_pnl

    def set_stock_commissions(self, buy_comm, sell_comm):
        self.buy_stock_com = buy_comm
        self.sell_stock_com = sell_comm

    def advance_day(self):
        self.trade_date = datetime.strptime(self.trade_date, '%Y-%m-%d') + timedelta(days=1)
        self.trade_date = str(self.trade_date.strftime('%Y-%m-%d'))
        self._check_day()

    def get_todays_df(self):
        ''' We need to construct a temporary df that combines all the stock
        data for any given day. We also need to add a symbol column. This could
        be made more efficient possibly. For some reason, we can't call this twice.
        THIS HAPPENED BECAUSE I USE THE SAME NAME FOR METHOD AND ATRIBUTE.
        '''
        stock_dfs_list = []

        for tradeable in self.tradeables:
            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            df['Symbol'] = tradeable
            df = df.loc[[self.trade_date]]
            stock_dfs_list.append(df)
        self._todays_df = pd.concat(stock_dfs_list, axis=0, sort=True)
        return self._todays_df

    def buy_stock(self, symbol, quantity):
        ''' Should log trade
        '''
        trans_pnl = -self.buy_stock_com
        self.closed_pnl -= self.buy_stock_com
        price = self._get_todays_price(symbol)

        if self._check_current_positions(symbol) is True:
            current_port_df = self.Portfolio.stock_positions
            current_port_df = current_port_df.loc[symbol]
            trans_pnl += self._find_pnl_on_trans(symbol, quantity, current_port_df, 'buy')

        self._purchase_sale_helper(symbol, quantity)
        date = self.todays_date
        self.log_trade(date, symbol, 'Buy', quantity, price, trans_pnl)

    def sell_stock(self, symbol, quantity):
        ''' Should log trade
        '''
        trans_pnl = -self.sell_stock_com
        self.closed_pnl -= self.sell_stock_com
        price = self._get_todays_price(symbol)

        if self._check_current_positions(symbol) is True:
            current_port_df = self.Portfolio.stock_positions
            current_port_df = current_port_df.loc[symbol]
            trans_pnl += self._find_pnl_on_trans(symbol, quantity, current_port_df, 'sell')

        self._purchase_sale_helper(symbol, -quantity)
        date = self.todays_date
        self.log_trade(date, symbol, 'Sell', quantity, price, trans_pnl)
