import pdb
from Dhan_Tradehull_V2 import Tradehull
import pandas as pd
import talib
import time
import datetime

client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM0MDcxMzE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.4i-edsCp4Z2r6Z82ewoZFW_enhENZ_4p1IdJcED5fROHGiqSqy_3yglYblDKlWIJIM8S9VM4ZwXfqd3T0ZfVZg"




tsl = Tradehull(client_code,token_id)

pre_market_watchlist = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC', 'BPCL', 'WIPRO', 'SHRIRAMFIN', 'ADANIPORTS', 'JSWSTEEL', 'COALINDIA', 'ULTRACEMCO', 'BAJAJ-AUTO', 'LT', 'POWERGRID', 'ADANIENT', 'SBIN', 'HCLTECH', 'TCS', 'EICHERMOT', 'BAJAJFINSV', 'TECHM', 'LTIM', 'HINDUNILVR', 'BHARTIARTL', 'AXISBANK', 'GRASIM', 'HEROMOTOCO', 'DRREDDY', 'ICICIBANK', 'HDFCBANK', 'BAJFINANCE', 'SBILIFE', 'RELIANCE', 'KOTAKBANK', 'ITC', 'TITAN', 'SUNPHARMA', 'INDUSINDBK', 'APOLLOHOSP', 'BRITANNIA', 'NESTLEIND', 'HDFCLIFE', 'DIVISLAB', 'CIPLA', 'ASIANPAINT', 'TATACONSUM']


body_dict = {}
tarde_info = {}




for name in pre_market_watchlist:
	time.sleep(1)
	print(f"Pre market scanning {name}")
	daily_data = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")
	ldc = daily_data.iloc[-1]  #last_day_candle
	body_percentage = ((ldc['close'] - ldc['open'])/ldc['open'])*100

	body_dict[name] = round(body_percentage, 2)



script_having_max_body = max(body_dict, key=body_dict.get)
daily_data = tsl.get_historical_data(tradingsymbol = script_having_max_body, exchange = 'NSE',timeframe="DAY")
ldc = daily_data.iloc[-1]  #last_day_candle
tarde_info = {"Direction":"buy", "level":ldc['high']}


print(script_having_max_body)
print(tarde_info)


