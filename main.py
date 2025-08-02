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
futures_ticker = "NQ=F" 
start_date = "2025-06-08"
end_date = "2025-07-07"
ticker_exchange = "NASDAQ"
futures_exchange = "CME"

total_plays=0
wins=0
losses=0


#calendar setup
calendar = mcal.get_calendar(ticker_exchange)
f_calendar = mcal.get_calendar(futures_exchange)
t_schedule =  calendar.schedule(start_date=start_date, end_date=end_date)
f_schedule = f_calendar.schedule(start_date=start_date, end_date=end_date)

trading_days = t_schedule.index.date
f_trading_days = f_schedule.index.date



    #startegy:
# orb with first candle and last futures candle
# mix news analyzed by LLM


#tc = ticker candle, fc = futures ticker
def ORB (tc, fc):       

    if (round((abs(tc.iloc[0]["Open"][ticker] - tc.iloc[0]["Close"][ticker]) / tc.iloc[0]["Open"][ticker]),2) < take_position_minimum ): #checks if theres enough slip to make the strategy work
        return "t-noslip"
    else:

        if ( round((abs(fc.iloc[0]["Open"][futures_ticker] - fc.iloc[0]["Close"][futures_ticker]) / fc.iloc[0]["Open"][futures_ticker]), 2) > take_position_minimum ): #checks if futures has enough slip
            
            if tc.iloc[0]["Open"][ticker] < tc.iloc[0]["Close"][ticker]:

                if fc.iloc[0]["Open"][futures_ticker] < fc.iloc[0]["Close"][futures_ticker]: # futures and ticker have same momentum

                    return "Long"
                
                else:
                    
                    return 0
            else:

                if fc.iloc[0]["Open"][futures_ticker] > fc.iloc[0]["Close"][futures_ticker]:

                    return "Short"
                
                else:

                    return 0
                
        else:

            return "f_noslip"
        

def LIMIT (tc ,fc):  #sets stop limits

    if ORB (tc, fc) == 0:

        return 0
    
    if ORB (tc, fc) == "long":

        return tc.iloc[0]["Low"][ticker]
    
    if ORB (tc, fc) == "short":

        return tc.iloc[0]["High"][ticker]
    

def RISK (tc, fc):   #calculates risk

    if ORB (tc, fc) == 0:

        return 0
    
    else :

        return abs(tc.iloc[1]["Open"][ticker] - LIMIT(tc, fc))
    

def SIZE (tc, fc):   #define size of trade

    if ORB (tc, fc) == 0:
        
        return 0
    
    else :
        if RISK(tc, fc)==0:
            return 1
        return int(min( (balance*0.01/RISK(tc, fc)), (max_leverage*balance/tc.iloc[0]["Open"][ticker]) ))



def percentage( balance, profit): #gets percentage after the positoin is closed - returns a string!

    return "("+str(profit/balance*100)+"%)"

















for day in trading_days:  


    next_day = day + timedelta(days=1)
    t_candle = yf.download(ticker, start=str(day), end=str(next_day), interval="5m", progress=False, auto_adjust=False)
    

for day in f_trading_days:  

    next_day = day + timedelta(days=1)
    f_candle = yf.download(futures_ticker, start=str(day), end=str(next_day), interval="5m", progress=False, auto_adjust=False)
 
 
 
 
