class Actions:
    '''Have to figure out a way where everytime a method
    in this class is called, it goes out and gets the
    current df and portfolo
    '''

    def _test(self):
        print(self.todays_df())

    def _check_valid_buy(self, symbol, quantity):
        pass

    def _check_valid_sell(self, symbol, quantity):
        pass

    def buy(self, symbol, quantity, todays_df, portfolio):
        print(todays_df)
        print(portfolio)

    def sell(self, symbol, quantity, todays_df, portfolio):
        pass
