import yfinance as yf   #yahoo finance API for candles
import pandas as pd     #formatting/datasets library
import pytz             #timezone library
from datetime import datetime, date, timedelta
import pandas_market_calendars as mcal #gets trading days, skips days where market is not open



# datetime with only valid market days
now = datetime.now(pytz.timezone("US/Eastern"))
print("Now in US/East:", now)
today = date.today()




balance = 10000
start_balance=balance
top_balance = balance
fee_rate = 0.0002 #percentage
max_leverage = 4
take_position_minimum = 0.002 #minimum % slip in first candle to open the position
ticker = "QQQ "  #title symbol
futures_ticket = "NQ=F" 
start_date = "2025-06-08"
end_date = "2025-07-07"
total_plays=0
wins=0
losses=0



#startegy:
# orb with first candle and last futures candle
# mix news analyzed by LLM
