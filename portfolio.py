import pandas as pd

STOCKPORTCOLS = ['Symbol', 'Quantity', 'Cost Basis']


class Portfolio:
    ''' Need to add PnL and market value functions
    '''
    def __init__(self, starting_cash):
        self.stock_positions = pd.DataFrame(columns=STOCKPORTCOLS)
        self.stock_positions = self.stock_positions.set_index('Symbol')
        self.cash = starting_cash
