from data import Data
from events import Events
import pandas as pd

Data = Data()
Events = Events()

Data.gather_data(['AAPL', 'SPY', 'AMD'])
Events.sma('AAPL', 20)
Events.daily_percent_change('AAPL')

df = pd.read_csv('stockdata/AAPL.csv', index_col="Date")
print(df.tail())