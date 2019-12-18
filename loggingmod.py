import pandas as pd

LOGCOLS = ['Trade Date', 'Symbol', 'Action', 'Quantity', 'Price', 'Trans PnL']


class Log:

    def _create_log_df(self):
        self.log_df = pd.DataFrame(columns=LOGCOLS)
        self.log_df = self.log_df.set_index('Trade Date')

    def log_trade(self, date, symbol, action, quantity, price, trans_pnl):
        ''' Need to figure out how to get the index to be the date of trade
        '''
        data = [date, symbol, action, quantity, price, trans_pnl]
        trade_df = pd.DataFrame([data], columns=LOGCOLS)
        trade_df = trade_df.set_index('Trade Date')
        self.log_df = pd.concat([self.log_df, trade_df], ignore_index=True)

    def save_log_locally(self):
        pass
