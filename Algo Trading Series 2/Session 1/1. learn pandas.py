
import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib


client_code = "1102790337"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM3NTIzMDg4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc5MDMzNyJ9.UWD34xX9VHFQ9ULmjhiufvqp-jzrDXFpKKOLVj0ix6wDVxOUZDmScAiQc-TBN_-TDT7wZl5AjLsFMFiuwrVciQ"


tsl         = Tradehull(client_code,token_id)
chart       = tsl.get_historical_data(tradingsymbol = 'TATAMOTORS',exchange = 'NSE',timeframe="5")




pdb.set_trace()
chart = tsl.get_historical_data(tradingsymbol = 'SENSEX 27 DEC 78500 CALL',exchange = 'BFO',timeframe="5")


tsl.get_historical_data(‘SENSEX 27 DEC 78500 CALL’, exchange=‘BFO’, timeframe=“5”)

ltp   = tsl.get_ltp_data(names = ['NIFTY DEC FUT'])


chart.sort_values(by="close")


new_chart = chart.set_index(chart['timestamp'])


# 5th   candle     iloc
# 10:35 candle      loc




