import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NTQ3ODE5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.xC4uOx0WmfKHjjNJbSWLsGWj3Aubuko47tnsBw-QlVQTcGkrBtnHwPPIDv0Hth3tbg96CyFtSHnGmy1ogB9eaQ"
tsl         = Tradehull(client_code,token_id)


candlestick_chart = tsl.get_historical_data(tradingsymbol = 'NIFTY',exchange = 'INDEX',timeframe="5")
hikenasi_chart    = tsl.heikin_ashi(df=candlestick_chart)
renko_chart       = tsl.renko_bricks(data=candlestick_chart, box_size=5)

pdb.set_trace()

tsl.send_telegram_alert(message="Order executed: BUY 50 shares of RELIANCE",receiver_chat_id="5726979878",bot_token="5189311784:AAHgQxiQ6uhc1Qf7AvPAiUoUzxetu8uKP58")


